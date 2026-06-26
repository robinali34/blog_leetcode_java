#!/usr/bin/env python3
"""Sync leetcode-questions-list.md from C++ blog with Java URL adaptations."""

from __future__ import annotations

import re
from pathlib import Path

CPP = Path("/home/robina/rli/blog_leetcode/leetcode-questions-list.md")
JAVA = Path(__file__).resolve().parent.parent / "leetcode-questions-list.md"

REPLACEMENTS = [
    (r"robinali34\.github\.io/blog_leetcode/", "robinali34.github.io/blog_leetcode_java/"),
    (r"(?<![\w])\/blog_leetcode\/", "/blog_leetcode_java/"),
    (r"New to LeetCode or C\+\+\?", "New to LeetCode or Java?"),
    (r"\[C\+\+ Guide\]\(/blog_leetcode_java/cpp-guide/\)", "[Java Guide](/blog_leetcode_java/java-guide/)"),
    (r"Learn C\+\+ for competitive programming -- language essentials, STL, patterns, and modern C\+\+ features",
     "Learn Java for LeetCode — language essentials, collections, patterns, and modern Java features"),
    (r"\| \[C\+\+ Guide\]", "| [Java Guide]"),
]

JAVA_GUIDES_SECTION = """## Guides & References

New to LeetCode or Java? Start here. For a curated interview path, see the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150) list (full breakdown in the Beginner's Guide).

| Guide | Description |
|---|---|
| [Interview Prep Hub](/blog_leetcode_java/interview-prep/) | Central starting point — NeetCode tracker, Meta list, study order |
| [NeetCode 150 Tracker](/blog_leetcode_java/neetcode-150-tracker.html) | Track NeetCode 150 with blog solution links |
| [LeetCode Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/) | What LeetCode is, how it works, difficulty levels, Blind 75, **NeetCode 150 full problem list**, and a step-by-step roadmap |
| [Java Guide](/blog_leetcode_java/java-guide/) | Learn Java for LeetCode — language essentials, collections, patterns, and modern Java features |
| [LeetCode Templates Index](/blog_leetcode_java/leetcode-templates/) | All algorithm pattern templates with relationship diagram |
| [Meta-Style Question List](/blog_leetcode_java/posts/2025-09-24-meta-question-list/) | FAANG-style curated list with blog solution links |
| [NeetCode 150 (official)](https://neetcode.io/practice/practice/neetcode150) | 150 curated problems with progress tracking on NeetCode |

---
"""


def main() -> None:
    text = CPP.read_text(encoding="utf-8")
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)

    # Replace Guides section with Java-specific version
    start = text.find("## Guides & References")
    end = text.find("## All LeetCode Problems")
    if start != -1 and end != -1:
        text = text[:start] + JAVA_GUIDES_SECTION + "\n" + text[end:]

    JAVA.write_text(text, encoding="utf-8")
    print(f"Updated {JAVA}")


if __name__ == "__main__":
    main()
