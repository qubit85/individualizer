# Validation

## Structural/profile checks

Run from the repository root:

```sh
python3 -m pip install -r tests/requirements.txt
python3 -m unittest discover -s tests -v
```

Python 3 and `jsonschema` are development dependencies, not requirements for the installed skill. `test_profiles.py` checks schema compatibility, approvals, language extensions, malformed profiles, and local runtime links. It does not evaluate prose quality.

## Live runtime smoke tests

These opt-in calls use your authenticated CLI and can consume model usage. The runner copies only the skill into a temporary workspace, passes source requests without candidate answers, and keeps raw output in ignored `work/runtime/`. Existing host instructions/settings can still affect behavior. No model is forced.

```sh
python3 tests/run_runtime_smoke.py --runtime codex --scenario explicit
python3 tests/run_runtime_smoke.py --runtime claude --scenario explicit
```

Also run `implicit-de`, `implicit-en`, and `unrelated` to inspect automatic selection and a negative control. Use `--executable /path/to/cli` if the CLI is not on PATH. Codex uses read-only file access; Claude is limited to Read and Skill tools with other requests denied. The runner leaves host authentication and configuration unchanged.

`explicit` batches eleven separate passages. An exit code of zero only means the host process completed: inspect the response, skill-read evidence, and semantic constraints. The unrelated control should answer `391` without loading Individualizer. Do not publish raw logs; they may contain machine paths and account or host context.

`behavioral-cases.json` holds earlier author-reviewed examples, including an initially flawed candidate and its correction. The runner supplies only id, language, request, and input. Output and review fields never enter the test prompt.

The [validation record](../research/VALIDATION.md) and [sanitized runtime results](../research/runtime-smoke-2026-11-02.json) distinguish observed behavior from untested claims. Future quality studies should use blinded native-reader comparisons and a baseline, with semantic failures assessed before style preference.

## Live learning checks

`run_learning_smoke.py` uses a synthetic approved profile in a temporary workspace. Four fresh sessions per host learn from two user revisions, reuse the saved profile, apply a one-off correction without changing it, and forget the learned preference. Only the profile carries state between phases; previous conversations and expected answers are not supplied.

```sh
python3 tests/run_learning_smoke.py --runtime codex
python3 tests/run_learning_smoke.py --runtime claude
```

These checks require an authenticated host and consume model quota. The fixture is writable: Codex runs with workspace-write access; Claude can use Read, Skill, Write, and Edit. Prompts limit writes to the two test profile files. Raw logs and before/after snapshots remain in ignored `work/learning/`; they are test evidence, not actual user memory. Schema checks and preservation indicators are automated; inspect text quality, scope, evidence, and Markdown/JSON agreement separately.

Use `--phase one-off` for a targeted repeat from the synthetic baseline. A single `recall` run from that baseline does not test prior learning. The full four-phase sequence is required to check cross-session reuse.
