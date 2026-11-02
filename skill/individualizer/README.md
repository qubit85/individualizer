# Individualizer 1.3.0

Develop a personal or brand voice, edit formulaic prose, and apply an approved identity across text and visuals. English and German have dedicated guides; other languages use locale-aware adaptation.

## Installation and use

Copy this entire folder, including references and assets:

| Host | Project location | Personal location | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/individualizer/` | `~/.agents/skills/individualizer/` | `$individualizer` |
| Claude Code | `.claude/skills/individualizer/` | `~/.claude/skills/individualizer/` | `/individualizer` |

Ask to refine a passage, discover a style, or apply a profile. Automatic selection depends on the host and request. If the skill does not appear after installation, restart the host. These locations apply to local sessions; hosted services have separate import controls.

The instructions require no runtime scripts or extra skill installation. You need access to the host model, and artifact creation uses its available tools. Follow the host's permissions and output format.

See the [project repository](https://github.com/qubit85/individualizer) for setup, tests, source research, and validation limits. Installation details follow the [Codex](https://learn.chatgpt.com/docs/build-skills) and [Claude Code](https://code.claude.com/docs/en/skills) documentation.

## Profiles and boundaries

Keep private profiles outside this package and any public repository. [Profile schema 1.2](references/profile-schema.md) accepts existing 1.0 and 1.1 profiles. The templates are unapproved scaffolds, not a default personality or palette.

Meaning, qualifications, protected content, and the author's voice take priority over style. Phrase lists are review cues, not global bans. The skill does not detect authorship, guarantee native quality, or promise detector evasion. Visual output still requires rendering and inspection with appropriate host tools.

## Learning from feedback

The next revision incorporates the user's corrections and keeps earlier feedback intact. For lasting preferences, [Learning from revisions](references/learning-from-revisions.md) separates session-only adaptation, review before saving, and explicitly authorized automatic updates. Rules retain their language/context scope and evidence; a factual correction or one-off tone change is not a global style preference.

Saved learning lives in the selected private profile, not in the shared skill or model weights. Users can inspect, revise, disable, or forget it. Cross-chat reuse requires an accessible profile; no automatic mode is enabled merely by installing the skill.

## Contents and license

`SKILL.md` routes to task-specific references. `assets/` contains profile templates and a JSON Schema. `agents/openai.yaml` supplies Codex UI metadata. `LICENSE`, `THIRD_PARTY_NOTICES.md`, and `licenses/` retain attribution. Research rationale is in [Research and integration notes](references/research-and-sources.md).

Individualizer contributions use MIT. Small runtime smoke tests and structural checks do not replace blinded reader comparisons or cross-media production tests.
