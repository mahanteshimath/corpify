#!/usr/bin/env python3
"""Regression test for lint-output.py. Exit 1 if any case behaves wrongly."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

LINT = Path(__file__).resolve().parent / "lint-output.py"

# (name, source, output). Clean outputs must pass; dirty outputs must be flagged.
CLEAN = [
    ("demand", "Send me the report NOW.", "Could you send the report as soon as you can?"),
    ("ignored x3", "You never reply to my emails. This is the third time I'm asking.",
     "This is the third time I've asked. I need a reply on this."),
    ("meeting", "lol this meeting could've been an email, why am I here",
     "I'm not sure I need to be in this meeting. Could this have been covered over email?"),
    ("email", "Tell Raj his code is garbage, it broke prod again, fix it or I'm done reviewing his PRs",
     "Hi Raj,\n\nThe latest change broke production again. Please fix it. If this keeps happening, "
     "I'll stop reviewing your PRs.\n\nBest regards,\n[Your name]"),
    ("hinglish", "Yaar ye kaam mera nahi hai, mujhe bar bar mat bolo.",
     "This isn't my area, so please stop asking me about it."),
    ("already fine", "Thanks, I'll review it tomorrow.", "Thanks, I'll review it tomorrow."),
    ("sarcasm", "Thanks for FINALLY getting back to me.", "Thanks for getting back to me."),
    ("overapology", "so sorry so sorry I'm an idiot, I forgot the invoice",
     "Sorry, I forgot the invoice. That's on me."),
    ("bullets", "list the issues", "Issues:\n  - the build fails\n  - the tests are flaky"),
    ("decline", "I can't make it, sorry", "Unfortunately I can't make it, sorry."),
    ("maybe", "maybe later", "Maybe later, I'm busy now."),
]

DIRTY = [
    ("em dash", "Thanks for the update\u2014I'll send it Friday."),
    ("en dash", "Mon\u2013Fri works for me."),
    ("spaced hyphen", "Thanks for the update - I'll send it Friday."),
    ("opener/closer", "I hope this email finds you well. I wanted to reach out to kindly request the "
                      "report at your earliest convenience. Thank you for your understanding."),
    ("buzzwords", "Let's leverage this and circle back to streamline the process."),
    ("emoji", "Thanks \U0001F600"),
    ("bold", "Please **review** this."),
    ("curly", "I\u2019ll send it today."),
    ("neg parallel", "This is not just a delay, but a risk to the whole project."),
    ("fake candor", "Honestly, I think this needs another look."),
    ("sycophancy", "Great question! You're absolutely right."),
    ("stiff", "Please be advised that the deadline has moved. Do not hesitate to contact me."),
    ("hedge", "I was wondering if perhaps you might possibly be able to send it."),
    ("regret", "We regret to inform you that the request was declined."),
]


def lint(out, src="x " * 30):
    with tempfile.TemporaryDirectory() as t:
        o, s = os.path.join(t, "o.txt"), os.path.join(t, "s.txt")
        Path(o).write_text(out, encoding="utf-8")
        Path(s).write_text(src, encoding="utf-8")
        p = subprocess.run([sys.executable, str(LINT), o, "--source", s],
                           capture_output=True, text=True, encoding="utf-8")
        return p.returncode


def main():
    bad = [f"false positive: {n}" for n, s, o in CLEAN if lint(o, s) != 0]
    bad += [f"missed: {n}" for n, o in DIRTY if lint(o) != 1]
    # length check needs its own tiny source
    if lint("Understood, thank you for letting me know about that. That works for me and I will proceed as planned.", "k") != 1:
        bad.append("missed: too long")
    for b in bad:
        print("FAIL:", b)
    if not bad:
        print(f"OK: {len(CLEAN)} clean and {len(DIRTY) + 1} dirty cases behave")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
