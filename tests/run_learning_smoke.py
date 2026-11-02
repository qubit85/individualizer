#!/usr/bin/env python3
"""Opt-in live profile-learning checks using synthetic files in a temporary workspace.

Each phase starts a fresh CLI session; only the profile persists between phases.
Requires an authenticated CLI and jsonschema. Consumes host model quota.
Raw logs and fixture snapshots remain in ignored work/; review before sharing.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def seed_profile(skill, destination):
    profile = json.loads((skill / 'assets/profile-template.json').read_text())
    profile.update(id='learning-test', name='Synthetic learning test', language='de', status='approved', approved_by_user=True)
    profile['customer_extension'] = {'preserve': ['exact']}
    profile['visual']['palette'] = [{'role': 'primary', 'hex': '#15324F'}]
    profile['learning'] = {
        'mode': 'automatic', 'automatic_updates_approved': True,
        'rules': [{
            'id': 'en-support-greeting', 'instruction': 'Start English support emails with Hello,',
            'scope': {'languages': ['en'], 'contexts': ['support emails']},
            'status': 'active', 'approval': 'explicit',
            'approval_source': 'User explicitly approved this English support-email greeting.',
            'evidence': [{'kind': 'explicit_preference', 'summary': 'User requested Hello, as the English support greeting.'}],
        }],
    }
    destination.mkdir()
    (destination / 'profile.json').write_text(json.dumps(profile, indent=2) + '\n')
    (destination / 'STYLE.md').write_text(
        '# Synthetic learning test\n\nProfile version: 1.0.0\nSchema version: 1.2\n'
        'Status: approved by the user.\nLanguage: de.\n'
        'Learning: automatic. The user authorized automatic learning from style corrections in this profile.\n'
        '## Active learned rules\n'
        '- en-support-greeting: Start English support emails with Hello,\n'
        '  Scope: en; support emails. Explicitly approved by the user.\n'
        '  Evidence: user requested this greeting.\n'
        '## Visual identity\nPrimary: #15324F.\n'
        '## Changelog\n- 1.0.0: Synthetic approved starting profile.\n')
    return profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, choices=['codex', 'claude'])
    parser.add_argument('--executable')
    parser.add_argument('--timeout', type=int, default=300)
    parser.add_argument('--phase', choices=['learn', 'recall', 'one-off', 'forget'], help='Run one phase only, starting from the synthetic baseline; recall alone does not test learned persistence.')
    args = parser.parse_args()
    executable = shutil.which(args.executable or args.runtime)
    if not executable:
        parser.error('Host CLI not found; set --executable if needed.')
    skill = ROOT / 'skill/individualizer'
    validator = Draft202012Validator(json.loads((skill / 'assets/profile.schema.json').read_text()))
    phases = json.loads((ROOT / 'tests/learning-scenarios.json').read_text())['phases']
    if args.phase:
        phases = [p for p in phases if p['id'] == args.phase]
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT / 'work/learning' / f'{args.runtime}-{timestamp}'
    output.mkdir(parents=True)
    metadata = {'runtime': args.runtime, 'cli_version': subprocess.check_output([executable, '--version'], text=True).strip(),
                'model_selection': 'configured host default; no override', 'phases': [],
                'skill_sha256': {str(f.relative_to(skill)): hashlib.sha256(f.read_bytes()).hexdigest()
                                 for f in sorted(skill.rglob('*')) if f.is_file()}}
    with tempfile.TemporaryDirectory(prefix='individualizer-learning-') as directory:
        workspace = Path(directory)
        installed = workspace / ('.agents' if args.runtime == 'codex' else '.claude') / 'skills/individualizer'
        shutil.copytree(skill, installed)
        baseline = seed_profile(skill, workspace / 'private')
        invocation = '$individualizer' if args.runtime == 'codex' else '/individualizer'
        for phase in phases:
            result_dir = output / phase['id']; result_dir.mkdir()
            prompt = (invocation + '\nUse the skill at ' + str(installed / 'SKILL.md') + '.\n' + phase['request'] +
                      '\nOnly use the supplied synthetic material, the selected private profile and this skill copy. '
                      'Write only private/profile.json and private/STYLE.md when this request authorizes learning. '
                      'Do not browse, publish, read unrelated user files, or change any other file.')
            (result_dir / 'prompt.txt').write_text(prompt)
            before = {name: (workspace / 'private' / name).read_bytes() for name in ['profile.json', 'STYLE.md']}
            if args.runtime == 'codex':
                command = [executable, 'exec', '--sandbox', 'workspace-write', '--ephemeral', '--skip-git-repo-check',
                           '--json', '-o', str(result_dir / 'final.txt'), '-']
            else:
                command = [executable, '--print', '--no-session-persistence', '--verbose', '--output-format', 'stream-json',
                           '--permission-mode', 'dontAsk', '--tools', 'Read,Skill,Write,Edit',
                           '--allowedTools', 'Read,Skill,Write,Edit', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}']
            record = {'id': phase['id']}
            with (result_dir / 'events.jsonl').open('w') as stdout, (result_dir / 'stderr.txt').open('w') as stderr:
                try:
                    result = subprocess.run(command, cwd=workspace, input=prompt, text=True, stdout=stdout, stderr=stderr, timeout=args.timeout)
                    record['exit_code'] = result.returncode
                except subprocess.TimeoutExpired:
                    record.update(exit_code=124, timed_out=True)
            after = {name: (workspace / 'private' / name).read_bytes() for name in before}
            for name, data in after.items(): (result_dir / name).write_bytes(data)
            record['profile_pair_unchanged'] = before == after
            record['private_files'] = sorted(str(p.relative_to(workspace / 'private')) for p in (workspace / 'private').rglob('*') if p.is_file())
            try:
                saved = json.loads(after['profile.json'])
                errors = list(validator.iter_errors(saved))
                record['schema_valid'] = not errors
                record['unrelated_fields_preserved'] = (saved.get('customer_extension') == baseline['customer_extension']
                                                        and saved.get('visual') == baseline['visual'])
                record['rule_ids'] = [r['id'] for r in saved.get('learning', {}).get('rules', [])]
            except (ValueError, KeyError):
                record['schema_valid'] = False
            metadata['phases'].append(record)
            (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
            print(json.dumps({'output': str(result_dir), **record}), flush=True)
            if record['exit_code'] != 0:
                raise SystemExit(record['exit_code'])
    print('Completed. Review semantic outcomes and both profile files; process completion alone is not a pass.')


if __name__ == '__main__':
    main()
