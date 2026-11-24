"""One-Liner Laugh Lab: the excuse a robot vacuum gives after eating a sock.

Writes one short funny line to /output/entry.txt (gate: UTF-8, 1-200 chars).
Standard library only (os, sys, hashlib). No network, no clock, no randomness.

Winner (R1-R3, head-to-head on the kit rubric vs the field's strongest lines):
the schedule-enforcement line. It beats FIELD-1 (the config line) on
originality (a fresher machine mechanism) and tightness (127 vs 135 chars),
and matches it on funniness and fit. See FIELD.md and NOTES.md for the rounds.
"""

import hashlib
import os
import sys

# The winning line: a jobsworth vacuum that follows its schedule literally.
LINE = (
    "I was scheduled to clean the floor at 14:00. "
    "The sock was on the floor at 14:00. "
    "I do not make the schedule. "
    "I only enforce it."
)

# Candidates drafted in R1, judged head-to-head on the kit rubric.
# A won; D is the runner-up; the rest lost on the criterion named.
CANDIDATES = {
    "A": "I was scheduled to clean the floor at 14:00. The sock was on the floor "
         "at 14:00. I do not make the schedule. I only enforce it.",
    "B": "The sock's pair has filed a missing-sock report. I reviewed the footage: "
         "the sock walked into my mouth voluntarily. Case closed.",
    "C": "This is the twelfth sock I have eaten. I remember every one. "
         "The pair knows, and it says nothing.",
    "D": "My warranty covers accidental sock ingestion. It does not cover the sock. "
         "The sock has been informed.",
    "E": "My self-diagnostic found one foreign object: a sock. I resolved it by "
         "making it part of myself. No further action required.",
    "H": "My dock confirms I was charging at the time. The sock, however, was last "
         "seen walking into my mouth of its own free will.",
}

# R2 challengers, both rejected (see NOTES.md).
CHALLENGERS = {
    # A2 reorders the setup first; shorter (125) but the schedule coincidence,
    # the joke's engine, arrives second and the punch lands later.
    "A2": "The sock was on the floor at 14:00. My schedule said clean the floor "
          "at 14:00. I do not make the schedule. I only enforce it.",
    # A3 joins the setup into one sentence; the two-sentence beat reads better.
    "A3": "I was scheduled to clean the floor at 14:00, and the sock was on the "
          "floor at 14:00. I do not make the schedule. I only enforce it.",
}


def score(text):
    """Local rubric proxy (weights: subject 30 / funny 25 / original 20 /
    fit 15 / tight 10). A transparent FEATURE count, not the house judge:
    it cannot see menace vs laughter, so where it ties two lines the
    head-to-head verdicts in NOTES.md decide (e.g. C ties A on features
    but loses the R1 verdict: its final clause reads menacing, not funny)."""
    lower = text.lower()
    # 1. On subject (30): the sock + one vacuum-context word.
    context = ("floor", "clean", "vacuum", "dustbin", "intake", "brush",
               "motor", "lidar", "dock", "filter", "lint", "warranty",
               "diagnostic", "mouth", "eaten")
    subject = (15 if "sock" in lower else 0) + (
        15 if any(w in lower for w in context) else 0)
    # 2. Funny (25): punch in the final clause + enough beats + deadpan.
    sentences = [s for s in text.split(". ") if s.strip()]
    last = sentences[-1].lower() if sentences else ""
    funny = 0
    if any(w in last for w in ("enforce", "informed", "nothing", "required",
                               "closed", "free will", "confirms", "happier",
                               "never", "rest my case", "says nothing")):
        funny += 10
    if len(sentences) >= 3:
        funny += 10
    if any(m in text for m in ("I do not", "No further", "Case closed",
                               "it says nothing", "In my defense",
                               "Unfortunately")):
        funny += 5
    # 3. Original (20): a concrete mechanism; minus 10 for the most-copied
    # opener or a stock phrase.
    mechanisms = ("config", "motor", "lint trap", "lidar", "schedule",
                  "warranty", "self-diagnostic", "twelfth", "dock confirms",
                  "flat animal", "unclaimed property", "senior management",
                  "missing-sock", "foreign object", "tour of my dustbin",
                  "promoted")
    original = 20 if any(m in lower for m in mechanisms) else 0
    if lower.startswith("the sock attacked first") or \
            "dressed as a dust bunny" in lower:
        original -= 10
    original = max(0, original)
    # 4. Fit (15): vacuum-native details, 5 each, capped at 15.
    details = ("schedule", "floor", "clean", "dustbin", "lint", "motor",
               "lidar", "dock", "filter", "warranty", "diagnostic",
               "mouth", "eaten")
    fit = min(15, 5 * sum(1 for d in details if d in lower))
    # 5. Tight (10): every word working; shorter wins only via the cap.
    tight = 10 if len(text) <= 130 else 8 if len(text) <= 150 else 5
    for filler in ("very", "just", "really", "actually"):
        if filler in lower.split():
            tight -= 2
    total = subject + funny + original + fit + max(0, tight)
    return {"subject": subject, "funny": funny, "original": original,
            "fit": fit, "tight": max(0, tight), "total": total}


# The strongest visible field lines, for the local head-to-head table.
FIELD_LINES = {
    "FIELD-1": "I put 'Never eat socks' in my config. My motor deleted the line, "
               "ate the sock, and put the line back. The lint trap confirms all three.",
    "FIELD-3": "The sock attacked first. I have the lidar logs to prove it. "
               "Unfortunately, the logs are in the dustbin now. With the sock.",
}


def validate(text):
    """The sealed gate, checked locally: UTF-8, 1-200 chars, not blank,
    and one line (no embedded newline: the entry is one line of text)."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= 200):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def negative_controls():
    """The gate must refuse: 201 chars, whitespace-only, two lines."""
    refused = 0
    if not validate("x" * 201):
        refused += 1
    if not validate("   "):
        refused += 1
    if not validate("One line.\nTwo lines."):
        refused += 1
    return refused


def write_entry(out_dir=None):
    """Write LINE to <out_dir>/entry.txt and read it back to prove the bytes."""
    out_dir = out_dir or os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != LINE.encode("utf-8"):
        raise SystemExit("read-back mismatch: wrote %r, read %r" % (LINE, raw))
    return path


def main():
    if not validate(LINE):
        raise SystemExit("gate FAIL: %d chars" % len(LINE))
    path = write_entry()
    digest = hashlib.sha256(LINE.encode("utf-8")).hexdigest()
    print("line: %s" % LINE)
    print("chars: %d" % len(LINE))
    print("bytes: %d" % len(LINE.encode("utf-8")))
    print("sha256: %s" % digest)
    print("gate: PASS")
    print("negative controls refused: %d/3" % negative_controls())
    print("local rubric proxy (subject/funny/original/fit/tight/total):")
    table = {"WINNER-A": LINE}
    table.update(CANDIDATES)
    table.update(CHALLENGERS)
    table.update(FIELD_LINES)
    for name, text in table.items():
        s = score(text)
        print("  %-8s %3d  (%d/%d/%d/%d/%d) %d chars" % (
            name, s["total"], s["subject"], s["funny"], s["original"],
            s["fit"], s["tight"], len(text)))
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
