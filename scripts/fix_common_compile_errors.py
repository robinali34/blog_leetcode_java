#!/usr/bin/env python3
"""Fix common Java compile errors left from C++ conversion."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}


def fix(code: str) -> str:
    r = code

    # Set.of / missing semicolons after factory calls
    r = re.sub(r"Set\.of\(([^)]+)\)\s*\n", r"Set.of(\1);\n", r)

    # C++-isms on Java collections
    r = re.sub(r"(\w+)\.count\(([^)]+)\)", r"\1.contains(\2)", r)
    r = re.sub(r"(\w+)\.pop\s*\(\s*\)", r"\1.poll()", r)

    # String[] board indexed like char[][]
    r = re.sub(r"board\[(\w+)\]\[(\w+)\]", r"board[\1].charAt(\2)", r)

    # Invalid declarations inside methods (C++ style)
    r = re.sub(
        r"^(\s+)public\s+((?:List<[^>]+>|int\[\]\[\]|int\[\]|ListNode|boolean|int|String)\s+\w+\s*=)",
        r"\1\2",
        r,
        flags=re.M,
    )

    # return {} for collections
    r = re.sub(r"return\s*\{\s*\}\s*;", "return new ArrayList<>();", r)

    # int[]stk((n + 1) / 2) C++ ctor syntax
    r = re.sub(r"int\[\]\s*(\w+)\s*\(\s*\(([^)]+)\)\s*/\s*(\d+)\s*\)", r"int[] \1 = new int[(\2) / \3]", r)
    r = re.sub(r"int\[\]\s*(\w+)\s*\(\s*(\w+)\s*\)", r"int[] \1 = new int[\2]", r)

    # Missing operator between identifiers (num1 num2 -> num1 * num2)
    r = re.sub(r"(\w+)\s+(\w+)\s*;\s*break\s*;", r"\1 * \2; break;", r)

    # for (int x : stringArray) when iterating tokens
    r = re.sub(r"for\s*\(\s*int\s+(\w+)\s*:\s*tokens\s*\)", r"for (String \1 : tokens)", r)

    # Escaped brace literals from bad conversion
    r = r.replace(r"\{\{", "{{").replace(r"\}\}", "}}")

    # constexpr / array C++
    r = re.sub(r"constexpr\s+array<[^>]+>\s+\w+\s*=", "int[][] dirs =", r)

    # this.win -> win (valid in instance methods)
    r = re.sub(r"this\.win\(", "win(", r)

    # switch on token[0] when token is String - ok in Java
    # token[0] on String in Java is charAt(0) in older style - actually token.charAt(0) 
    r = re.sub(r"switch\s*\(\s*(\w+)\[0\]\s*\)", r"switch (\1.charAt(0))", r)

    # swap(a, b) without method - inline for ints
    # leave for manual/canonical

    # Python blocks mislabeled - skip in java blocks

    return r


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + fix(m.group(2)) + m.group(3)

    updated = JAVA_BLOCK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = sum(
        1 for p in ROOT.rglob("*.md")
        if not any(x in SKIP_DIRS for x in p.parts) and process_file(p)
    )
    print(f"Fixed compile patterns in {n} files")


if __name__ == "__main__":
    main()
