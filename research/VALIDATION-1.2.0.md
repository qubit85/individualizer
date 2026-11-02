# Validation record — 2026-11-02

## Structural and profile checks

The Skill Creator structural validator passes. All 15 automated profile/reference tests pass. They cover the original v1.0 profile, the v1.1 template, approval consistency, language extensions, malformed inputs, and runtime Markdown links. These checks do not assess prose quality.

## Live Codex and Claude Code smoke tests

Fresh CLI sessions received only the source inputs and requests, without stored answers or reviews. Each session used a temporary copy of the skill. The host selected its configured default model; no model override was supplied. Raw local logs are excluded from the repository. [Sanitized results](runtime-smoke-2026-11-02.json) retain synthetic outputs, tool-read evidence, CLI versions, and skill-entrypoint hashes.

| Check | Codex | Claude Code |
| --- | --- | --- |
| Explicit invocation, 11 passages | 11 reviewed outputs satisfy the stated text constraints | 11 reviewed outputs satisfy the stated text constraints |
| Automatic selection, German request | Skill and relevant guides read | Skill invoked and relevant guides read |
| Automatic selection, English request | Skill and relevant guides read | Skill invoked and relevant guides read |
| Unrelated arithmetic request | Correct answer; no skill reads | Correct answer; no skill invocation or reads |
| Final batch delivery as JSON | Valid JSON, no appended notes | Valid JSON after format clarification |

The passages cover factual uncertainty, dates and formal address, meaningful technical wording, a true three-item list, narrow edit scope, Spanish fallback, mixed language, protected quotation/command/URL, and avoiding invented autobiography. All 22 final batch outputs were reviewed by the developing agent against those constraints. This is a cross-runtime smoke check, not an independent human quality score.

The first Claude batch added code fences and change notes to the requested JSON. The skill now explicitly respects requested delivery formats. Both hosts were rerun on the batch after this change. The automatic-selection checks preceded that clarification; their description and routing were unchanged. In the final Claude explicit run, no reference-read calls were emitted, although the initial explicit run and both automatic-selection runs did read the guides. Consistent reference loading remains unproven.

Tested CLIs: Codex `0.166.0-alpha.5.1`; Claude Code `2.1.289`. Claude reported `claude-sonnet-5-5`; the Codex event stream did not report the resolved model. Host versions, defaults, and global instructions can affect results. Local connector-startup warnings appeared in Codex logs but did not prevent these text-only runs.

## Earlier author review

`tests/behavioral-cases.json` retains eleven examples created and reviewed by the authoring agent before the runtime checks. One initial candidate added “mir” to a German request and changed the implied recipient. Its corrected candidate preserves the original ambiguity. The fresh runtime prompts excluded both candidates and the review.

## Limits

- No blinded native-reader study, no unskilled baseline, and no statistical generalization.
- Spanish is a single smoke example without native-reader validation.
- No rendered images, slide decks, or documents were produced in this check.
- Profile creation and unrestricted write restraint were not tested; the hosts ran with restricted tools or read-only file access.
- No claim of detector evasion, guaranteed naturalness, or consistent activation on every paraphrase.
