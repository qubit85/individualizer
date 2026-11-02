# Individualizer development

Individualizer supports Codex and Claude Code through one shared skill package.

- Edit `skill/individualizer/`; keep the core short and load references by task.
- Read `DEVELOPMENT.md` and `research/VALIDATION.md` for the current revision and evidence.
- English and German are focus languages, not an exclusive restriction.
- Preserve facts, qualifications, author voice, and protected spans. Do not add universal phrase bans or detector-score promises.
- Keep private profiles, local chat provenance, authentication data, and raw runtime logs out of commits and packages. Preserve any local `source/` directory without publishing it.
- Keep attribution in `THIRD_PARTY_NOTICES.md` and `licenses/` when adapting external material.
- Run `python3 -m unittest discover -s tests -v`. Runtime smoke tests are opt-in, require signed-in host tools, and can consume model usage.
- Do not present agent-reviewed examples or small runtime tests as blind human evaluation.
- Publish, install globally, or call paid services only within the user's authorized task scope.
