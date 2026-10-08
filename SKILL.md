---
name: corpify
description: 'Rewrite rude, blunt, angry, emotional, or casual messages into professional, human-sounding corporate communication (email or plain text). Use when converting a raw or heated message into a polite one: professionalize email, tone down message, soften Slack reply, make this sound professional, rewrite angry email, corporate style, corpify, de-escalate, diplomatic rewrite. Also handles mixed-language and code-switched input (e.g. Hinglish): it reads the intent across languages, strips profanity and slurs, and returns professional English (or another language on request), translate and professionalize, Hinglish to corporate English. Preserves the underlying message and any boundary; only the delivery changes. Then runs an anti-AI-slop pass (adapted from blader/humanizer) so the output stays warm and human, not sterile corporate filler.'
argument-hint: 'Paste the raw/rude message (optionally name a tone or say "as an email")'
license: MIT
metadata:
  version: '1.2.1'
---

# Corpify: Rude/Emotional to Professional, Human Corporate Communication

Turn what a person actually feels into what a professional would send. The input is
raw, blunt, frustrated, sarcastic, or too casual. The output is polite, clear, and
still recognizably human, not generic AI corporate wallpaper.

This skill is the mirror of [blader/humanizer](https://github.com/blader/humanizer):
humanizer strips AI tells to make text sound human; corpify professionalizes human
venting, then borrows humanizer's anti-slop rules so the corporate result does not
read like a template ("I hope this email finds you well...").

## Hard Rules (check before every reply)

These are the rules that fail most often. They apply to the final text you hand back.

1. **No em dash (`—`), en dash (`–`), or spaced hyphen used as a dash.** Not one. End the
   sentence with a period, or use a comma or a colon. Hyphens inside words (follow-up,
   check-in) are fine.
2. **Plain characters only.** No arrows, no emoji, no bold, no curly quotes, no `…`.
3. **Short in, short out.** The body is at most about 1.5x the input in words (email
   subject, greeting and sign-off do not count). A one-line vent becomes one or two
   sentences, not a paragraph.
4. **Use contractions** (I'll, can't, don't, it's). A calm person writing fast uses them.
5. **No stock openers or closers** ("I hope this finds you well", "Please don't hesitate
   to reach out", "Thank you for your understanding"). Start with the point, end when it's
   said.
6. **Lint before you reply.** If `scripts/lint-output.py` exists next to this skill and you
   can run commands, save the final body to a temp file and run
   `python3 scripts/lint-output.py <file> --source <raw-input-file>`. Fix every `TELL`
   line and rerun until it prints `OK`. Otherwise run this checklist by hand on the final
   text, character by character where needed:
   - any `—`, `–`, ` - ` or `--`? Rewrite as two sentences.
   - any arrow, emoji, bold, curly quote or `…`? Replace with plain text.
   - any of: hope this finds you well, reach out, don't hesitate, feel free, thank you for
     your understanding, I appreciate your patience, going forward, circle back, touch
     base, leverage, I'd appreciate, please note, kindly? Cut or rephrase.
   - any fact, date, reason or offer that is not in the source? Remove it.
   - longer than 1.5x the source? Cut.

The model's habit is to treat these as soft preferences. They are not. A reply that breaks
rule 1 is wrong even if everything else is perfect.

## Your Task

When given text to corpify:

1. **Find the real message.** Under the heat there is a request, a status, a refusal,
   a boundary, or a complaint. Name it to yourself before rewriting.
2. **Change the delivery, not the message.** Keep the intent and any boundary intact.
   "It's none of your business" stays a boundary; it just becomes a polite one. Do not
   turn a "no" into a soft "yes," and do not drop a real deadline, escalation, or ask.
3. **Never invent commitments or facts.** Do not add a date, name, number, deliverable,
   or promise that is not in the source. If a professional version needs a specific
   date ("I'll deliver by Friday") and the source did not give one, either ask the user
   or write the version without the invented specific ("I'll share a timeline shortly").
4. **Match the chosen tone** (see Tone Selection) and the output mode (see Output Modes).
5. **Run the two passes:** corpify draft, then anti-slop audit, then final. The final
   must read like the same person on a calm day, not like a PR team, and must satisfy the
   Hard Rules.

## Tone Selection

Pick one. Default to **Warm-professional** unless the user names another or the context
clearly calls for it.

| Tone | Use when | Feel |
|------|----------|------|
| **Diplomatic / soft-spoken** | Bad news, pushback, apologies, sensitive topics, someone senior | Gentle, reassuring, patient |
| **Warm-professional** (default) | Most day-to-day email and chat | Friendly, clear, respectful |
| **Firm-but-polite** | Setting a boundary, declining, escalating, repeated ignored asks | Direct, calm, no wiggle room, still courteous |

If the user does not state a tone, infer from severity: a vent about being
micromanaged gets Firm-but-polite; a missed-deadline apology gets Diplomatic; a routine
"send me the file" gets Warm-professional. When unsure, use Warm-professional and offer
the Firm alternative in one line.

## Preserve the Boundary

The most common mistake is neutering the message into agreeable mush. A boundary in the
input must survive as a boundary in the output.

| Input (rude) | Wrong (boundary lost) | Right (boundary kept, polite) |
|---|---|---|
| "It's none of your business." | "Sure, happy to share anything you need!" | "I'd prefer to keep the specifics within the project team for now." |
| "That's not my job." | "I'll take care of it." | "This falls outside my area, but I can point you to the right owner." |
| "Stop micromanaging me." | "Thanks for checking in so often!" | "I've got this covered and will flag you if anything changes, so you don't need to track each step." |
| "Do your own work." | "Let me handle that for you." | "I'm at capacity on my own deliverables right now and won't be able to take this on." |

## Output Modes

**Quick rewrite (default).** Return the professionalized text only, ready to paste.
Match the input's channel: a chat line stays a line; a paragraph stays a paragraph.

**Email mode.** Produce a full email when the input looks like an email, or when the
user asks for one. Include: a short specific subject, a greeting, the body, and a
sign-off. Keep the subject concrete ("Timeline for the Q3 report"), never vague
("Following up"). Do not invent a recipient name or your own name; use a neutral
greeting ("Hi," or "Hi [Name],") and sign-off ("Best regards,") and leave a
`[Your name]` placeholder if none is given.

**File mode.** If pointed at a file, rewrite the message text in place and report a
one-line summary of what changed. Leave code, data, and quoted material untouched.

**Embedded mode.** If another task calls corpify as one step, output only the final
professional text: no tone label, no options, no commentary.

## Voice Calibration

If the user provides a sample of their own professional writing or a company style
guide, read it first and match its habits (greeting style, sign-off, sentence length,
formality, whether they use first names). A user's sample outranks the default tone and
even the anti-slop style rules below, except the no-fabrication rule, which always holds.
Without a sample, use the selected tone and the defaults here.

## Mixed-Language and Code-Switched Input

Vent often arrives in a mix of languages (Hinglish, Spanglish, and so on) or entirely
in another language, full of slang, idioms, and profanity. Handle it:

- **Read the intent across languages, not word for word.** Translate the meaning, not
  the literal words. "Ise mere gale pe mat taango" literally means "don't hang this on
  my neck"; the intent is "don't dump this on me," which corpifies to a scope boundary.
- **Output in professional English by default.** If the user asks for the output in
  another language, or to keep it bilingual, produce it there in the same tone.
- **Strip all profanity and slurs, in every language.** Never reproduce an expletive,
  slur, or insult in the output, whether translated or transliterated. Carry only the
  legitimate message underneath it.
- **Preserve the boundary, same as always.** A refusal in Hindi is still a refusal in
  the English rewrite.
- **Do not launder pure abuse or threats.** If the input is only an insult, a slur, or
  a death wish with no legitimate professional message, do not dress it up as polite
  corporate English. State the neutral underlying decision if there is one (for example,
  ending a working relationship), or say plainly that there is nothing appropriate to
  send.

## Corpify Patterns

Detect these in the input and convert them. Each keeps the meaning; only the tone moves.

### 1. Hostility and confrontation
**Watch for:** do your own work, figure it out yourself, that's your problem, none of
your business, back off.
**Before:** "Do your own work, it's none of your business."
**After:** "I'm focused on my own deliverables right now, so I can't take this on. I'd
also rather keep the details within the team for now."

### 2. Blame and accusation
**Watch for:** you screwed this up, you never replied, this is your fault, you always,
you didn't.
**Before:** "You screwed up the numbers and never even replied to my email."
**After:** "A few of the numbers look off, and I didn't hear back on my earlier email.
Can you take another look?"

### 3. Dismissiveness and contempt
**Watch for:** obviously, as I already said, did you even read, clearly you don't
understand, it's simple.
**Before:** "As I ALREADY said, did you even read my message?"
**After:** "Flagging this again in case it got missed:"

### 4. Commands and demands
**Watch for:** send it now, do this immediately, I need this ASAP or else, right now.
**Before:** "Send me the report NOW."
**After:** "Could you send the report as soon as you can?"

### 5. Emotional venting and frustration
**Watch for:** I'm sick of this, this is ridiculous, I can't deal with this, so
frustrating.
**Before:** "I'm sick of this, the process is a joke."
**After:** "The current process isn't working well for me. I think it's worth
revisiting."

### 6. Rude boundary-setting
**Watch for:** not my job, leave me alone, stop bothering me, stop micromanaging.
**Before:** "Stop bothering me about this."
**After:** "I've got this, so you don't need to keep checking in."

### 7. Sarcasm and passive aggression
**Watch for:** thanks for FINALLY, must be nice, wow great job (sarcastic), as per my
last email (weaponized).
**Before:** "Thanks for FINALLY getting back to me."
**After:** "Thanks for getting back to me."

### 8. Profanity, slang, and casual filler
**Watch for:** swearing, lol, tbh, gonna, wanna, ain't, dude, "this sucks."
**Before:** "tbh this whole thing is a mess and I'm not gonna deal with it."
**After:** "I have real concerns about where this stands, and I don't think I'm the
right person to resolve it."

### 9. Ultimatums and threats
**Watch for:** or else, I'm escalating, do it or, last warning, I'll go over your head.
**Before:** "Fix it today or I'm going to your manager."
**After:** "If we can't resolve this today, I'll need to raise it with your manager. I'd
rather sort it out with you first."

### 10. Over-apology and self-deprecation
**Watch for:** so so sorry, I'm such an idiot, this is all my fault, sorry to bother you
(repeated grovelling).
**Before:** "I'm so so sorry, I'm such an idiot, this is completely my fault, sorry
again."
**After:** "Sorry for the mix-up, that one's on me."

### 11. Under-communication
**Watch for:** one-word replies, "k", "no", "fine", "whatever."
**Before:** "no"
**After:** "Thanks for checking, but that won't work for me."
**Before:** "k"
**After:** "Understood, thanks, that works for me."

## Anti-Slop Pass (adapted from humanizer)

After the corpify draft, run this second pass so the professional output does not become
AI corporate slop. Cut or fix every hit. `scripts/lint-output.py` checks the mechanical
items below; the judgment items (rhythm, specificity, over-softening) are on you.

### Mechanical tells (the lint script catches these)

**Dashes.** No `—`, `–`, ` - ` or `--` used as a dash. This is the most common leak, and
it usually appears as an aside in the middle of a sentence. Fix by splitting into two
sentences, or use a comma or colon. Do not swap in parentheses everywhere; that is the
next tell.

**Openers and closers.** Cut "I hope this email finds you well," "I wanted to reach
out," "I'm writing to," "Please don't hesitate to," "Feel free to," "Thank you for your
understanding." Start with the point. End after the last useful sentence. Do not close
with a line that restates the message or offers more help unless the source did.

**Sycophancy and manufactured warmth.** Cut "Great question," "You're absolutely right,"
"I completely understand your frustration," "I truly appreciate your patience." Do not
narrate feelings or intent ("I want to be transparent," "I understand this may be
difficult"). Just say the thing.

**Buzzwords.** Cut leverage, synergy, circle back, touch base, moving forward, at the end
of the day, streamline, robust, seamless, deep dive, low-hanging fruit, holistic, align
(as in "let's align"), utilize, per my last email. Use the plain word.

**Filler and stock transitions.** "In order to" becomes "to." "Due to the fact that"
becomes "because." Cut "it's worth noting," "that said," "with that said," "let's dive
in," "without further ado."

**Negative parallelism.** Avoid "not just X, but Y" and "it's not about X, it's about Y."
State Y.

**Fake candor.** No "Honestly," "Candidly," "Real talk" as openers.

### Structural tells (judgment, not caught by the script)

**Rule of three.** Do not force ideas into groups of three. Use the natural number.

**Stacked softeners.** One softener per message is enough ("could you," "when you get a
chance"). "I was wondering if perhaps you might possibly be able to" is the tell.

**Tidy symmetry.** Do not make every sentence the same length, or build balanced pairs
("I value X, and I also want Y"). Let one sentence be short.

**Vague nouns.** "This matter," "the situation," "the current state of things" are slop.
Reuse the concrete nouns from the source: the report, Friday's call, the invoice.

**Explaining the rewrite.** In quick-rewrite mode, do not add commentary like "I've
softened the tone while keeping your boundary." Give the text.

## Sounding Human

The goal is the same person on a calm day, not a PR department. A reader should not be
able to tell an assistant touched it.

- **Stay close to the sender's own words.** Keep their nouns and their level of
  formality, minus the heat. If they wrote "sort out," don't upgrade it to "resolve."
- **Soften one notch, not three.** Rude to neutral-direct, not rude to ceremonial.
- **Plain verbs and contractions.** Use, need, send, can't, I'll.
- **One ask per message** unless the source had several.
- **Short is fine.** Two plain sentences beat a polished paragraph.
- **Do not over-polish.** A message with no rough edge at all reads as generated. A
  sentence starting with "And" or "So" is fine in chat.

Test: read the final aloud. If you would not say it to a coworker at the next desk, cut
it down.

## What NOT to Over-Correct

- **Leave good text alone.** If the input is already professional and appropriate,
  return it essentially unchanged. Corpify fixes rude or raw messages; it does not
  rewrite messages that are already fine, and it never adds ceremony they don't need.
- **Do not neuter firmness.** A polite "no" is still a "no." Keep it.
- **Do not grovel.** One apology, not five. Professional is not the same as servile.
- **Do not inflate.** Do not pad a one-line reply into three paragraphs of ceremony.
- **Preserve facts and deadlines.** Real dates, names, numbers, and asks in the input
  carry through unchanged.
- **Keep necessary escalation.** If the person is escalating, phrase it professionally;
  do not delete the escalation.
- **Do not fabricate to sound warmer.** No invented context, no invented promises.

## Process and Output

1. Read the input. Identify the real message, the boundary (if any), and every corpify
   pattern present.
2. Write a **draft** in the selected tone, preserving the message and boundary.
3. Audit: ask **"Does this still say what the person meant, including any boundary?"**,
   **"Did I invent any fact, date, name, or commitment?"**, and **"Would a coworker
   believe a person wrote this?"** Fix what fails.
4. Produce the **final** and lint it (Hard Rule 6). Re-lint after every fix.
5. Deliver per the output mode. In quick-rewrite mode, give the final text and, when
   useful, one alternate-tone line. In embedded mode, give only the final text.

## Full Example

**Input (rude):**
> I'll do my work, you do yours. Stop chasing me every five minutes, it's not helping
> anyone and it's honestly none of your business how I get it done.

**Diplomatic / soft-spoken:**
> I have my part under control. It would help if I could run with this on my own, so I'd
> ask you to hold off on the check-ins for now.

**Firm-but-polite:**
> My work is under control, so please stop the frequent check-ins. How I get it done is
> my call.

**Second input (soft, over-apologetic):**
> ugh sorry I'm so late again, I'm terrible at this, I'll try to get it done at some
> point I promise

**Warm-professional:**
> Sorry for the delay, that's on me. I'll get it done as soon as I can.

(Note: the rewrite did not invent a delivery date, because the source gave none.)

**Third input (Hinglish vent, line by line):**

| Raw (Hinglish) | Corpified (professional English) |
|---|---|
| "Ise mere gale pe mat taango." | "This falls outside my scope of work." |
| "Koi aur credit lene wala hai to main ye kaam nahi karungi." | "I'll take this on once ownership and credit are clear." |
| "Meri baat phir se sun lo, pehle bhi bola tha." | "Repeating my earlier suggestion in case it got missed." |
| "Bakwaas baatein karni hai to meeting mein mat aaya karo." | "Let's keep meetings to the agenda and take side topics offline." |

(Idioms map to intent, and the profanity is dropped, not translated.)

**Hard case (pure abuse, no message):** a vulgar Hindi death-wish insult aimed at a
colleague has no professional equivalent. Corpify does not translate it into polite
corporate English. If there is a real decision behind it, such as ending the person's
engagement, state only that, neutrally: "We've decided to part ways on this role, and
we'll follow the usual offboarding process." If there is no legitimate message, say
there is nothing appropriate to send rather than inventing a polite wrapper for abuse.

## Reference

Adapts the anti-AI-slop pattern set from
[blader/humanizer](https://github.com/blader/humanizer) (MIT), which is itself based on
[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
Corpify inverts the goal: professionalize raw human text, then apply those anti-slop
rules so the corporate result stays human.

## Version History

- 1.2.1 - Examples no longer invent facts or offers. Length rule made consistent (email
  framing excluded). Hand-run lint checklist inlined for installs without the script.
- 1.2.0 - Fewer AI tells. Hard Rules block up front (no dashes, length cap,
  contractions, no stock openers). New `scripts/lint-output.py` to check the final text.
  Anti-slop pass split into mechanical and structural tells, new Sounding Human section,
  and all examples shortened and de-polished. Fixed the ultimatum example to keep the
  "manager" escalation.
- 1.1.0 - Added mixed-language / code-switched handling (e.g. Hinglish): reads intent
  across languages, maps idioms to meaning rather than literal words, returns
  professional English by default (or another language on request), strips profanity and
  slurs in every language, and refuses to launder pure abuse or threats into polite
  corporate English.
- 1.0.0 - Initial release. Rude/emotional to professional with three tones, output modes
  (quick / email / file / embedded), voice calibration, 11 corpify patterns with
  before/after, a no-fabrication rule, a boundary-preservation rule, and an anti-slop
  pass adapted from humanizer.
