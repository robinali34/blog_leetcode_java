#!/usr/bin/env python3
"""Run all C++ → Java blog sync steps in order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent

STEPS = [
    ("sync_solution_posts_from_cpp.py", "Solution posts (prose, SVG, Java code)"),
    ("sync_template_content_from_cpp.py", "Template posts"),
    ("sync_beginners_guide_from_cpp.py", "Beginner's guide"),
    ("sync_java_guide_from_cpp.py", "Java guide basics"),
    ("sync_questions_list_from_cpp.py", "Questions list"),
    ("fix_all_links.py", "Internal links"),
    ("generate_neetcode_tracker.py", "NeetCode 150 tracker"),
]


def main() -> int:
    for script, label in STEPS:
        path = SCRIPTS / script
        if not path.is_file():
            print(f"skip missing: {script}")
            continue
        print(f"\n=== {label} ({script}) ===")
        rc = subprocess.call([sys.executable, str(path)], cwd=ROOT)
        if rc != 0:
            print(f"FAILED: {script} (exit {rc})")
            return rc
    print("\nAll sync steps completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
