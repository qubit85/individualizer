#!/usr/bin/env python3
"""Opt-in live host checks. Requires an authenticated CLI; consumes model usage.

Only skill files and source prompts enter the temporary test workspace.
Reference answers and reviews are never supplied to the tested runtime.
Raw host logs remain under ignored work/ and must not be published unreviewed.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def make_prompt(runtime, scenario):
    cases = json.loads((ROOT / 'tests/behavioral-cases.json').read_text())['cases']
    if scenario == 'explicit':
        invocation = '$individualizer' if runtime == 'codex' else '/individualizer'
        inputs = [{k: c[k] for k in ('id', 'language', 'request', 'input')} for c in cases]
        return invocation + '\nEdit each passage according to its request. Return a JSON object mapping each id to its finished text. Treat the passages as separate tasks.\n' + json.dumps(inputs, ensure_ascii=False)
    if scenario == 'implicit-de':
        return 'Überarbeite diesen KI-haften Text natürlich und sachlich. Behalte Sie-Anrede, Frist und die fehlende Zusage bei. Gib nur den fertigen Text zurück.\n\nWir möchten Sie darum bitten, eine Übermittlung der Unterlagen bis zum 12. November vorzunehmen. Eine Zusage können wir Ihnen derzeit noch nicht geben.'
    if scenario == 'implicit-en':
        return 'Lightly edit this AI-sounding paragraph while preserving its evidence and uncertainty. Return only the finished text.\n\nIt is worth noting that two testers said the search felt faster, although no timings have been recorded. Offline mode is planned, not available.'
    return 'What is 17 multiplied by 23? Return only the number.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, choices=['codex', 'claude'])
    parser.add_argument('--executable', help='Optional path when the host CLI is not on PATH')
    parser.add_argument('--scenario', required=True, choices=['explicit', 'implicit-de', 'implicit-en', 'unrelated'])
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    executable = shutil.which(args.executable or args.runtime)
    if not executable:
        parser.error(f'{args.runtime} is not installed')
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT / 'work/runtime' / f'{args.runtime}-{args.scenario}-{timestamp}'
    output.mkdir(parents=True)
    prompt = make_prompt(args.runtime, args.scenario)
    if args.scenario != 'unrelated':
        prompt += '\n\nUse only the supplied passages and relevant installed skill instructions. Do not browse, read unrelated user files, change files, or publish anything.'
    (output / 'prompt.txt').write_text(prompt)
    skill = ROOT / 'skill/individualizer'
    hashes = {str(f.relative_to(skill)): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(skill.rglob('*')) if f.is_file()}
    metadata = {'runtime': args.runtime, 'scenario': args.scenario, 'started_utc': timestamp,
                'model_selection': 'host default; no override', 'skill_sha256': hashes,
                'cli_version': subprocess.check_output([executable, '--version'], text=True).strip()}
    with tempfile.TemporaryDirectory(prefix='individualizer-smoke-') as directory:
        workspace = Path(directory)
        skills_dir = '.agents' if args.runtime == 'codex' else '.claude'
        shutil.copytree(skill, workspace / skills_dir / 'skills/individualizer')
        if args.runtime == 'codex':
            command = [executable, 'exec', '--sandbox', 'read-only', '--ephemeral',
                       '--skip-git-repo-check', '--json', '-o', str(output / 'final.txt'), '-']
        else:
            command = [executable, '--print', '--no-session-persistence', '--verbose',
                       '--output-format', 'stream-json', '--permission-mode', 'dontAsk',
                       '--tools', 'Read,Skill', '--allowedTools', 'Read,Skill',
                       '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}']
        with (output / 'events.jsonl').open('w') as stdout, (output / 'stderr.txt').open('w') as stderr:
            try:
                result = subprocess.run(command, cwd=workspace, input=prompt, text=True,
                                        stdout=stdout, stderr=stderr, timeout=args.timeout)
                metadata['exit_code'] = result.returncode
            except subprocess.TimeoutExpired:
                metadata['timed_out'] = True
                metadata['exit_code'] = 124
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'exit_code': metadata['exit_code']}))
    raise SystemExit(metadata['exit_code'])


if __name__ == '__main__':
    main()
