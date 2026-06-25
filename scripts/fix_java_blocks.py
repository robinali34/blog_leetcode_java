#!/usr/bin/env python3
"""Second-pass cleanup for converted Java code blocks."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)


def fix_java(code: str) -> str:
    r = code
    r = re.sub(r"\bvector<\s*int\[\]\s*>", "List<int[]>", r)
    r = re.sub(r"\bvector<\s*pair<[^>]+>\s*>", "List<int[]>", r)
    r = re.sub(r"\bvector<\s*(\w+)\s*>", r"\1[]", r)
    r = re.sub(r"\bunordered_map<\s*int\s*,\s*int\[\]\s*>", "HashMap<Integer, int[]>", r)
    r = re.sub(r"\bunordered_map<\s*int\s*,\s*List<\s*Integer\s*>\s*>", "HashMap<Integer, List<Integer>>", r)
    r = re.sub(r"\bunordered_map<\s*int\s*,\s*int\s*>", "HashMap<Integer, Integer>", r)
    r = re.sub(r"\bunordered_map<\s*String\s*,\s*int\s*>", "HashMap<String, Integer>", r)
    r = re.sub(r"\bunordered_map<\s*(\w+)\s*,\s*(\w+)\s*>", r"HashMap<\1, \2>", r)
    r = re.sub(r"\bunordered_set<\s*(\w+)\s*>", r"HashSet<\1>", r)
    r = re.sub(r"\bnullptr\b", "null", r)
    r = re.sub(r"->", ".", r)
    r = re.sub(r"\bNode\s*\*", "Node", r)
    r = re.sub(r"\bListNode\s*\*", "ListNode", r)
    r = re.sub(r"\bTreeNode\s*\*", "TreeNode", r)
    r = re.sub(r"(\w+)\.begin\(\)\s*,\s*\1\.end\(\)", r"\1", r)
    r = re.sub(r"(\w+)\.begin\(\)", r"\1.iterator()", r)
    r = re.sub(r"(\w+)\.end\(\)", r"\1.iterator()", r)
    r = re.sub(r"\bmax\s*\(", "Math.max(", r)
    r = re.sub(r"\bmin\s*\(", "Math.min(", r)
    r = re.sub(r"Math\.Math\.(max|min)", r"Math.\1", r)
    return r


def main() -> None:
    changed = 0
    for path in ROOT.glob("**/*.md"):
        if "scripts" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            fixed = fix_java(m.group(2))
            return m.group(1) + fixed + m.group(3)

        updated = JAVA_BLOCK_RE.sub(repl, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Fixed Java blocks in {changed} files")


if __name__ == "__main__":
    main()
