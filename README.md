# Corpify

> Turn raw, heated, or code-switched venting into calm, professional, human-sounding
> corporate communication, without losing your point.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Type: Agent Skill](https://img.shields.io/badge/type-agent%20skill-8A2BE2.svg)
![Harness: agnostic](https://img.shields.io/badge/harness-agnostic-informational.svg)

A portable agent skill that rewrites rude, blunt, angry, emotional, or too-casual
messages into professional, human-sounding corporate communication (email or plain
text). It preserves the underlying message and any boundary you set, then runs an
anti-AI-slop pass so the result stays warm and human, not sterile corporate filler.

Corpify is the mirror of [blader/humanizer](https://github.com/blader/humanizer):
humanizer removes AI tells to make writing sound human; corpify professionalizes human
venting, then borrows humanizer's anti-slop rules so the corporate output does not read
like a template ("I hope this email finds you well...").

The runtime artifact is `SKILL.md`, plain Markdown, so it runs in any harness that
supports skill-style instructions.

## Features

- **Rude to professional in one step** — hostility, blame, sarcasm, demands, and
  venting become calm and courteous.
- **Keeps your meaning and boundaries** — a "no" stays a "no"; it just gets polite.
- **Three tones** — Diplomatic, Warm-professional (default), and Firm-but-polite.
- **Email or plain text** — quick rewrite by default, or a full email on request.
- **Mixed-language aware** — understands code-switched input (e.g. Hinglish), maps
  idioms to intent, and returns professional English (or another language on request).
- **Anti-slop pass** — cuts em dashes, sycophancy, buzzwords, and "I hope this email
  finds you well" filler so the output still sounds human.
- **No fabrication** — never invents dates, names, or commitments.
- **Portable and dependency-free** — one Markdown file, works in any skill-aware harness.

## Installation

Corpify is plain Markdown (`SKILL.md`), so it works in any harness that loads
skill-style instructions. Pick whichever fits your setup.

### Skills CLI (any agent, global)

```sh
npx skills add mahanteshimath/corpify --global
```

Update later with `npx skills update corpify --global`. Omit `--global` for a
project-local install you can commit and share with collaborators.

### Claude Code plugin

```text
/plugin marketplace add mahanteshimath/corpify
/plugin install corpify@corpify
```

The skill is then invoked as `/corpify:corpify`.

### VS Code Copilot

This repo already ships the discovery copy at `.github/skills/corpify/SKILL.md`. Clone
it (or copy that folder) into your project, reload skills or start a new Copilot session,
then type `/corpify` in chat.

### Manual (any harness)

```sh
git clone git@github.com:mahanteshimath/corpify.git
# or copy just the runtime artifact into your skills folder:
mkdir -p /path/to/your/skills/corpify
cp SKILL.md /path/to/your/skills/corpify/
```

Common project-scoped locations: `.github/skills/corpify/`, `.agents/skills/corpify/`,
or `.claude/skills/corpify/`. Personal (all projects): `~/.copilot/skills/corpify/`.

> The canonical file is the root `SKILL.md`. The copy under `.github/skills/corpify/`
> exists so VS Code Copilot can discover it. If you edit one, sync the other.

## Usage

Invoke `/corpify` or just ask, and paste the raw message:

```text
/corpify

I'll do my work, you do yours. Stop chasing me every five minutes.
```

Ask for a specific tone or format:

```text
Corpify this as a firm-but-polite email: [your text]
```

Point it at a file to rewrite the message in place:

```text
Corpify the message in drafts/reply.txt
```

### Voice calibration

To match your own writing, include a sample:

```text
Here's how I usually write: [paste 2-3 of your own messages]

Now corpify this: [raw text]
```

Your sample outranks the default tone (but never the no-fabrication rule).

## Tones

| Tone | Use when |
| ---- | -------- |
| Diplomatic / soft-spoken | Bad news, pushback, apologies, sensitive or senior recipients |
| Warm-professional (default) | Most day-to-day email and chat |
| Firm-but-polite | Setting a boundary, declining, escalating, ignored asks |

## Output modes

- **Quick rewrite** (default): professional text, ready to paste.
- **Email**: full email with subject, greeting, body, and sign-off (auto when the input
  looks like an email, or on request).
- **File**: rewrite the message in a file in place.
- **Embedded**: final text only, for use as a step in a larger task.

## Core rules

- **Preserve the message and any boundary.** "It's none of your business" stays a
  boundary, just a polite one. A "no" stays a "no."
- **Never fabricate.** No invented dates, names, numbers, or commitments. If a specific
  is needed and not given, it asks or writes the plain version.
- **Stay human.** The anti-slop pass cuts em dashes, sycophancy, buzzwords, empty
  filler, and "I hope this finds you well" openers.

## Patterns handled

Hostility · blame · dismissiveness · demands · venting · rude boundary-setting ·
sarcasm/passive-aggression · profanity/slang · ultimatums/threats · over-apology ·
one-word replies. See `SKILL.md` for before/after examples of each.

It also handles **mixed-language / code-switched input** (e.g. Hinglish): it reads the
intent across languages, maps idioms to meaning, strips profanity in every language, and
returns professional English (or another language on request).

## Example

**Before:** "I'll do my work, you do yours. Stop chasing me every five minutes, it's
none of your business how I get it done."

**After (Firm-but-polite):** "I have my deliverables under control and will flag you if
anything changes. I'd appreciate the space to manage the how on my side, rather than
frequent check-ins, so I can keep the work moving. Happy to align on the key milestones
if that would help."

## Reference

Anti-slop rules adapted from [blader/humanizer](https://github.com/blader/humanizer)
(MIT), based on
[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## Contributing

Issues and pull requests are welcome. When changing behavior, keep the root `SKILL.md`
and its `.github/skills/corpify/` copy byte-identical, update the version in `SKILL.md`,
`README.md`, and `.claude-plugin/plugin.json` together, and run
`python scripts/validate-package.py` before opening a PR. See [AGENTS.md](AGENTS.md) for
the full maintenance contract.

## Author

Created and maintained by **[Mahantesh Hiremath](https://bit.ly/atozaboutdata)**.

## Version history

- 1.1.0 - Added mixed-language / code-switched handling (e.g. Hinglish): reads intent
  across languages, maps idioms to meaning, returns professional English by default (or
  another language on request), strips profanity and slurs, and refuses to launder pure
  abuse or threats into polite corporate English.
- 1.0.0 - Initial release. Rude/emotional to professional with three tones, output
  modes (quick / email / file / embedded), voice calibration, 11 corpify patterns with
  before/after, a no-fabrication rule, a boundary-preservation rule, and an anti-slop
  pass adapted from humanizer.

## License

MIT &copy; [Mahantesh Hiremath](https://bit.ly/atozaboutdata). See [LICENSE](LICENSE).
