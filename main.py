#!/usr/bin/env python3
"""One-Line Office Jokes (make.fun entry).

The joke: the office printer only ever jams when the writer is already
late, and the punchline reframes the jam as the printer reading the
writer's calendar more carefully than their manager does. The setup is a
concrete office detail (printer + calendar); the laugh lands in the last
few words, as the judge's brief requires; the wording is original, not a
circulating office joke, and it needs no setup beyond the line itself.
"""

import os

JOKE = (
    "Our printer only jams when I'm already late, which is how I know "
    "it reads my calendar better than my manager does."
)

OUT_PATH = "/output/entry.txt"

# Gate (from the kit's RULES.txt): /output/entry.txt must be UTF-8 text of
# 1 to 199 characters, not only white space. main() enforces the same bound
# here so a bad edit fails loudly instead of submitting an invalid entry.
MIN_CHARS = 1
MAX_CHARS = 199

# Judge criterion 2: the line must turn on a real detail of office life
# (meetings, email, the printer, the coffee machine), not generic talk
# about work. This joke's details are the printer and the calendar.
OFFICE_TOKENS = ("printer", "calendar", "meeting", "email", "coffee machine",
                 "boss", "manager", "desk", "HR", "standup", "inbox")

# Worn-out office lines that flood a field of one-line entries. The judge's
# criterion 5 rewards fresh wording; any of these in the text means the
# entry is playing a joke everyone has already heard.
CLICHES = ("could have been an email", "per my last email", "circle back",
           "synergy", "reply all", "take this offline", "low-hanging fruit",
           "quick sync", "bandwidth", "touch base", "ping me",
           "this meeting could have been", "monday meeting",
           "case of the mondays", "working hard or hardly working",
           "live laugh love", "rise and grind")


def _check_gate(text):
    """Gate checks from the kit's RULES.txt: 1-199 characters, one line,
    not only whitespace, valid UTF-8, no leading/trailing space and no
    double spaces. A bad entry must fail loudly here, before any of the
    judge-criterion checks run, so a broken edit never reaches the
    output file looking like a valid submission.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "  " in text:
        raise ValueError("entry must be tight: no double spaces")


def _check_office_detail(text):
    """Judge criteria 2 and 5: the line must turn on a real detail of
    office life, and it must not lean on a worn-out office cliché.
    """
    lowered = text.lower()
    if not any(token in lowered for token in OFFICE_TOKENS):
        raise ValueError("entry must turn on a real detail of office life")
    if any(cliche in lowered for cliche in CLICHES):
        raise ValueError("entry uses a worn-out office cliché")


def _check_single_sentence(text):
    """Judge criterion 4: one sentence, clear on one reading. A single
    sentence-ending mark is allowed, and only at the very end.
    """
    body = text[:-1] if text[-1] in ".!?" else text
    if any(mark in body for mark in (".", "!", "?", ";", ":")):
        raise ValueError("entry must be a single sentence")


def _check_punchline(text):
    """Judge criterion 3: the laugh lands in the last few words. The
    twist here is the comparison with the manager, so the line must end
    on it; a punchline parked up front would read as a setup with no
    payoff.
    """
    if not text.endswith("better than my manager does."):
        raise ValueError("entry must land its punchline in the last words")


def validate(text):
    """Fail loudly if the entry would fail the gate or lose on the judge's
    own criteria. Returns the validated text unchanged.

    Gate: 1-199 characters, one line, not only whitespace, valid UTF-8.
    Judge: a single sentence about office life (criterion 1-2), with the
    punch in the last few words (criterion 3: the twist must sit at the
    end, not up front), clear on one reading (criterion 4: no second
    sentence, no double space, no unexplained setup), and fresh wording
    (criterion 5: no circulating office cliché).
    """
    _check_gate(text)
    _check_office_detail(text)
    _check_single_sentence(text)
    _check_punchline(text)
    _check_read_aloud(text)
    return text


def _check_read_aloud(text):
    """Brand-new check: the line must survive being read aloud once.
    A one-line office joke is spoken, not studied, so it must stay
    short enough to hold in one breath and must not bury its twist
    behind a long subordinate clause. Concretely: at most 30 words,
    the setup (everything before the comma) at most 12 words, and the
    punchline clause must carry at least two content words after the
    comparison word, so the ending lands instead of trailing off.
    """
    words = text.split()
    if len(words) > 30:
        raise ValueError(
            f"entry must read aloud in one breath (<=30 words), "
            f"got {len(words)}")
    setup, _, punch = text.partition(",")
    if len(setup.split()) > 12:
        raise ValueError("entry setup must stay short: at most 12 words")
    tail = punch.rsplit("better than", 1)[-1].split()
    if len(tail) < 2:
        raise ValueError("entry punchline must land with a full comparison")


def main():
    validate(JOKE)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)


if __name__ == "__main__":
    main()
