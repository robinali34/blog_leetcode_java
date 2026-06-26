#!/usr/bin/env python3
"""Re-apply C++→Java conversion and careful cleanups to all ```java blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from convert_cpp_to_java import convert_cpp_to_java  # noqa: E402

JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}

ARRAY_NAMES = (
    "nums", "strs", "arr", "grid", "board", "intervals", "heights", "values",
    "words", "stones", "points", "edges", "times", "dist", "cost", "prices",
    "ranks", "weights", "targets", "candidates", "tasks", "jobs", "rooms",
    "matrix", "mat", "dp", "prefix", "suffix", "count", "freq", "visited",
    "seen", "parent", "rank", "indegree", "buildings", "ranks", "arr1", "arr2",
)

PYTHON_MARKERS = re.compile(
    r"^\s*#\s|:\s*List\[|self,|self\.|^\s*def\s+\w+\s*\(|//\s*2\b",
    re.M,
)


def extra_fixes(code: str) -> str:
    r = code

    # Containers still in C++ form
    r = re.sub(r"\bvector<\s*String\[\]\s*>", "List<List<String>>", r)
    r = re.sub(r"\bvector<\s*List<\s*String\s*>\s*>", "List<List<String>>", r)
    r = re.sub(r"\bvector<\s*(\w+)\[\]\s*>", r"List<List<\1>>", r)
    r = re.sub(r"\bvector<\s*(\w+)\s*>", r"List<\1>", r)
    r = re.sub(r"\bunordered_map<\s*String\s*,\s*String\[\]\s*>", "HashMap<String, List<String>>", r)
    r = re.sub(r"\bunordered_map<\s*String\s*,\s*List<\s*String\s*>\s*>", "HashMap<String, List<String>>", r)
    r = re.sub(r"\bunordered_map<\s*int\s*,\s*List<\s*Integer\s*>\s*>", "HashMap<Integer, List<Integer>>", r)
    r = re.sub(r"\bunordered_map<\s*(\w+)\s*,\s*(\w+)\s*>", r"HashMap<\1, \2>", r)
    r = re.sub(r"\bunordered_set<\s*(\w+)\s*>", r"HashSet<\1>", r)
    r = re.sub(r"\bmap<\s*(\w+)\s*,\s*(\w+)\s*>", r"TreeMap<\1, \2>", r)
    r = re.sub(r"\bset<\s*(\w+)\s*>", r"TreeSet<\1>", r)
    r = re.sub(r"\bdeque<\s*(\w+)\s*>", r"ArrayDeque<\1>", r)
    r = re.sub(r"\bstack<\s*(\w+)\s*>", r"Deque<\1>", r)
    r = re.sub(r"\bqueue<\s*(\w+)\s*>", r"Queue<\1>", r)
    r = re.sub(r"\blist<\s*(\w+)\s*>", r"LinkedList<\1>", r)
    r = re.sub(r"\bpair<\s*int\s*,\s*int\s*>", "int[]", r)

    r = re.sub(
        r"priority_queue<\s*int\s*,\s*[^>]+>\s+(\w+)\s*;",
        r"PriorityQueue<Integer> \1 = new PriorityQueue<>();",
        r,
    )
    r = re.sub(
        r"priority_queue<\s*int\[\]\s*,\s*[^>]+>\s+(\w+)\s*;",
        r"PriorityQueue<int[]> \1 = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));",
        r,
    )
    r = re.sub(r"priority_queue<\s*(\w+)\s*>", r"PriorityQueue<\1>", r)
    r = re.sub(r"\bgreater<>\s*\(\s*\)", "Comparator.reverseOrder()", r)
    r = re.sub(r"\bgreater<\s*int\s*>\s*\(\s*\)", "Comparator.reverseOrder()", r)

    r = re.sub(r"fill\s*\(\s*begin\s*\(\s*(\w+)\s*\)\s*,\s*end\s*\(\s*\1\s*\)\s*,\s*0\s*\)", r"Arrays.fill(\1, 0)", r)
    r = re.sub(r"\bto_string\s*\(", "String.valueOf(", r)
    r = re.sub(r"\bstoi\s*\(", "Integer.parseInt(", r)
    r = re.sub(r"__builtin_popcount\s*\(", "Integer.bitCount(", r)
    r = re.sub(r"__builtin_clz\s*\(", "Integer.numberOfLeadingZeros(", r)
    r = re.sub(r"__builtin_ctz\s*\(", "Integer.numberOfTrailingZeros(", r)

    r = re.sub(r"(\w+)\.find\(([^)]+)\)\s*!=\s*\1\.end\(\)", r"\1.containsKey(\2)", r)
    r = re.sub(r"(\w+)\.find\(([^)]+)\)\s*==\s*\1\.end\(\)", r"!\1.containsKey(\2)", r)
    r = re.sub(r"!(\w+)\.contains\(([^)]+)\)", r"!\1.containsKey(\2)", r)

    # Map bracket access
    r = re.sub(
        r"(\w+)\[([^\]]+)\]\.push_back\s*\(",
        r"\1.computeIfAbsent(\2, k -> new ArrayList<>()).add(",
        r,
    )
    r = re.sub(
        r"if\s*\(\s*!(\w+)\.containsKey\(([^)]+)\)\s*\)\s*\1\[(\2)\]\s*=\s*new ArrayList<>\(\)\s*;",
        r"if (!\1.containsKey(\2)) \1.put(\2, new ArrayList<>());",
        r,
    )
    r = re.sub(
        r"if\s*\(\s*!(\w+)\.contains\(([^)]+)\)\s*\)\s*\1\[(\2)\]\s*=\s*[^;]+;",
        r"if (!\1.containsKey(\2)) \1.put(\2, new ArrayList<>());",
        r,
    )

    r = re.sub(r"([\w]+)\.push_back\s*\(", r"\1.add(", r)
    r = re.sub(r"([\w]+)\.emplace_back\s*\(", r"\1.add(", r)
    r = re.sub(r"([\w]+)\.pop_back\s*\(\s*\)", r"\1.remove(\1.size() - 1)", r)
    r = re.sub(r"([\w]+)\.top\s*\(\s*\)", r"\1.peek()", r)
    r = re.sub(r"([\w]+)\.substr\s*\(", r"\1.substring(", r)

    r = re.sub(r"(\w+)\.getLast\s*\(\s*\)", r"\1.get(\1.size() - 1)", r)
    r = re.sub(r"(\w+)\.getFirst\s*\(\s*\)", r"\1.get(0)", r)
    r = re.sub(r"(\w+)\.removeLast\s*\(\s*\)", r"\1.remove(\1.size() - 1)", r)

    r = re.sub(r"\bString\[\]\s*\(\s*\)", "new ArrayList<>()", r)
    r = re.sub(r"return\s+vector<[^>]+>\s*\(\s*\)", "return new ArrayList<>()", r)
    r = re.sub(r"return\s+List<[^>]+>\s*\(\s*\)", "return new ArrayList<>()", r)

    r = re.sub(r"public\s+int\s+(\w+)\[(\d+)\]", r"int[] \1 = new int[\2]", r)
    r = re.sub(r"^\s+public\s+(String|int|char|boolean|long|double)\s+(\w+)", r"        \1 \2", r, flags=re.M)

    r = re.sub(r"\barray<\s*int\s*,\s*(\d+)\s*>", "int[]", r)
    r = re.sub(r"\bint\s+(\w+)\[(\d+)\]\s*;", r"int[] \1 = new int[\2];", r)

    for name in ("s", "t", "word", "text", "pattern"):
        r = re.sub(rf"\b{name}\[(\w+)\]", rf"{name}.charAt(\1)", r)

    for name in ARRAY_NAMES:
        r = re.sub(rf"\b{name}\.size\(\)", f"{name}.length", r)
    r = re.sub(r"\b(\w+)\[0\]\.size\(\)", r"\1[0].length", r)

    r = re.sub(r"for\s*\(\s*char\s+c\s*:\s*s\s*\)", "for (char c : s.toCharArray())", r)

    # Broken iterator loops
    r = re.sub(
        r"for\s*\(\s*var\s+\w+\s*=\s*(\w+)\.iterator\(\)\s*;\s*\w+\s*!=\s*\1\.iterator\(\)\s*;\s*\w+\+\+\s*\)\s*\{[^}]*\}",
        r"for (var group : \1.values()) rtn.add(group);",
        r,
        flags=re.S,
    )

    r = re.sub(
        r"(HashMap<[^>]+>|HashSet<[^>]+>|PriorityQueue<[^>]+>|ArrayDeque<[^>]+>|LinkedList<[^>]+>|ArrayList<[^>]+>)\s+(\w+)\s*;",
        lambda m: f"{m.group(1)} {m.group(2)} = new {m.group(1).split('<')[0]}<>();",
        r,
    )
    r = re.sub(
        r"(List<List<String>>|List<List<Integer>>)\s+(\w+)\s*;",
        r"\1 \2 = new ArrayList<>();",
        r,
    )

    r = re.sub(r"^\s*cin\s*>>.*$", "", r, flags=re.M)
    r = re.sub(r"^\s*cout\s*<<.*$", "", r, flags=re.M)
    r = re.sub(r"^\s*#include[^\n]*\n", "", r, flags=re.M)
    r = re.sub(r"Math\.Math\.(max|min)", r"Math.\1", r)
    r = re.sub(r"\bpublic\s+public\b", "public", r)

    return r


def fix_block(body: str) -> str:
    if PYTHON_MARKERS.search(body):
        return body  # leave for manual / separate pass
    body = convert_cpp_to_java(body)
    body = extra_fixes(body)
    return body


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + fix_block(m.group(2)) + m.group(3)

    updated = JAVA_BLOCK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if process_file(path):
            changed += 1
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
