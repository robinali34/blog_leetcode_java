#!/usr/bin/env python3
"""Replace broken ```java blocks with canonical solutions where available."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from canonical_solutions import CANONICAL, problem_number  # noqa: E402
from fix_all_java_blocks import apply_java_fixes, CPP_MARKERS  # noqa: E402

JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}


def is_broken(code: str) -> bool:
    return bool(CPP_MARKERS.search(code))


def patch_file(path: Path) -> int:
    num = problem_number(path.name)
    if not num or num not in CANONICAL:
        return 0

    text = path.read_text(encoding="utf-8")
    solutions = CANONICAL[num]
    sol_idx = 0
    changed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal sol_idx, changed
        code = m.group(2)
        if sol_idx < len(solutions):
            if code.strip() != solutions[sol_idx].strip():
                changed += 1
                out = solutions[sol_idx]
                sol_idx += 1
                return m.group(1) + out + m.group(3)
            sol_idx += 1
            return m.group(0)
        if is_broken(code):
            fixed = apply_java_fixes(code)
            if fixed != code:
                changed += 1
                return m.group(1) + fixed + m.group(3)
        return m.group(0)

    updated = JAVA_BLOCK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> None:
    total = 0
    files = 0
    for p in sorted(ROOT.glob("_posts/*.md")):
        n = patch_file(p)
        if n:
            files += 1
            total += n
    print(f"Patched {total} java blocks in {files} posts")


if __name__ == "__main__":
    main()
