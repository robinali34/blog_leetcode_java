#!/usr/bin/env python3
"""Safe final cleanup pass on ```java blocks — no C++ converter re-run."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK_RE = re.compile(r"(```java\s*\n)(.*?)(```)", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}


def cleanup(code: str) -> str:
    r = code

    # Repeated corruption from bad conversions
    r = re.sub(r"(new int\[\]\s*){2,}", "new int[] ", r)
    r = re.sub(r"(new ArrayList<>\(\)\s*){2,}", "new ArrayList<>() ", r)

    # C++ heap / queue
    r = re.sub(
        r"priority_queue<\s*int\s*,\s*int\[\]\s*,\s*greater<[^>]*>\s*>",
        "PriorityQueue<Integer>",
        r,
    )
    r = re.sub(
        r"priority_queue<\s*int\[\]\s*,\s*List<int\[\]>\s*,\s*greater<int\[\]>\s*>",
        "PriorityQueue<int[]>",
        r,
    )
    r = re.sub(
        r"priority_queue<\s*int\[\]\s*,\s*List<int\[\]>\s*,\s*[^>]+>",
        "PriorityQueue<int[]>",
        r,
    )
    r = re.sub(r"priority_queue<\s*(\w+)\s*>", r"PriorityQueue<\1>", r)
    r = re.sub(r"priority_queue<[^>]+>\s+(\w+)\s*;", r"PriorityQueue<Integer> \1 = new PriorityQueue<>();", r)

    r = re.sub(r"(\w+)\.pop\s*\(\s*\)", r"\1.poll()", r)
    r = re.sub(r"!(\w+)\.length\s*==\s*0", r"!\1.isEmpty()", r)
    r = re.sub(r"!(\w+)\.length\s*>\s*0", r"!\1.isEmpty()", r)

    # C++ containers
    r = re.sub(r"\bvector<\s*(\w+)\s*>", r"List<\1>", r)
    r = re.sub(r"\bunordered_map<\s*(\w+)\s*,\s*(\w+)\s*>", r"HashMap<\1, \2>", r)
    r = re.sub(r"\bunordered_set<\s*(\w+)\s*>", r"HashSet<\1>", r)
    r = re.sub(r"(\w+)\.push_back\s*\(", r"\1.add(", r)
    r = re.sub(r"(\w+)\.emplace_back\s*\(", r"\1.add(", r)
    r = re.sub(r"(\w+)\.empty\s*\(\s*\)", r"\1.isEmpty()", r)
    r = re.sub(r"(\w+)\.reserve\s*\([^)]*\)\s*;?", "", r)

    # Invalid declarations
    r = re.sub(r"HashMap<int,\s*(\w+)>", r"HashMap<Integer, \1>", r)
    r = re.sub(r"LinkedList<int\[\]>", "LinkedList<int[]>", r)
    r = re.sub(r"LinkedList<int\[\]>::iterator", "Iterator<int[]>", r)
    r = re.sub(r"explicit\s+(\w+)\s*\(", r"public \1(", r)
    r = re.sub(r"unique_ptr<(\w+)>", r"\1", r)
    r = re.sub(r"(\w+)\(LRUCache\)\s*=\s*delete\s*;", "", r)
    r = re.sub(r"(\w+)\s+operator=\([^)]+\)\s*=\s*delete\s*;", "", r)

    # Lambdas / comparators
    r = re.sub(r"var\s+\w+\s*=\s*\[\]\([^)]*\)\s*\{[^}]*\}", "", r)
    r = re.sub(r"decltype\([^)]+\)", "", r)
    r = re.sub(r"boolean operator\(\)\([^)]*\)\s*\{[^}]*\}", "", r)
    r = re.sub(r"int dist\(\)\s*\{\s*return\s+x\s+x\s*\+\s*y\s+y\s*;\s*\}", "int distSq() { return x * x + y * y; }", r)

    # Map access
    r = re.sub(r"count_map\[([^\]]+)\]", r"count_map.get(\1)", r)
    r = re.sub(r"cache_\.find\(([^)]+)\)", r"cache_.get(\1)", r)
    r = re.sub(r"cache_\.iterator\(\)", "null", r)
    r = re.sub(r"it\s*==\s*cache_\.iterator\(\)", "it == null", r)
    r = re.sub(r"it\s*!=\s*cache_\.iterator\(\)", "it != null", r)

    # auto destructuring
    r = re.sub(r"auto\s*\[\s*(\w+)\s*,\s*(\w+)\s*\]\s*=\s*(\w+)\.peek\(\)", r"int[] \1pair = \3.peek(); int \1 = \1pair[0]; int \2 = \1pair[1]", r)
    r = re.sub(r"for\s*\(\s*auto&\s*\[\s*(\w+)\s*,\s*(\w+)\s*\]\s*:\s*(\w+)\[(\w+)\]\s*\)", r"for (int[] edge : \3.get(\4))", r)

    # Return / result types
    r = re.sub(r"int\[\]\s*(\w+)\s*;", r"List<Integer> \1 = new ArrayList<>();", r)
    r = re.sub(r"int\[\]\s*(\w+)\s*\(\s*(\w+)\s*\)", r"int[] \1 = new int[\2]", r)
    r = re.sub(r"double\[\]\s*(\w+)\s*;", r"List<Double> \1 = new ArrayList<>();", r)
    r = re.sub(r"int\[\]\[\]\s*(\w+)\s*;", r"List<int[]> \1 = new ArrayList<>();", r)

    # Method signatures
    r = re.sub(r"int\[\]find", "int[] find", r)
    r = re.sub(r"int\[\]\s+find", "int[] find", r)
    r = re.sub(r"double\[\]median", "double[] median", r)
    r = re.sub(r"ListNode\[\]\s*&", "ListNode[]", r)
    r = re.sub(r"int\[\]\[\]\s*&", "int[][]", r)

    # Misc C++
    r = re.sub(r"using\s+T\s*=\s*[^;]+;", "", r)
    r = re.sub(r"multiset<[^>]+>", "TreeMap<Integer, Integer>", r)
    r = re.sub(r"binary search \(lower bound\)", "floorKey", r)
    r = re.sub(r"rand\s*\(\s*\)", "new Random().nextInt()", r)
    r = re.sub(r"swap\s*\(\s*(\w+)\[([^\]]+)\]\s*,\s*\1\[([^\]]+)\]\s*\)", r"swap(\1, \2, \3)", r)

    # Fix broken getOrDefault missing paren
    r = re.sub(
        r"getOrDefault\(([^,]+),\s*([^)]+)\s*;",
        r"getOrDefault(\1, \2));",
        r,
    )

    # C++ brace initialization
    r = re.sub(
        r'HashSet<String>\s+(\w+)\s*=\s*\{([^}]+)\}',
        r'Set<String> \1 = Set.of(\2)',
        r,
    )
    r = re.sub(r'constexpr\s+array<[^>]+>\s+\w+\s*=', 'int[][] dirs =', r)
    r = re.sub(r'for\s*\(\s*auto\s+(\w+)\s*:\s*(\w+)\[(\w+)\]\s*\)', r'for (char \1 : \2[\3].toCharArray())', r)
    r = re.sub(r'(\w+)\s+(\w+)\s*=\s*(\w+)\s*;\s*//', r'\2 = \3; //', r)
    r = re.sub(r'public\s+(ListNode|TreeNode|int|void)\s+(\w+)\s*=', r'\1 \2 =', r)
    r = re.sub(r'(\w+)\s+(\w+)\(([^)]+)\)\s*;', r'\1 \2 = new \1(\3);', r)
    r = re.sub(r'half\s+half', 'half * half', r)
    r = re.sub(r'while\s*\(\s*(\w+)\s*\)\s*\{', r'while (\1 > 0) {', r)

    return r


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        fixed = cleanup(m.group(2))
        return m.group(1) + fixed + m.group(3)

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
    print(f"Cleaned {changed} files")


if __name__ == "__main__":
    main()
