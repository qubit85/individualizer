# Learning from revisions

Use when a user refines a draft, supplies a revised version, corrects recurring style, or asks to remember, change, or forget a preference. The result is a better next draft and, when authorized, a reusable private preference. This is profile-based adaptation, not model training.

## Apply feedback now

Compare the previous draft with the user's correction or revised passage. Separate style changes (openings, rhythm, word choice, address, formatting, humour) from factual corrections, new requirements, and changes of audience. Apply all requested corrections to the current artifact; factual corrections are not automatically style rules.

Keep a compact working view of the user's latest relevant feedback during the conversation. Before returning each revision, check both the original constraints and the corrections already made. Do not reintroduce a rejected opener while fixing the ending. If the user only corrects one span, preserve unrelated successful choices. If earlier versions are unavailable, use the visible feedback without inventing a comparison.

Distinguish evidence:

- An explicit preference such as “For future English updates, start with the result” can establish a rule immediately in that context.
- A user-authored revision suggests the narrowest observable choice. One shortened email does not establish “always use short sentences.”
- Consistent corrections across distinct relevant texts can support a reusable inference. Several rounds on one draft are one context, not independent confirmations. Keep genuine evidence pointers; do not invent counts or confidence percentages.
- “Looks good,” silence, acceptance of a whole artifact, and the model's own rewrites do not approve every inferred trait. Generated alternatives remain proposals until the user selects them.

## Choose persistence once, then respect it

Use the selected profile's `learning.mode`. If absent, use `review`. All modes adapt the current conversation immediately and can use existing active rules.

| Mode | Behavior for new preferences |
| --- | --- |
| `session` | Keep new observations in this conversation; do not write them merely because they recur. |
| `review` | Propose a compact profile change when evidence is useful. Activate and save it when the user approves it. Do not interrupt every edit to ask about learning. |
| `automatic` | With recorded standing user authorization, save explicit durable preferences and well-supported recurring inferences within the authorized scope. Do not ask again for each covered change. |

An instruction such as “Remember this for future support emails” already authorizes that scoped update; no second confirmation is needed. “Learn automatically from my corrections in this profile” can enable automatic mode for that selected profile. A general request to edit a text, use this skill, or improve the skill's learning capability does not enable automatic learning in every personal profile.

Before the first persistent write, resolve which private profile and storage location the user intends. Reuse a known selected location and existing permission. Without a destination or write capability, continue adapting in the conversation and explain the persistence limit; do not claim to remember across chats. Do not save candidates, full drafts, or backups to an arbitrary public checkout. In review mode, leave unapproved candidates in the conversation unless saving a private draft was itself authorized.

Automatic mode does not turn weak signals into rules. Keep ambiguous one-off observations provisional. A rule needs either a clear durable user preference or consistent evidence from distinct relevant user edits. Limit its scope to supported languages, medium, audience, and purpose. Use `*` for a dimension only when the user authorized that breadth; a German wording preference is not automatically an English ban. Never treat punctuation or phrase preferences as permission to alter protected quotations or code.

## Save a small, inspectable update

Use the optional `learning` block in [Profile contract](profile-schema.md). Each rule has a stable ID, actionable instruction, language/context scope, status, approval provenance, and concise user-derived evidence. Keep general voice, language settings, and learned rules coherent; prefer one canonical rule over duplicates. A new learned exception may override a broad baseline only within its recorded scope. Explain that exception in STYLE.md rather than silently flattening the baseline.

Store only the preference and a brief evidence summary or private pointer. Do not archive entire source texts, infer personal facts, or copy confidential sentences into the profile. A standing authorization approves the learning process; it does not mean the user explicitly approved each inferred rule. Record `approval: standing` for those changes, and `explicit` only for a directly approved rule. Generated demonstrations still need their own sample approval.

Preserve unrelated fields, visual settings, and extensions. Increment the profile version once per accepted update, record the actual change and known date, and synchronize profile.json with STYLE.md. When upgrading a 1.0/1.1 profile for an authorized learning update, preserve existing data and add only the required 1.2 fields. Before replacing files, recheck that the source has not changed since reading it. Parse and validate the resulting JSON where a validator is available, reread both files, and verify the intended change and preserved fields. Do not report persistence if one write failed or the pair disagrees.

## Apply, revise, and forget

At the start of a new text, load the selected profile and apply only active rules whose language and context match. Candidates, rejected rules, and superseded rules do not govern output. The current explicit brief wins over older preferences; a one-off exception leaves the persistent rule intact. Do not require setup again when the profile is already selected.

Transfer the style, not the example's facts. Keep the source material for separate artifacts separate. Removing a rhetorical opening does not justify inventing a replacement claim about the author's plans; making a support message warmer does not justify adding undocumented operating instructions. Use only the new text's supported content and requested intent, then check factual fidelity again.

If the user explicitly replaces a lasting preference, supersede the old rule in the overlapping scope instead of keeping contradictory active instructions. If the intended scope is unclear, apply the correction locally and clarify only before making a consequential persistent change. Merge duplicate evidence without counting the same correction twice.

The user can inspect what was learned, disable automatic updates, reject a candidate, change a rule, or ask to forget it. Disabling automatic updates stops new automatic writes; it does not erase already approved style. When asked to forget, remove the relevant learned rule and its stored evidence from both profile files; do not preserve the deleted content in a new history note or backup. Do not promise erasure from pre-existing external backups or platform chat history. Do not revive a rejected preference from the same old evidence.

Deliver the revised artifact in the requested format. Where commentary is allowed, briefly mention a meaningful saved preference; avoid learning reports after every small edit. “Only the text” still means only the text. If persistence failed, do not imply success; report the limitation through an allowed status channel or at the next appropriate opportunity.

## Examples of scope

- “Für diese Mail bitte kürzer” changes this email and subsequent revisions of it.
- “Bei meinen deutschen LinkedIn-Posts bitte künftig ohne rhetorische Einstiegsfrage” establishes that scoped opening preference. It does not ban questions in interviews or English posts.
- “Use contractions in my future English product updates” can be saved once authorized; a legal notice may still require a different register.
- “The deadline is Friday, not Thursday” corrects a fact; it does not establish a preference for Friday deadlines.
- Two independently user-edited updates that replace vague openings with a concrete result support a candidate. Approved automatic mode can store the inference in the matching context; review mode waits for approval before activation.
