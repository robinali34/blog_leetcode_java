#!/usr/bin/env python3
"""Sync beginners guide prose from C++ blog, keeping Java front matter and Java-specific sections."""

from __future__ import annotations

import re
from pathlib import Path

CPP = Path("/home/robina/rli/blog_leetcode/_posts/2026-06-25-leetcode-beginners-guide.md")
JAVA = Path(__file__).resolve().parent.parent / "_posts/2026-06-25-leetcode-beginners-guide.md"

JAVA_FM = """---
layout: post
title: "LeetCode Beginner's Guide: From Zero to Competitive Programming"
date: 2026-06-25 10:00:00 -0700
categories: [guide, leetcode, java]
tags: [guide, leetcode, beginner, competitive-programming, interview-prep, java]
permalink: /posts/2026-06-25-leetcode-beginners-guide/
---
"""

JAVA_LANGUAGE_SECTION = """### Which Language Should I Use on This Blog?

| Language | Best For | Trade-offs | Guide |
|---|---|---|---|
| **Java** (recommended here) | Interviews, readable typed code, strong collections API | More boilerplate than Python; use `HashMap`, `Deque`, `PriorityQueue` | [Java Guide](/blog_leetcode_java/java-guide/) |
| **Python** | Rapid prototyping, short syntax | Slower runtime; may TLE on tight constraints | — |

**Bottom line:** All solutions on **this blog** are in **Java**. Pick Java in the LeetCode language dropdown and use the [Java Guide](/blog_leetcode_java/java-guide/) while you learn. In real interviews, the algorithm matters more than the language — but stick to one language until patterns feel automatic.
"""

JAVA_QUICK_LINKS = """## Quick Links

| Resource | Description |
|---|---|
| [Interview Prep Hub](/blog_leetcode_java/interview-prep/) | Central hub — NeetCode 150 tracker, Meta list, study order |
| [NeetCode 150 Tracker](/blog_leetcode_java/neetcode-150-tracker.html) | Track NeetCode 150 with blog solution links |
| [Java Guide](/blog_leetcode_java/java-guide/) | Learn Java for LeetCode — intro, learning path, language basics |
| [LeetCode Templates Index](/blog_leetcode_java/leetcode-templates/) | All algorithm pattern templates on this blog |
| [Meta-Style Question List](/blog_leetcode_java/posts/2025-09-24-meta-question-list/) | FAANG-style curated list with blog links |
| [NeetCode 150 (official)](https://neetcode.io/practice/practice/neetcode150) | Curated 150-problem interview roadmap with progress tracking |
| [All Solved Problems](/blog_leetcode_java/leetcode-questions-list.html) | Every problem solved on this blog, with links |
| [Java Collections Quick Reference](/blog_leetcode_java/posts/2025-09-23-java-cheatsheet/) | Fast API lookup while coding |
"""

