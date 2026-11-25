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
    lowered = text.lower()
    if not any(token in lowered for token in OFFICE_TOKENS):
        raise ValueError("entry must turn on a real detail of office life")
    if any(cliche in lowered for cliche in CLICHES):
        raise ValueError("entry uses a worn-out office cliché")
    # One sentence: a single sentence-ending mark, at the very end.
    body = text[:-1] if text[-1] in ".!?" else text
    if any(mark in body for mark in (".", "!", "?", ";", ":")):
        raise ValueError("entry must be a single sentence")
    # Criterion 3: the laugh lands in the last few words. The twist here
    # is the comparison with the manager, so the line must end on it.
    if not text.endswith("better than my manager does."):
        raise ValueError("entry must land its punchline in the last words")
    return text


def main():
    validate(JOKE)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)


if __name__ == "__main__":
    main()
