# Individualizer

**Make every output unmistakably yours.**

Individualizer is a shared skill for **Codex and Claude Code**. It helps you develop a personal or brand voice, edit formulaic prose, and carry an approved identity across text, visuals, slides, and documents.

English and German have dedicated editing guides. Other languages use a locale-aware workflow. You can improve one paragraph without setting up a style profile.

## Try it

In Codex:

```text
$individualizer Überarbeite diesen Text. Behalte Sie-Anrede, Zahlen und Unsicherheiten bei:
Es ist wichtig zu betonen, dass der Pilot die Bearbeitungszeit möglicherweise um 12 % senkt.
```

In Claude Code:

```text
/individualizer Lightly edit this paragraph. Keep my dry humour and technical terms.
```

You can also ask naturally: “Make this German text less formulaic without changing its meaning.” The host decides when to load a skill; use the explicit invocation when you want to be certain.

## Install

Clone this repository, then copy the **entire** `skill/individualizer` directory into one of these locations:

| Scope | Codex | Claude Code |
| --- | --- | --- |
| Current project | `.agents/skills/individualizer/` | `.claude/skills/individualizer/` |
| All local projects | `~/.agents/skills/individualizer/` | `~/.claude/skills/individualizer/` |

For example, to install in Codex on macOS or Linux:

```sh
git clone https://github.com/qubit85/individualizer.git
cd individualizer
mkdir -p "$HOME/.agents/skills"
if [ ! -e "$HOME/.agents/skills/individualizer" ] && [ ! -L "$HOME/.agents/skills/individualizer" ]; then
  cp -R skill/individualizer "$HOME/.agents/skills/individualizer"
else
  echo 'Individualizer already exists; inspect it before updating.'
fi
```

For Claude Code, replace `.agents/skills` with `.claude/skills`. On Windows, copy the directory into the corresponding location under your user profile. Restart the host if the skill does not appear. These are local installations; they do not install a skill into a hosted chat service.

Maintainers can use a directory symlink in Codex to keep the installation linked to a checkout. Keep only one intended version per host and remove the installation directory or link to uninstall.

Install paths and invocation follow the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills).

## What the skill does

- Edits in light, standard, or deep passes while preserving factual meaning.
- Treats common AI wording as contextual review cues, not a blacklist.
- Builds a voice from examples and user choices, without inventing personal experience.
- Separates persistent identity from the tone of a particular artifact.
- Defines visual roles and checks consistency across formats.
- Keeps private profiles outside the distributed package.

The workflow does not promise detector evasion or universal native-speaker quality. Meaning, uncertainty, quotations, code, and attribution take precedence over stylistic changes. Actual image and document creation depends on the host's tools; a style specification alone is not a rendered artifact.

## Package and development

The current skill version is **1.2.0**. The profile schema remains **1.1**, with support for existing 1.0 profiles. The skill itself needs no Python dependency, external skill bundle, or additional API key; you still need access to your chosen host.

- [Skill entrypoint](skill/individualizer/SKILL.md)
- [Packaged skill ZIP](dist/individualizer-1.2.0.zip)
- [Editing and language guides](skill/individualizer/references/text-editing.md)
- [Profile contract](skill/individualizer/references/profile-schema.md)
- [Research and source decisions](skill/individualizer/references/research-and-sources.md)
- [Validation record](research/VALIDATION.md) and [test instructions](tests/README.md)
- [Changelog](CHANGELOG.md)

Run structural/profile checks with:

```sh
python3 -m pip install -r tests/requirements.txt
python3 -m unittest discover -s tests -v
```

Small runtime smoke tests are documented separately from author-reviewed examples. Blinded reader comparisons and rendered cross-media validation remain future work.

## License

Individualizer is MIT licensed. See [LICENSE](LICENSE) and [third-party notices](skill/individualizer/THIRD_PARTY_NOTICES.md) for retained source licenses. References do not imply endorsement.
