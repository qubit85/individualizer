# Validation record — current version 1.3.0

The structural Skill Creator check passes. All **25 automated profile/reference tests pass**, including schema 1.0/1.1 compatibility, learning authorization, rule approval/evidence, scope, and retained extensions. These tests do not assess prose quality.

[Learning validation](LEARNING-VALIDATION.md) documents live Codex and Claude Code checks for saving scoped preferences, reusing them in fresh sessions, keeping a one-off edit local, and forgetting a learned rule. The learning/profile behavior worked in the selected cases. **A Claude wording-fidelity failure remains open:** a warmer German email added an unspecified recipient, despite preserving the profile correctly. Do not describe this suite as an unconditional pass.

- [Sanitized learning results](learning-smoke-2026-11-02.json)
- [Earlier 1.2.0 validation record](VALIDATION-1.2.0.md)
- [Earlier 1.2.0 text outputs](runtime-smoke-2026-11-02.json)
- [Test instructions](../tests/README.md)

These are agent-reviewed smoke checks, not independent reader studies or guarantees across models and requests. Native-reader comparisons, broader language coverage, profile conflict/failure scenarios, and rendered cross-media tests remain future work.
