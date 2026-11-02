# Individualizer 1.2.0

One shared package targets Codex and Claude Code. English and German have dedicated editorial guides; other languages use locale-aware adaptation. Profile schema 1.1 remains compatible with 1.0 profiles.

## Layout

- `skill/individualizer/`: distributable runtime instructions, references, templates, schema, and licenses.
- `tests/`: structural/profile checks, source examples, and an opt-in live runtime runner.
- `research/`: source identities, validation methods, and sanitized synthetic outputs.
- `dist/individualizer-1.2.0.zip`: the skill folder only, suitable for extraction or supported import flows.
- `work/`, `source/`, `profiles/`, and `IMPORT-STATUS.md`: private/local material, excluded from version control.

## Validation and packaging

Run `python3 -m unittest discover -s tests -v`. See `tests/README.md` for live checks; they need authenticated host tools and consume the host's model quota. Small smoke tests are not human validation.

When packaging, include only `skill/individualizer/`, with `individualizer/SKILL.md` at the ZIP root's first directory level. Retain all notices and licenses. Do not include private profiles, source chat exports, raw runtime logs, credentials, or machine-specific paths.

The public repository may include tests, sanitized results, and development documentation, while the installable package stays limited to runtime files. Review the exact staged files before publishing. Publication and global installation need user authorization for that task.
