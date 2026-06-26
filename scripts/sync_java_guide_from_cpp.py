#!/usr/bin/env python3
"""Merge cpp-guide.md prose/SVG into java-guide-basics.md; preserve Java code blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_template_content_from_cpp import merge_bodies, strip_front_matter  # noqa: E402

CPP = Path("/home/robina/rli/blog_leetcode/cpp-guide.md")
JAVA = Path(__file__).resolve().parent.parent / "_posts/2026-06-24-java-guide-basics.md"

JAVA_FM = """---
layout: post
title: "Java Guide: Language Basics"
date: 2026-06-24 10:00:00 -0700
categories: java guide reference tutorial programming fundamentals
permalink: /posts/2026-06-24-java-guide-basics/
tags: [java, guide, basics, tutorial, leetcode, collections, arrays, strings, oop, templates, java-21, java-25, java-26]
---
"""

GUIDE_REPLACEMENTS = [
    (r"robinali34\.github\.io/blog_leetcode/", "robinali34.github.io/blog_leetcode_java/"),
    (r"(?<![\w])\/blog_leetcode\/", "/blog_leetcode_java/"),
    (r"C\+\+ Guide: From Basics to LeetCode-Ready", "Java Guide: Language Basics"),
    (r"Why C\+\+ for Algorithms\?", "Why Java for Algorithms?"),
    (r"C\+\+ for Algorithms", "Java for Algorithms"),
    (r"New to C\+\+\?", "New to Java?"),
    (r"\[C\+\+ Guide\]", "[Java Guide]"),
    (r"cpp-guide", "java-guide"),
    (r"/posts/2025-09-23-cpp-cheatsheet/", "/posts/2025-09-23-java-cheatsheet/"),
    (r"C\+\+ Collections Quick Reference", "Java Collections Quick Reference"),
    (r"STL Toolkit", "Collections Toolkit"),
    (r"Modern C\+\+ \(20/23\)", "Modern Java (21+)"),
    (r"Cheat Sheet", "Quick Reference"),
    (r"\[Beginner's Guide\]\(/blog_leetcode_java/2026/06/25/leetcode-beginners-guide/\)",
     "[Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/)"),
]


def adapt_guide(text: str) -> str:
    for pattern, repl in GUIDE_REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text


def main() -> None:
    _, cpp_body = strip_front_matter(CPP.read_text(encoding="utf-8"))
    java_fm, java_body = strip_front_matter(JAVA.read_text(encoding="utf-8"))
    cpp_body = adapt_guide(cpp_body)

    # Prepend hub intro if missing
    hub = (
        "Part of the [Java Guide](/blog_leetcode_java/java-guide/) — practical Java for algorithm problems. "
        "For a compact API lookup, see the [Java Collections Quick Reference]"
        "(/blog_leetcode_java/posts/2025-09-23-java-cheatsheet/).\n\n"
    )
    if "Part of the [Java Guide]" not in java_body:
        cpp_body = cpp_body.replace(
            "# Java Guide: Language Basics\n\n",
            "# Java Guide: Language Basics\n\n" + hub,
            1,
        )

    merged = merge_bodies(cpp_body, java_body)
    if not merged.lstrip().startswith("{% raw %}"):
        merged = "{% raw %}\n" + merged.rstrip() + "\n{% endraw %}\n"

    JAVA.write_text(JAVA_FM + "\n" + merged.lstrip(), encoding="utf-8")
    print(f"Updated {JAVA}")


if __name__ == "__main__":
    main()
