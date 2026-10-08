#!/usr/bin/env python3
"""Flag AI tells in a corpified message. Exit 1 if any hit, 0 if clean.

Usage:
  python3 scripts/lint-output.py draft.txt
  echo "text" | python3 scripts/lint-output.py -
  python3 scripts/lint-output.py draft.txt --source raw.txt   # also checks length ratio
"""
import re
import sys

CHARS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u2015": "horizontal bar",
    "\u2012": "figure dash",
    "\u2192": "arrow",
    "\u2026": "ellipsis char",
    "\u201c": "curly quote",
    "\u201d": "curly quote",
    "\u2018": "curly quote",
    "\u2019": "curly apostrophe",
}

PATTERNS = [
    (r"\s--+\s|\w--+\w", "double hyphen used as a dash"),
    (r"\S\s-\s\S", "spaced hyphen used as a dash"),
    (r"->|=>", "ascii arrow"),
    (r"\*\*|__", "bold markup"),
    (r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "emoji"),
    (r"hope this (email|message|note) finds you", "stock opener"),
    (r"\b(i )?wanted to (reach out|touch base|follow up|check in)", "stock opener"),
    (r"\breach(ing)? out\b", "reach out"),
    (r"i('m| am) writing to", "stock opener"),
    (r"\b(please )?(do not|don't) hesitate\b", "stock closer"),
    (r"\bfeel free to\b", "stock closer"),
    (r"\brest assured\b|\bplease be advised\b|\bkindly\b|\bgentle reminder\b", "stiff filler"),
    (r"\bthank you for your (patience|understanding|cooperation|continued)", "stock closer"),
    (r"\bi (completely |totally |fully )?understand your (frustration|concern)", "sycophancy"),
    (r"\b(great question|you're absolutely right|you are absolutely right)", "sycophancy"),
    (r"\bi (truly |really |deeply )?appreciate (your|the) (patience|understanding|flexibility|support)", "manufactured warmth"),
    (r"\b(going|moving) forward\b|\bcircl(e|ing) back\b|\btouch(ing)? base\b|\bat the end of the day\b", "buzzword"),
    (r"\b(leverag\w*|synerg\w*|streamlin\w*|robust|seamless\w*|deep dive|low-hanging|utiliz\w*|holistic|alignment)\b", "buzzword"),
    (r"\bper my last\b|\bas per\b", "weaponized or stiff phrase"),
    (r"\bin order to\b|\bdue to the fact\b|\bat this point in time\b|\bit('s| is) worth noting\b", "filler"),
    (r"\b(let's|let us) dive in\b|\bwithout further ado\b|\bhere's what you need to know\b", "signposting"),
    (r"\bnot (just|only|merely) [^.]{1,60}\bbut\b", "negative parallelism"),
    (r"\b(honestly|candidly|real talk)\s*[,?:]", "fake-candid opener"),
    (r"\bi hope (this|that) (helps|works|makes sense)\b", "stock closer"),
    (r"\bthat said,|\bwith that said,|\bthat being said,", "stock transition"),
    (r"\bi('d| would) appreciate\b", "stiff request"),
    (r"\bplease note\b|\bjust a (quick|friendly)\b|\bapologies for (any|the) inconvenience\b", "stock phrase"),
    (r"\bi (just )?wanted to (flag|mention|let you know)\b", "stock opener"),
    (r"\bi was wondering if\b|\b(perhaps|possibly|maybe)\b[^.]{0,40}\b(perhaps|possibly|might|could)\b", "stacked hedging"),
    (r"\bregret to inform\b|\bat your earliest convenience\b|\bwant to be transparent\b|\bi understand (that )?this (may|might)\b", "stiff phrase"),
]


def main() -> int:
    args = sys.argv[1:]
    source = None
    if "--source" in args:
        i = args.index("--source")
        source = open(args[i + 1], encoding="utf-8").read()
        del args[i : i + 2]
    path = args[0] if args else "-"
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()

    hits = []
    for ch, name in CHARS.items():
        if ch in text:
            hits.append(f"{name} x{text.count(ch)}")
    for pat, name in PATTERNS:
        for m in re.finditer(pat, text, re.I):
            hits.append(f"{name}: {m.group(0).strip()!r}".encode("ascii", "backslashreplace").decode())

    if source:
        src_words, out_words = len(source.split()), len(text.split())
        if src_words and out_words > max(1.5 * src_words, src_words + 12):
            hits.append(f"too long: {out_words} words vs {src_words} in source")

    for h in hits:
        print("TELL:", h)
    if not hits:
        print("OK: no tells found")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
