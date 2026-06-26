#!/usr/bin/env python3
"""Sync leetcode-questions-list.md from C++ blog with Java URL adaptations."""

from __future__ import annotations

import re
from pathlib import Path

CPP = Path("/home/robina/rli/blog_leetcode/leetcode-questions-list.md")
JAVA = Path(__file__).resolve().parent.parent / "leetcode-questions-list.md"

REPLACEMENTS = [
    (r"robinali34\.github\.io/blog_leetcode/", "robinali34.github.io/blog_leetcode_java/"),
    (r"/blog_leetcode/", "/blog_leetcode_java/"),
    (r"New to LeetCode or C\+\+\?", "New to LeetCode or Java?"),
    (r"\[C\+\+ Guide\]\(/blog_leetcode_java/cpp-guide/\)", "[Java Guide](/blog_leetcode_java/java-guide/)"),
    (r"Learn C\+\+ for competitive programming -- language essentials, STL, patterns, and modern C\+\+ features",
     "Learn Java for LeetCode — language essentials, collections, patterns, and modern Java features"),
    (r"\| \[C\+\+ Guide\]", "| [Java Guide]"),
]


def main() -> None:
    text = CPP.read_text(encoding="utf-8")
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    JAVA.write_text(text, encoding="utf-8")
    print(f"Updated {JAVA}")


if __name__ == "__main__":
    main()
