# Research and integration decisions

Reviewed 2026-11-02. English and German are the detailed focus languages; other languages use contextual adaptation. Source skills are practical design references, not scientific evidence of effectiveness. No external skill needs to be installed for Individualizer's workflow.

## Evidence informing the design

- [Kobak et al., excess vocabulary in biomedical abstracts](https://arxiv.org/abs/2406.07016): population-level vocabulary changes support examining habitual wording. These results do not establish the author of an individual passage or justify universal word bans.
- [Shaitarova et al., English and German linguistic footprints](https://aclanthology.org/2024.swisstext-1.9.pdf): the tested domains and models showed different patterns across languages, including greater English prompt sensitivity. This motivates separate language guidance; it does not validate the present skill or a current-model detector.
- [Liang et al., detector bias](https://arxiv.org/abs/2304.02819): the studied detectors misclassified non-native English writing. Individualizer therefore evaluates clarity, meaning, and voice rather than a detector score.
- [Bundesverwaltungsamt, Bürgernahe Verwaltungssprache, 2002, pp. 19–24 and 40–42](https://moderne-verwaltungssprache.de/fileadmin/redaktion/Leitf_den/HandbuchB_rgernaheVerwaltungsspracheBVA.pdf): practical clarity guidance, including verbal expression and understandable sentence organization, with context-sensitive exceptions. It predates LLMs and is not evidence of German AI markers.
- [GCA English style guide](https://www.gca.gov.uk/government-commercial-agency-style-guide/language): audience-aware language and clearer expression. Its house conventions are not imposed on every author.
- [Anthropic skill-authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): conditional reference loading and concrete evaluation cases inform the package architecture.

## Skills evaluated

| Source | Adopted or complementary idea | Boundary |
| --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) | Structural review, voice matching, final fidelity comparison | No global dash/word ban, no mandatory display of intermediate drafts |
| [Copy Editing](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md) | Respect point edits; review clarity, voice, evidence, and specificity separately | Emotion amplification and conversion pressure are conditional on the task |
| [Copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) | Use audience, purpose, and supported claims for marketing requests | No invented proof, guarantees, urgency, or mandatory CTA |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh/blob/main/SKILL.md) | A concrete example of adapting checks to a language and preserving valid uses | Its Chinese phrase list is not translated into a supposed universal blacklist |
| [Anthropic Canvas Design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md) | Art direction followed by realization and inspection | No forced manifesto, poster style, minimal-text ratio, or assumed fonts |
| [Anthropic Brand Guidelines](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md) | Concrete color/type roles and font fallbacks illustrate useful token design | Its Anthropic identity is not a default user identity |
| [borghei Brand Guidelines](https://github.com/borghei/Claude-Skills/blob/main/marketing/brand-guidelines/SKILL.md) | Evaluated coverage of brand systems and audits | Not incorporated because the inspected license adds Commons Clause restrictions |

MIT notices for adapted editorial procedures are included. Anthropic's inspected Apache-2.0 license is also retained. No entire third-party skill bundle was copied into the runtime instructions.

## Implementation choices and limits

The four editorial passes, edit depths, DE/EN cue tables, multilingual procedure, approval model, and profile extensions are Individualizer's synthesis. The German cue table is an editorial heuristic, not an empirical frequency list.

A brief or approved sample can override generic style preferences. New facts, invented autobiography, omitted uncertainty, and changes to protected content are not acceptable methods of making prose seem human.

Reusable identity is now connected to locale-specific choices and medium-specific production. Document/image renderers remain host capabilities. A role token does not itself ensure correct rendering.

Structural/profile checks, author-reviewed examples, and small live Codex and Claude Code smoke tests support this revision. Automatic selection was observed on English and German requests in both hosts. These are agent-reviewed checks, not blinded reader comparisons or proof of broad language quality. See the [repository validation record](https://github.com/qubit85/individualizer/blob/main/research/VALIDATION.md) for methods, an output-format correction, and remaining limits.
