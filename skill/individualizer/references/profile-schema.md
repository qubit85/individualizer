# Portable profile contract, schema 1.1

Store synchronized STYLE.md and profile.json in a user-selected private location outside the distributed skill by default. JSON is the structured record; Markdown explains the same choices. Do not silently choose a public repository as storage.

Use assets/profile-template.json and assets/profile-template.md as scaffolds. Neither is an approved style. The JSON Schema in assets/profile.schema.json accepts both schema versions 1.0 and 1.1. Any JSON Schema draft 2020-12 validator can check it; a validator is optional at runtime. Without one, parse the JSON and check the following invariants explicitly.

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

## Existing v1.0 profiles

Read them as they stand. Do not require new fields, reset their version, or infer locale settings. On a requested profile update, preserve the original, add only supported settings, change schema_version to 1.1 if the new extensions are adopted, and increment the profile version appropriately. Log the actual changed fields and date only when known. Keep STYLE.md synchronized.

The legacy voice.avoid_phrases is a preference field; do not silently promote every entry to a strict ban. Resolve material conflicts with current user intent.

## Approval and changes

A request to revise an artifact does not authorize changing the persistent identity. If a previously approved profile is being explored without final approval, retain the approved version and save a separate draft candidate. When approval arrives, commit the approved update and changelog together.

Compare JSON and Markdown after writing, including examples, vocabulary exceptions, and language settings. Schema validation alone cannot detect a contradiction between those two files.
