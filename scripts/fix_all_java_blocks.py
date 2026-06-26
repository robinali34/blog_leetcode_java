#!/usr/bin/env python3
"""Single-pass Java block repair: convert C++ remnants to valid Java."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from convert_cpp_to_java import convert_cpp_to_java  # noqa: E402

JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}
PYTHON_MARKERS = re.compile(r"^\s*#\s|:\s*List\[|self,|self\.|^\s*def\s+\w+\s*\(", re.M)
CPP_MARKERS = re.compile(
    r"vector<|unordered_map|unordered_set|push_back|emplace_back|begin\(|end\(|"
    r"to_string\(|priority_queue|__builtin_|nullptr|cin >>|#include|pair<|greater<",
)

ARRAY_NAMES = (
    "nums", "strs", "arr", "grid", "board", "intervals", "heights", "values",
    "words", "stones", "points", "edges", "times", "dist", "cost", "prices",
    "matrix", "mat", "dp", "prefix", "suffix", "count", "freq", "visited", "seen",
)

GENERIC_DECL = (
    r"(?:HashMap|HashSet|ArrayList|PriorityQueue|ArrayDeque|LinkedList|"
    r"TreeMap|TreeSet)<(?:[^<>]|<[^<>]*>)*>"
)


def repair(code: str) -> str:
    if PYTHON_MARKERS.search(code):
        return code

    r = code
    for _ in range(2):
        prev = r
        if CPP_MARKERS.search(r):
            r = convert_cpp_to_java(r)
        r = apply_java_fixes(r)
        if r == prev:
            break
    return r


def apply_java_fixes(code: str) -> str:
    r = code

    # Containers
    r = re.sub(r"\bvector<\s*String\[\]\s*>", "List<List<String>>", r)
    r = re.sub(r"\bvector<\s*List<\s*String\s*>\s*>", "List<List<String>>", r)
    r = re.sub(r"\bvector<\s*(\w+)\[\]\s*>", r"List<List<\1>>", r)
    r = re.sub(r"\bvector<\s*(\w+)\s*>", r"List<\1>", r)
    r = re.sub(r"\bunordered_map<\s*String\s*,\s*String\[\]\s*>", "HashMap<String, List<String>>", r)
    r = re.sub(r"\bunordered_map<\s*(\w+)\s*,\s*(\w+)\s*>", r"HashMap<\1, \2>", r)
    r = re.sub(r"\bunordered_set<\s*(\w+)\s*>", r"HashSet<\1>", r)
    r = re.sub(r"\bpair<\s*int\s*,\s*int\s*>", "int[]", r)

    r = re.sub(
        r"priority_queue<\s*int\s*,\s*[^>]+>\s+(\w+)\s*;",
        r"PriorityQueue<Integer> \1 = new PriorityQueue<>();",
        r,
    )
    r = re.sub(r"priority_queue<\s*(\w+)\s*>", r"PriorityQueue<\1>", r)
    r = re.sub(r"\bgreater<>\s*\(\s*\)", "Comparator.reverseOrder()", r)

    r = re.sub(r"fill\s*\(\s*begin\s*\(\s*(\w+)\s*\)\s*,\s*end\s*\(\s*\1\s*\)\s*,\s*0\s*\)", r"Arrays.fill(\1, 0)", r)
    r = re.sub(r"\bto_string\s*\(", "String.valueOf(", r)
    r = re.sub(r"\bstoi\s*\(", "Integer.parseInt(", r)
    r = re.sub(r"__builtin_\w+\s*\(", "Integer.bitCount(", r)

    r = re.sub(r"(\w+)\.find\(([^)]+)\)\s*!=\s*\1\.end\(\)", r"\1.containsKey(\2)", r)
    r = re.sub(r"!(\w+)\.contains\(([^)]+)\)", r"!\1.containsKey(\2)", r)

    r = re.sub(
        r"(\w+)\[([^\]]+)\]\.push_back\s*\(",
        r"\1.computeIfAbsent(\2, k -> new ArrayList<>()).add(",
        r,
    )
    r = re.sub(r"([\w]+)\.push_back\s*\(", r"\1.add(", r)
    r = re.sub(r"([\w]+)\.top\s*\(\s*\)", r"\1.peek()", r)
    r = re.sub(r"([\w]+)\.substr\s*\(", r"\1.substring(", r)
    r = re.sub(r"(\w+)\.getLast\s*\(\s*\)", r"\1.get(\1.size() - 1)", r)
    r = re.sub(r"(\w+)\.getFirst\s*\(\s*\)", r"\1.get(0)", r)

    r = re.sub(r"\bString\[\]\s*\(\s*\)", "new ArrayList<>()", r)
    r = re.sub(r"return\s+vector<[^>]+>\s*\(\s*\)", "return new ArrayList<>()", r)
    r = re.sub(r"return\s+List<(?:[^<>]|<[^<>]*>)*>\s*\(\s*\)", "return new ArrayList<>()", r)

    r = re.sub(r"public\s+int\s+(\w+)\[(\d+)\]", r"int[] \1 = new int[\2]", r)

    for name in ("s", "t", "word", "text"):
        r = re.sub(rf"\b{name}\[(\w+)\]", rf"{name}.charAt(\1)", r)
    for name in ARRAY_NAMES:
        r = re.sub(rf"\b{name}\.size\(\)", f"{name}.length", r)

    r = re.sub(r"for\s*\(\s*char\s+c\s*:\s*s\s*\)", "for (char c : s.toCharArray())", r)

    r = re.sub(
        r"for\s*\(\s*var\s+\w+\s*=\s*(\w+)\.iterator\(\)\s*;\s*\w+\s*!=\s*\1\.iterator\(\)\s*;\s*\w+\+\+\s*\)\s*\{[^}]*\}",
        r"for (var group : \1.values()) rtn.add(group);",
        r,
        flags=re.S,
    )

    r = re.sub(
        rf"\b({GENERIC_DECL})\s+(\w+)\s*;",
        lambda m: f"{m.group(1)} {m.group(2)} = new {m.group(1).split('<')[0]}<>();",
        r,
    )
    r = re.sub(
        r"(List<List<String>>|List<List<Integer>>)\s+(\w+)\s*;",
        r"\1 \2 = new ArrayList<>();",
        r,
    )
    r = re.sub(r"\bnew List<>\(\)", "new ArrayList<>()", r)

    r = re.sub(
        r"if\s*\(\s*!(\w+)\.containsKey\(([^)]+)\)\s*\)\s*\1\[(\2)\]\s*=\s*new ArrayList<>\(\)\s*;",
        r"if (!\1.containsKey(\2)) \1.put(\2, new ArrayList<>());",
        r,
    )
    r = re.sub(
        r"if\s*\(\s*!(\w+)\.containsKey\(([^)]+)\)\s*\)\s*\1\.put\(\2, new ArrayList<>\(\)\);\s*\n\s*\1\.computeIfAbsent\(\2, k -> new ArrayList<>\(\)\)\.add\(",
        r"\1.computeIfAbsent(\2, k -> new ArrayList<>()).add(",
        r,
    )

    r = re.sub(r"for\s*\(\s*auto\s+(\w+)\s*:\s*(\w+)\s*\)", r"for (int \1 : \2)", r)
    r = re.sub(
        r"for\s*\(\s*auto\s*&\s*\[\s*(\w+)\s*,\s*(\w+)\s*\]\s*:\s*(\w+)\s*\)",
        r"for (var e : \3.entrySet())",
        r,
    )
    r = re.sub(r"\b(\w+)\.first\b", r"\1[0]", r)
    r = re.sub(r"\b(\w+)\.second\b", r"\1[1]", r)
    r = re.sub(r"\{(\w+),\s*(\w+)\}", r"new int[] {\1, \2}", r)
    r = re.sub(r"(\w+)\.push\s*\(", r"\1.offer(", r)
    r = re.sub(r"(\w+)\[(\w+)\]\s*\+=\s*", r"\1.put(\2, \1.getOrDefault(\2, 0) + ", r)
    r = re.sub(
        r"int\[\]\[\]\s+(\w+)\s*\(\s*(\w+)\s*\+\s*1\s*\)",
        r"List<List<Integer>> \1 = new ArrayList<>(\2 + 1)",
        r,
    )
    r = re.sub(r"int\[\]\s+(\w+)\s*\(\s*(\w+)\s*\)", r"int[] \1 = new int[\2]", r)
    r = re.sub(r"int\[\]\s+(\w+)\s*;", r"List<Integer> \1 = new ArrayList<>();", r)
    r = re.sub(r"for\s*\(\s*int\s+(\w+)\s*:\s*buckets\[(\w+)\]\s*\)", r"for (int \1 : buckets.get(\2))", r)
    r = re.sub(
        r"priority_queue<[^>]+>\s+(\w+)\s*;",
        r"PriorityQueue<int[]> \1 = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));",
        r,
    )
    r = re.sub(r"public int\[\](\w+)", r"public int[] \1", r)
    r = re.sub(r"Comparator\.(\w+)Order\(\)", r"Comparator.\1Order()", r)
    r = re.sub(r"Math\.Math\.(max|min)", r"Math.\1", r)
    r = re.sub(r"\bpublic\s+public\b", "public", r)

    r = re.sub(r"^\s+public (String|int|char|boolean|long|double|var) ", r"        \1 ", r, flags=re.M)

    # Ensure public on Solution / design-class methods
    lines = r.split("\n")
    out: list[str] = []
    in_class = False
    brace = 0
    for line in lines:
        if re.match(r"\s*class\s+(Solution|Trie|LRUCache|MinStack|FooBar|WordDictionary)\b", line):
            in_class = True
            brace = line.count("{") - line.count("}")
            out.append(line)
            continue
        if in_class:
            brace += line.count("{") - line.count("}")
            if brace <= 0:
                in_class = False
            elif re.match(
                r"^(\s+)((?:public\s+)?(?:static\s+)?"
                r"(?:boolean|int|long|void|String|double|List(?:<[^>]+>)+|int\[\]|ListNode|TreeNode)\s+\w+\s*\()",
                line,
            ) and "public " not in line:
                line = re.sub(r"^(\s+)", r"\1public ", line, count=1)
        out.append(line)
    r = "\n".join(out)

    return r


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + repair(m.group(2)) + m.group(3)

    updated = JAVA_BLOCK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = sum(
        1 for p in ROOT.rglob("*.md")
        if not any(x in SKIP_DIRS for x in p.parts) and process_file(p)
    )
    print(f"Repaired {changed} files")


if __name__ == "__main__":
    main()
