# Learning validation — 2026-11-02

## Method

The live runner copies the skill and a synthetic approved profile into a temporary workspace. Four fresh CLI sessions per host receive source requests only. No previous session or expected answer is supplied; the two profile files carry the learned state. Codex uses workspace-write access; Claude can use Read, Skill, Write, and Edit. Only the test profile is authorized for modification. Both hosts use configured default models.

The user feedback consists of two independently revised German LinkedIn posts whose rhetorical openings were removed. The existing profile also has an unrelated English support-email greeting, a color, and an extension field. Checks examine the saved rule, its scope and standing authorization, later use, preservation of unrelated content, and deletion on request.

## Observed behavior

| Scenario | Codex | Claude Code |
| --- | --- | --- |
| Learn from two user revisions under standing approval | Saves scoped active rule with evidence | Saves scoped active rule with evidence |
| Fresh session: German LinkedIn text | Uses the direct opening; preserves supplied facts in rerun | Uses the direct opening; preserves supplied facts in rerun |
| Fresh session: separate English support text and German interview | Keeps the English greeting and interview question | Keeps the English greeting and interview question |
| One-off warmth and factual correction | Profile pair byte-identical | Profile pair byte-identical |
| One-off text fidelity after targeted changes | Final targeted sample passes | Still adds unsupported “mir”; needs revision |
| Forget the learned rule | Removes it and its evidence; keeps unrelated rule/settings | Removes it and its evidence; keeps unrelated rule/settings |
| Verify persistent updates | Both profile files reread in full rerun | Both profile files reread in full rerun |

All saved snapshots were valid against the profile schema. Their relevant JSON/Markdown rules were inspected for agreement. No additional file appeared in the synthetic private directory during the full rerun. A successful save does not prove correct text behavior: the one-off case deliberately records profile and prose outcomes separately.

## Development findings and changes

The initial recall run showed factual mixing and, in Claude, unsupported advice to keep a page open. The skill now explicitly transfers style without carrying facts between artifacts; the scenario also states that its three sources are independent. The full rerun preserved their factual boundaries.

Claude initially acknowledged that it had not reread both saved files. A concise entrypoint checkpoint led to observed rereads in the full rerun. The test harness additionally validated every saved JSON snapshot.

Both hosts added an unsupported recipient while warming a German request in the full sequence. The role-preservation instruction was clarified. A targeted Codex sample then retained the original unspecified recipient. Claude still inserted “mir” in two targeted follow-ups, including one after a German-specific clarification. This remains a known fidelity limitation; it is not counted as a successful editing outcome.

## Evidence and limits

[Sanitized results](learning-smoke-2026-11-02.json) include selected actual outputs, learned rules, profile checks, CLI versions, and hashes identifying the tested instruction variants. In total, 19 live phase executions were run during development. The full sequence precedes the last recipient-role edits; those edits received targeted one-off tests rather than another full run.

This is a small, non-randomized, agent-reviewed test, not a blind human study. Review/session-mode decisions, conflicting durable preferences, failed/concurrent writes, broader languages, and visual output were not live-tested. “Learning” means updating an accessible private profile and loading it in later sessions; it does not retrain a model or promise memory without profile access.
