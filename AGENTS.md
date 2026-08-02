# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Copilot, Warp, etc.) working in
this repository.

## What this repo is

A portable agent skill implemented entirely as Markdown. The runtime artifact is
`SKILL.md`: the agent reads its YAML frontmatter and the instruction body. There is no
build step, and install and usage language stays harness-neutral.

Corpify rewrites rude, blunt, angry, or emotional messages into professional,
human-sounding corporate communication. It is the mirror of
[blader/humanizer](https://github.com/blader/humanizer): humanizer removes AI tells to
sound human; corpify professionalizes human venting, then applies humanizer's anti-slop
rules so the corporate result stays human.

## Key files

- `SKILL.md` — the skill itself, at the repo root. Portable YAML frontmatter (`name`,
  `description`, `argument-hint`, `license`, `metadata.version`) followed by the tone
  guide, corpify pattern catalog with before/after examples, the anti-slop pass, and the
  process loop. **This is the source of truth.**
- `.github/skills/corpify/SKILL.md` — a byte-identical copy so VS Code Copilot discovers
  the skill. It must stay in sync with the root `SKILL.md`.
- `README.md` — for humans: installation, usage, tone table, and version history.
- `.claude-plugin/plugin.json` — optional Claude Code plugin manifest.
- `.claude-plugin/marketplace.json` — optional single-repo marketplace entry so
  `/plugin marketplace add mahanteshimath/corpify` works.
- `scripts/validate-package.py` — dependency-free sync and version checks.

## The maintenance contract

`SKILL.md`, its `.github/skills/corpify/` copy, and `README.md` must stay in sync. When
you change behavior or content:

- **Skill copies:** the root `SKILL.md` and `.github/skills/corpify/SKILL.md` must be
  identical. If you edit one, copy it to the other in the same change.
- **Patterns:** the skill defines 11 corpify patterns and an anti-slop pass. If you add,
  remove, or renumber patterns, update the README summary in the same change.
- **Version:** `SKILL.md` frontmatter stores the version under `metadata.version`,
  `README.md` has a "Version History" section, and `.claude-plugin/plugin.json` has a
  `version` field. Bump them together so package metadata matches the skill. Keep the
  skill version under `metadata`; a top-level `version` key is not portable across Agent
  Skills hosts. (`marketplace.json` intentionally omits a version so `plugin.json` stays
  the package source of truth.)
- **Behavior guardrails:** preserve the message and any boundary, never fabricate facts
  or commitments, and keep the anti-slop rules (no em dashes, no "I hope this email finds
  you well," no sycophancy). These are the product; do not weaken them casually.
- **Compatibility:** keep install and usage language harness-neutral. The skill should
  work in any harness that can load Markdown skill instructions.
- **Validation:** run `python3 scripts/validate-package.py` before publishing.

## Editing SKILL.md

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product. Edit it like a careful instruction
  document, not code.
- After editing the root `SKILL.md`, copy it to `.github/skills/corpify/SKILL.md`.

## Attribution

Anti-slop pattern rules are adapted from
[blader/humanizer](https://github.com/blader/humanizer) (MIT).