TEXT_REPLACEMENTS = [
    (r"robinali34\.github\.io/blog_leetcode/", "robinali34.github.io/blog_leetcode_java/"),
    (r"/blog_leetcode/", "/blog_leetcode_java/"),
    (r"> \*\*New to C\+\+\?\*\* Check out the \[C\+\+ Guide\]\(/blog_leetcode_java/cpp-guide/\) to learn the language alongside this guide\.",
     "> **New to Java?** Check out the [Java Guide](/blog_leetcode_java/java-guide/) to learn the language alongside this guide."),
    (r"1\. \*\*Pick a language\*\* -- C\+\+, Python, Java, or others \(new to C\+\+? See the \[C\+\+ Guide\]\(/blog_leetcode_java/cpp-guide/\)\)",
     "1. **Pick a language** — select **Java** in the editor (new to Java? See the [Java Guide](/blog_leetcode_java/java-guide/))"),
    (r"2\. \*\*Write your code\*\* in the browser editor",
     "2. **Write your code** in the browser editor — usually inside `class Solution { ... }`"),
    (r"3\. \*\*Click \"Run\"\*\* -- tests",
     "3. **Click \"Run\"** — tests"),
    (r"4\. \*\*Click \"Submit\"\*\* -- tests",
     "4. **Click \"Submit\"** — tests"),
    (r"\*\*Runtime Error \(RE\)\*\* \| Crash \(null pointer, out of bounds, etc\.\)",
     "**Runtime Error (RE)** | Crash (`NullPointerException`, out of bounds, etc.)"),
    (r"\| Hash map, sliding window \|", "| HashMap, sliding window |"),
    (r"\*\*You'll use:\*\* Arrays, hash maps, basic string operations, simple loops\.",
     "**You'll use:** Arrays, `HashMap`, basic string operations, simple loops."),
    (r"Yes: use a hash map\.", "Yes: use a `HashMap`."),
    (r"Pure pointer manipulation, no tricks\.", "Update `ListNode.next` references in place."),
    (r"Combine a hash map with a linked list\.", "Combine a `HashMap` with a linked structure."),
    (r"- \*\*Arrays and strings\*\* -- looping, indexing, basic manipulation",
     "- **Arrays and strings** — looping, indexing, `charAt`, `StringBuilder`"),
    (r"- \*\*Hash maps\*\* -- the single most useful data structure in interviews \(instant lookup\)",
     "- **Hash maps** — the single most useful data structure in interviews (`HashMap`, `HashSet`)"),
    (r"- \*\*Linked lists\*\* -- pointer manipulation \(this feels weird at first, that's normal\)",
     "- **Linked lists** — `ListNode` and updating `next` references (feels weird at first, that's normal)"),
    (r"- \*\*Stacks and queues\*\* -- LIFO vs FIFO, when to use each",
     "- **Stacks and queues** — use `Deque` / `ArrayDeque` for stack; `Queue` for BFS"),
    (r"> \*\*Learning C\+\+ alongside\?\*\* Work through Stages 1-2 of the \[C\+\+ Guide\]\(/blog_leetcode_java/cpp-guide/\) in parallel\.",
     "> **Learning Java alongside?** Work through [Language Basics](/blog_leetcode_java/posts/2026-06-24-java-guide-basics/) and the [Collections Quick Reference](/blog_leetcode_java/posts/2025-09-23-java-cheatsheet/) in parallel."),
    (r"\| Hash Map \|", "| HashMap |"),
    (r"\| Hash Set \|", "| HashSet |"),
    (r"\| Hash Map / Sorting \|", "| HashMap / Sorting |"),
    (r"\| Stack \|", "| Stack (`Deque`) |"),
    (r"\| \[Arrays & Strings\]\(/blog_leetcode_java/posts/2025-10-29-leetcode-templates-arrays-strings/\)",
     "| [String Processing](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-string-processing/)"),
    (r"\| \[Arrays & Strings\]\(/blog_leetcode_java/posts/2025-10-29-leetcode-templates-arrays-strings/\) \|",
     "| [Array & Matrix](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-array-matrix/) |"),
]


def strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text[end + 4 :].lstrip("\n") if end != -1 else text


def replace_language_section(body: str) -> str:
    start = body.find("### Which Language Should I Use?")
    end = body.find("## Getting the Most Out of LeetCode")
    if start == -1 or end == -1:
        return body
    return body[:start] + JAVA_LANGUAGE_SECTION + "\n" + body[end:]


def replace_quick_links(body: str) -> str:
    start = body.find("## Quick Links")
    if start == -1:
        return body.rstrip() + "\n\n" + JAVA_QUICK_LINKS + "\n"
    return body[:start] + JAVA_QUICK_LINKS + "\n"


def main() -> None:
    body = strip_front_matter(CPP.read_text(encoding="utf-8"))
    for pattern, repl in TEXT_REPLACEMENTS:
        body = re.sub(pattern, repl, body)
    body = replace_language_section(body)
    body = replace_quick_links(body)
    JAVA.write_text(JAVA_FM + "\n" + body.lstrip(), encoding="utf-8")
    print(f"Updated {JAVA}")


if __name__ == "__main__":
    main()
