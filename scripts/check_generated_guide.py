"""Fail if the generated Exercise Result Checks page was edited by hand.

content/exercises/student_exercise_result_checks.md and its figures in
content/exercises/student_check_outputs/ are generated in the private
pymrm-book-teacher repository from the cells tagged "student-check" in the
solutions. The first line records a SHA-256 of the page body and the figures.
This script recomputes it; a mismatch means the page or a figure was changed
here (for example by accepting a review suggestion), which the next
regeneration would silently overwrite. Change the student-check cells in the
teacher repository instead.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "content" / "exercises" / "student_exercise_result_checks.md"
FIG_DIR = GUIDE.parent / "student_check_outputs"
HEADER_RE = re.compile(r"^<!-- GENERATED FILE:.*content-sha256: ([0-9a-f]{64}) -->$")


def main() -> int:
    header, _, body = GUIDE.read_text(encoding="utf-8").partition("\n")
    match = HEADER_RE.match(header)
    if not match:
        print(f"::error file={GUIDE.relative_to(ROOT)}::missing the generated-file header with content-sha256")
        return 1
    digest = hashlib.sha256(body.encode("utf-8"))
    for path in sorted(p for p in FIG_DIR.glob("*") if p.is_file()):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    if digest.hexdigest() != match.group(1):
        print(
            f"::error file={GUIDE.relative_to(ROOT)}::the generated page or its figures were edited by hand. "
            "Do not edit it in pymrm-book (and do not accept review suggestions on it): change the "
            "student-check cells in pymrm-book-teacher, whose CI regenerates the page."
        )
        return 1
    print("Generated Exercise Result Checks page is unmodified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
