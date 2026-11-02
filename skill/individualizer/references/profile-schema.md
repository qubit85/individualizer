# Portable profile contract, schema 1.2

Store synchronized STYLE.md and profile.json in a user-selected private location outside the distributed skill by default. JSON is the structured record; Markdown explains the same choices. Do not silently choose a public repository as storage.

Use assets/profile-template.json and assets/profile-template.md as scaffolds. Neither is an approved style. The JSON Schema in assets/profile.schema.json accepts schema versions 1.0, 1.1, and 1.2. Any JSON Schema draft 2020-12 validator can check it; a validator is optional at runtime. Without one, parse the JSON and check the following invariants explicitly.

## Core invariants

- Preserve the v1.0 core fields: schema_version, id, name, version, status, language, audience, personality, voice, visual, media, accessibility, approved_by_user, and changelog.
- ID: lowercase letters/numbers separated by hyphens. Profile version: MAJOR.MINOR.PATCH, independently of the skill version.
- Status is draft or approved. approved_by_user is true exactly when status is approved; set approval only after the user's approval.
- Use a six-digit HEX value when adding a palette color. Leave an unchosen palette empty. Unknown font/motif values may be null or unspecified.
- Preserve additional fields, including extensions that this skill does not interpret.
- Do not insert sensitive personal facts into a profile merely because they appear in samples.
- A structurally valid file does not prove the choices were approved or the style is effective.

## Optional 1.1 extensions

| Field | Meaning |
| --- | --- |
| voice.contextual_tone | Context name mapped to a tone description, without changing core voice |
| language_settings | Language/locale keys, such as en-GB or de-CH, with address, formality, spelling, punctuation, inclusive language, and terminology |
| editorial.edit_depth | light, standard, or deep; the current request may override it |
| editorial.review_phrases | Contextual review cues, not forbidden words |
| editorial.prohibited_phrases | Explicit user prohibitions for newly written prose; quoted/protected text remains protected |
| editorial.protected_terms | Exact names or technical vocabulary that should not be paraphrased |
| editorial.phrase_exceptions | Approved exceptions and their context |
| samples | Evidence records with ID, language, context, kind (own/reference/generated), and approval state; text or a private source pointer is optional |
| visual.tokens | Additional role-based design values, with their meaning explained in STYLE.md |

Select settings by exact locale, then language, then relevant existing profile rules. If none match, use the current brief and language guide provisionally. Do not manufacture a locale preference. Shared identity does not require shared idioms.

A generated sample remains unapproved until the user chooses it. An approved third-party reference is an approved inspiration, not proof of the user's personal experience.

## Optional 1.2 learning extension

Follow [Learning from revisions](learning-from-revisions.md) for decisions about evidence, authorization, scope, and persistence. The `learning` block contains:

| Field | Meaning |
| --- | --- |
| mode | `session`, `review`, or `automatic`; absent block means `review` |
| automatic_updates_approved | True only after the user authorized automatic learning for this profile; required true in automatic mode |
| rules | Scoped preference records; an empty list learns no default personality |

Each rule requires `id`, `instruction`, `scope`, `status`, `approval`, and `evidence`. Scope has nonempty `languages` and `contexts` lists. Use language/locale values such as `de` or `en-GB` and understandable contexts such as `LinkedIn posts for peers`; `*` means an explicitly authorized shared scope, not unknown. Status is `candidate`, `active`, `rejected`, or `superseded`. Approval is `none`, `explicit`, or `standing`; an active rule requires the latter two and a nonempty `approval_source` describing the actual authorization.

Evidence entries contain a `kind` of `explicit_preference` or `user_revision`, a concise `summary`, and optionally a private `source_ref`. Generated examples are not learning evidence by themselves. Optional `supersedes` references earlier rule IDs. Keep rule IDs unique, resolve such references, and avoid contradictory active rules in the same scope; these semantic checks go beyond JSON Schema.

The profile's `approved_by_user` describes the baseline identity's approval. A learned rule's provenance separately records whether the user approved that rule directly or authorized the automatic process. Changing the learning mode does not retroactively relabel standing approvals as explicit approvals. Pending rules never become effective merely because the enclosing profile is approved.

On load, apply active rules in the matching language and context, alongside the relevant baseline. On save, synchronize rule IDs, scope, status, and authorization in STYLE.md and profile.json. A schema validator cannot verify whether evidence is real or a rule is appropriate.

## Existing v1.0 and v1.1 profiles

Read them as they stand. Do not require new fields, reset their version, or infer locale settings. On an authorized learning update, preserve existing content and extensions, adopt schema_version 1.2 when adding the learning block, and increment the profile version appropriately. Do not create an unrequested backup of private material. Log the actual changed fields and date only when known. Keep STYLE.md synchronized.

The legacy voice.avoid_phrases is a preference field; do not silently promote every entry to a strict ban. Resolve material conflicts with current user intent.

## Approval and changes

A request to revise an artifact adapts that artifact immediately. Persistent changes require an explicit instruction or a previously approved automatic-learning mode covering that update; do not request permission again when it is already present. Without that authorization, keep proposals in the conversation, or in a separate private draft only if saving a draft was authorized. When approval arrives, save the accepted update and changelog together.

Compare JSON and Markdown after writing, including examples, vocabulary exceptions, and language settings. Schema validation alone cannot detect a contradiction between those two files.
