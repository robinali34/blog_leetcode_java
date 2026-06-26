#!/usr/bin/env python3
"""Final Java block cleanups after refix_java_blocks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}


def finalize(code: str) -> str:
    r = code

    r = re.sub(r"return\s+List<[^>]+>\s*\(\s*\)", "return new ArrayList<>()", r)
    r = re.sub(
        r"if\s*\(\s*!(\w+)\.containsKey\(([^)]+)\)\s*\)\s*\1\[(\2)\]\s*=\s*new ArrayList<>\(\)\s*;",
        r"if (!\1.containsKey(\2)) \1.put(\2, new ArrayList<>());",
        r,
    )
    r = re.sub(
        r"(\w+)\[([^\]]+)\]\s*=\s*new ArrayList<>\(\)\s*;",
        r"\1.put(\2, new ArrayList<>());",
        r,
    )
    r = re.sub(
        r"(\w+)\[([^\]]+)\]\s*=\s*([^;]+);",
        r"\1.put(\2, \3);",
        r,
    )
    r = re.sub(
        r"(\w+)\[([^\]]+)\]\.add\(",
        r"\1.computeIfAbsent(\2, k -> new ArrayList<>()).add(",
        r,
    )

    r = re.sub(
        r"(HashMap<[^>]+>|HashSet<[^>]+>|TreeMap<[^>]+>|TreeSet<[^>]+>|"
        r"PriorityQueue<[^>]+>|ArrayDeque<[^>]+>|LinkedList<[^>]+>|ArrayList<[^>]+>)\s+(\w+)\s*;",
        lambda m: f"{m.group(1)} {m.group(2)} = new {m.group(1).split('<')[0]}<>();",
        r,
    )

    # Solution / design class methods need public
    r = re.sub(
        r"(class Solution \{.*?)(\n\s+)((?:static\s+)?(?:boolean|int|long|void|String|double|"
        r"List<|int\[\]|ListNode|TreeNode|char\[\]))",
        r"\1\2public \3",
        r,
        flags=re.S,
    )
    r = re.sub(r"\bpublic\s+public\b", "public", r)

    r = re.sub(r"\.binary search \(lower bound\)", ".lowerBound", r)
    r = re.sub(r"\.binary search \(upper bound\)", ".upperBound", r)
    r = re.sub(r"reverse\s*\(\s*(\w+)\s*/\*[^*]*\*/\s*\)", r"Collections.reverse(Arrays.asList(\1))", r)

    r = re.sub(r"(\w+)\.push_back\s*\(", r"\1.add(", r)
    r = re.sub(r"\bvector<[^>]+>", "List", r)
    r = re.sub(r"\bunordered_map<[^>]+>", "HashMap", r)
    r = re.sub(r"\bunordered_set<[^>]+>", "HashSet", r)

    return r


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + finalize(m.group(2)) + m.group(3)

    updated = JAVA_BLOCK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = sum(1 for p in ROOT.rglob("*.md") if not any(x in SKIP_DIRS for x in p.parts) and process_file(p))
    print(f"Finalized {n} files")


if __name__ == "__main__":
    main()
