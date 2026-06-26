#!/usr/bin/env python3
"""Convert C++ code blocks in markdown/HTML to Java for blog_leetcode_java."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CODE_BLOCK_RE = re.compile(
    r"(```)(cpp|c\+\+|python)(\s*\n)(.*?)(```)",
    re.DOTALL | re.IGNORECASE,
)


def convert_cpp_to_java(code: str) -> str:
    result = code

    # Remove includes / using
    result = re.sub(r"^\s*#include[^\n]*\n", "", result, flags=re.M)
    result = re.sub(r"^\s*using\s+namespace\s+std\s*;\s*\n", "", result, flags=re.M)

    # Access specifiers and destructors
    result = re.sub(r"^\s*(public|private|protected)\s*:\s*\n", "", result, flags=re.M)
    result = re.sub(r"^\s*~\w+\s*\([^)]*\)\s*(\{[^}]*\})?\s*\n", "", result, flags=re.M)

    # Constructor initializer lists
    result = re.sub(
        r"(\w+)\s*\(\s*\)\s*:\s*children\s*\(\s*26\s*\)\s*,\s*isWord\s*\(\s*false\s*\)\s*\{",
        r"\1() { children = new Trie[26]; isWord = false;",
        result,
    )
    result = re.sub(
        r"(\w+)\s*\(([^)]*)\)\s*:\s*val\(([^)]*)\),\s*next\(nullptr\)\s*\{\s*\}",
        r"\1(\2) { this.val = \3; this.next = null; }",
        result,
    )
    result = re.sub(
        r"(\w+)\s*\(([^)]*)\)\s*:\s*val\(([^)]*)\),\s*next\(([^)]*)\)\s*\{\s*\}",
        r"\1(\2) { this.val = \3; this.next = \4; }",
        result,
    )
    result = re.sub(
        r"(\w+)\s*\(\s*\)\s*:\s*val\(0\),\s*next\(nullptr\)\s*\{\s*\}",
        r"\1() { this.val = 0; this.next = null; }",
        result,
    )
    result = re.sub(
        r"(\w+)\s*\(([^)]*)\)\s*:\s*[^{]+\{",
        lambda m: f"{m.group(1)}({m.group(2)}) {{",
        result,
    )

    # struct -> class
    result = re.sub(r"\bstruct\b", "class", result)

    # Primitive / literal types
    result = re.sub(r"\blong\s+long\b", "long", result)
    result = re.sub(r"\bunsigned\s+long\s+long\b", "long", result)
    result = re.sub(r"\bunsigned\s+int\b", "int", result)
    result = re.sub(r"\bunsigned\b", "int", result)
    result = re.sub(r"\bbool\b", "boolean", result)
    result = re.sub(r"\bnullptr\b", "null", result)
    result = re.sub(r"\bINT_MAX\b", "Integer.MAX_VALUE", result)
    result = re.sub(r"\bINT_MIN\b", "Integer.MIN_VALUE", result)
    result = re.sub(r"\bLLONG_MAX\b", "Long.MAX_VALUE", result)
    result = re.sub(r"\bLLONG_MIN\b", "Long.MIN_VALUE", result)
    result = re.sub(r"__builtin_popcount\s*\(", "Integer.bitCount(", result)

    # Nested containers first
    result = re.sub(r"\bvector<\s*vector<\s*vector<\s*int\s*>\s*>\s*>", "int[][][]", result)
    result = re.sub(r"\bvector<\s*vector<\s*int\s*>\s*>", "int[][]", result)
    result = re.sub(r"\bvector<\s*vector<\s*String\s*>\s*>", "String[][]", result)
    result = re.sub(r"\bvector<\s*vector<\s*char\s*>\s*>", "char[][]", result)
    result = re.sub(r"\bvector<\s*vector<\s*long\s*>\s*>", "long[][]", result)
    result = re.sub(r"\bvector<\s*vector<\s*boolean\s*>\s*>", "boolean[][]", result)
    result = re.sub(r"\bvector<\s*ListNode\s*\*\s*>", "ListNode[]", result)
    result = re.sub(r"\bvector<\s*TreeNode\s*\*\s*>", "TreeNode[]", result)
    result = re.sub(r"\bvector<\s*Trie\s*\*\s*>", "Trie[]", result)
    result = re.sub(r"\bvector<\s*String\s*>\s*&?", "String[]", result)
    result = re.sub(r"\bvector<\s*char\s*>\s*&?", "char[]", result)
    result = re.sub(r"\bvector<\s*boolean\s*>\s*&?", "boolean[]", result)
    result = re.sub(r"\bvector<\s*long\s*>\s*&?", "long[]", result)
    result = re.sub(r"\bvector<\s*double\s*>\s*&?", "double[]", result)
    result = re.sub(r"\bvector<\s*int\s*>\s*&?", "int[]", result)
    result = re.sub(r"\bvector<\s*(\w+)\s*>\s*&?", r"\1[]", result)

    result = re.sub(r"\bunordered_set<\s*String\s*>", "HashSet<String>", result)
    result = re.sub(r"\bunordered_set<\s*int\s*>", "HashSet<Integer>", result)
    result = re.sub(r"\bunordered_set<\s*long\s*>", "HashSet<Long>", result)
    result = re.sub(r"\bunordered_set<\s*(\w+)\s*>", r"HashSet<\1>", result)

    result = re.sub(r"\bunordered_map<\s*int\s*,\s*list<\s*int\s*>\s*>", "HashMap<Integer, LinkedList<Integer>>", result)
    result = re.sub(r"\bunordered_map<\s*int\s*,\s*vector<\s*int\s*>\s*>", "HashMap<Integer, List<Integer>>", result)
    result = re.sub(r"\bunordered_map<\s*int\s*,\s*int\s*>", "HashMap<Integer, Integer>", result)
    result = re.sub(r"\bunordered_map<\s*String\s*,\s*int\s*>", "HashMap<String, Integer>", result)
    result = re.sub(r"\bunordered_map<\s*String\s*,\s*String\s*>", "HashMap<String, String>", result)
    result = re.sub(r"\bunordered_map<\s*(\w+)\s*,\s*(\w+)\s*>", r"HashMap<\1, \2>", result)

    result = re.sub(r"\bmap<\s*int\s*,\s*int\s*>", "TreeMap<Integer, Integer>", result)
    result = re.sub(r"\bmap<\s*(\w+)\s*,\s*(\w+)\s*>", r"TreeMap<\1, \2>", result)
    result = re.sub(r"\bset<\s*int\s*>", "TreeSet<Integer>", result)
    result = re.sub(r"\bset<\s*String\s*>", "TreeSet<String>", result)
    result = re.sub(r"\bset<\s*(\w+)\s*>", r"TreeSet<\1>", result)
    result = re.sub(r"\blist<\s*int\s*>", "LinkedList<Integer>", result)
    result = re.sub(r"\blist<\s*pair<\s*int\s*,\s*int\s*>\s*>", "LinkedList<int[]>", result)
    result = re.sub(r"\blist<\s*(\w+)\s*>", r"LinkedList<\1>", result)
    result = re.sub(r"\bdeque<\s*int\s*>", "ArrayDeque<Integer>", result)
    result = re.sub(r"\bdeque<\s*(\w+)\s*>", r"ArrayDeque<\1>", result)
    result = re.sub(r"\bqueue<\s*int\s*>", "Queue<Integer>", result)
    result = re.sub(r"\bqueue<\s*(\w+)\s*>", r"Queue<\1>", result)
    result = re.sub(r"\bstack<\s*int\s*>", "Deque<Integer>", result)
    result = re.sub(r"\bstack<\s*(\w+)\s*>", r"Deque<\1>", result)
    result = re.sub(
        r"\bpriority_queue<\s*pair<\s*int\s*,\s*int\s*>\s*,\s*vector<\s*pair<\s*int\s*,\s*int\s*>\s*>\s*,\s*greater<>\s*>",
        "PriorityQueue<int[]>",
        result,
    )
    result = re.sub(r"\bpriority_queue<\s*int\s*>", "PriorityQueue<Integer>", result)
    result = re.sub(r"\bpriority_queue<\s*(\w+)\s*>", r"PriorityQueue<\1>", result)

    result = re.sub(r"\bpair<\s*int\s*,\s*int\s*>", "int[]", result)
    result = re.sub(r"\bpair<\s*(\w+)\s*,\s*(\w+)\s*>", r"\1[]", result)
    result = re.sub(r"\bmake_pair\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)", r"new int[] {\1, \2}", result)

    result = re.sub(r"\bstring\b", "String", result)
    # Pointer types — preserve word boundary between type and field name
    result = re.sub(r"\b(ListNode|TreeNode|Trie|Node)\s*\*\s*(\w+)", r"\1 \2", result)
    result = re.sub(r"\b(\w+)\s*\*\s*(\w+)\b", r"\1 \2", result)

    # const / references
    result = re.sub(r"\bconst\s+", "", result)
    result = re.sub(r"(\w[\]\w]*)\s*&\s*(\w+)", r"\1 \2", result)
    result = re.sub(r"(\w)\s*&\s*\)", r"\1)", result)
    result = re.sub(r"(\w)\s*&\s*,", r"\1,", result)

    result = re.sub(r"\bstd::", "", result)
    # C++ pointer member access only — preserve Java lambda arrows (x -> y)
    result = re.sub(r"(\w+)\s*->\s*(\w+)", r"\1.\2", result)

    # Vector / array initialization patterns
    result = re.sub(
        r"int\[\]\s*(\w+)\s*\(\s*(\w+)\s*\+\s*1\s*,\s*0\s*\)",
        r"int[] \1 = new int[\2 + 1]",
        result,
    )
    result = re.sub(
        r"int\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*0\s*\)",
        r"int[] \1 = new int[\2]",
        result,
    )
    result = re.sub(
        r"int\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)",
        r"int[] \1 = new int[\2]",
        result,
    )
    result = re.sub(
        r"long\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*0\s*\)",
        r"long[] \1 = new long[\2]",
        result,
    )
    result = re.sub(
        r"boolean\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*false\s*\)",
        r"boolean[] \1 = new boolean[\2]",
        result,
    )
    result = re.sub(
        r"int\[\]\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*int\[\]\s*\(\s*(\w+)\s*,\s*0\s*\)\s*\)",
        r"int[][] \1 = new int[\2][\3]",
        result,
    )
    result = re.sub(
        r"int\[\]\[\]\s*(\w+)\s*\(\s*(\w+)\s*,\s*vector<\s*int\s*>\s*\(\s*(\w+)\s*,\s*0\s*\)\s*\)",
        r"int[][] \1 = new int[\2][\3]",
        result,
    )
    result = re.sub(
        r"Trie\[\]\s+children\s*=\s*new\s+Trie\[26\]",
        "Trie[] children = new Trie[26]",
        result,
    )
    result = re.sub(
        r"vector<\s*Trie\s*>\s+children\s*\(\s*26\s*\)",
        "Trie[] children = new Trie[26]",
        result,
    )

    # Iterator / algorithm patterns
    result = re.sub(
        r"sort\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*,\s*greater<>\(\)\s*\)",
        r"Arrays.sort(\1, Collections.reverseOrder())",
        result,
    )
    result = re.sub(
        r"sort\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*\)",
        r"Arrays.sort(\1)",
        result,
    )
    result = re.sub(
        r"\*\s*max_element\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*\)",
        r"Arrays.stream(\1).max().getAsInt()",
        result,
    )
    result = re.sub(
        r"\*\s*min_element\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*\)",
        r"Arrays.stream(\1).min().getAsInt()",
        result,
    )
    result = re.sub(
        r"return\s+unordered_set<int>\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*\)\.size\(\)\s*!=\s*(\w+)\.size\(\)",
        r"return IntStream.of(\1).distinct().count() != \2.length",
        result,
    )
    result = re.sub(
        r"unordered_set<int>\s*\(\s*(\w+)\.begin\(\)\s*,\s*\1\.end\(\)\s*\)",
        r"Arrays.stream(\1).boxed().collect(Collectors.toCollection(HashSet::new))",
        result,
    )

    # Container methods
    result = re.sub(r"(\w+)\.push_back\s*\(", r"\1.add(", result)
    result = re.sub(r"(\w+)\.emplace_back\s*\(", r"\1.add(", result)
    result = re.sub(r"(\w+)\.pop_back\s*\(\s*\)", r"\1.removeLast()", result)
    result = re.sub(r"(\w+)\.back\s*\(\s*\)", r"\1.getLast()", result)
    result = re.sub(r"(\w+)\.front\s*\(\s*\)", r"\1.getFirst()", result)
    result = re.sub(r"(\w+)\.pop_front\s*\(\s*\)", r"\1.removeFirst()", result)
    result = re.sub(r"(\w+)\.empty\s*\(\s*\)", r"\1.isEmpty()", result)
    result = re.sub(r"(\w+)\.contains\s*\(", r"\1.contains(", result)
    result = re.sub(r"(\w+)\.insert\s*\(", r"\1.add(", result)
    result = re.sub(r"(\w+)\.erase\s*\(", r"\1.remove(", result)
    result = re.sub(r"(\w+)\.splice\s*\([^)]+\)", r"/* move to end */", result)
    result = re.sub(r"--(\w+)\.end\(\)", r"\1.getLast()", result)

    # auto
    result = re.sub(r"\bauto\s+&\s*(\w+)\s*=", r"var \1 =", result)
    result = re.sub(r"\bauto\s+(\w+)\s*=", r"var \1 =", result)

    # map access ++
    result = re.sub(
        r"(\w+)\[(\w+)\]\+\+;",
        r"\1.put(\2, \1.getOrDefault(\2, 0) + 1);",
        result,
    )
    result = re.sub(
        r"if\s*\(\s*(\w+)\[(\w+)\]\s*>\s*1\s*\)",
        r"if (\1.getOrDefault(\2, 0) > 1)",
        result,
    )
    result = re.sub(
        r"(\w+)\[(\w+)\]\s*=\s*([^;]+);",
        lambda m: (
            f"{m.group(1)}.put({m.group(2)}, {m.group(3)});"
            if re.search(r"HashMap|TreeMap", result[: result.find(m.group(0)) + 200])
            else m.group(0)
        ),
        result,
    )

    # max/min functions
    result = re.sub(r"(?<![.\w])max\s*\(", "Math.max(", result)
    result = re.sub(r"(?<![.\w])min\s*\(", "Math.min(", result)

    # .size() on arrays / common 2D arrays
    for name in ("nums", "wt", "val", "dp", "g", "grid", "words", "intervals", "heights"):
        result = re.sub(rf"\b{name}\.size\(\)", f"{name}.length", result)
    result = re.sub(r"\b(\w+)\[0\]\.size\(\)", r"\1[0].length", result)
    result = re.sub(r"\(int\)\s*(\w+)\.length", r"\1.length", result)

    # Collection initialization
    result = re.sub(
        r"(HashSet<\w+>)\s+(\w+)\s*;",
        r"\1 \2 = new \1();",
        result,
    )
    result = re.sub(
        r"(HashMap<[^>]+>)\s+(\w+)\s*;",
        r"\1 \2 = new \1();",
        result,
    )
    result = re.sub(
        r"(PriorityQueue<[^>]+>)\s+(\w+)\s*;",
        r"\1 \2 = new \1();",
        result,
    )
    result = re.sub(
        r"(Deque<[^>]+>)\s+(\w+)\s*;",
        r"\1 \2 = new ArrayDeque<>();",
        result,
    )
    result = re.sub(
        r"(Queue<[^>]+>)\s+(\w+)\s*;",
        r"\1 \2 = new LinkedList<>();",
        result,
    )
    result = re.sub(
        r"(LinkedList<[^>]+>)\s+(\w+)\s*;",
        r"\1 \2 = new \1();",
        result,
    )

    # Concurrency -> Java
    result = re.sub(r"\bmutex\b", "lock", result)
    result = re.sub(r"\bcondition_variable\b", "Condition", result)
    result = re.sub(r"\bReentrantLock\s+lock\b", "ReentrantLock lock = new ReentrantLock()", result)
    result = re.sub(
        r"unique_lock<\s*ReentrantLock\s*>\s+(\w+)\s*\(\s*lock\s*\)\s*;",
        r"\1 = lock;",
        result,
    )
    result = re.sub(
        r"cv\.wait\s*\(\s*(\w+)\s*,\s*\[this\]\(\)\s*\{\s*return\s+([^;]+);\s*\}\s*\)\s*;",
        r"while (!(\2)) { cv.await(); }",
        result,
    )
    result = re.sub(r"cv\.notify_all\s*\(\s*\)", "cv.signalAll()", result)
    result = re.sub(r"\bfunction<void\(\)>\s+(\w+)", r"Runnable \1", result)
    result = re.sub(r"\bcounting_semaphore\b", "Semaphore", result)
    result = re.sub(r"\bbinary_semaphore\b", "Semaphore", result)
    result = re.sub(r"Semaphore\s+(\w+)\{(\d+)\}", r"Semaphore \1 = new Semaphore(\2)", result)

    # Boolean ops
    result = re.sub(r"(\w+)\s*!=\s*null\s*&\s*(\w+)", r"\1 != null && \2", result)
    result = re.sub(r"(\w+)\s*==\s*null\s*\|\s*(\w+)", r"\1 == null || \2", result)

    # Add public to class methods and fields (not local variables)
    lines = result.split("\n")
    out_lines: list[str] = []
    in_class = False
    depth = 0
    method_depth = 0
    for line in lines:
        stripped = line.strip()
        if re.match(r"^class\s+\w+", stripped):
            in_class = True
            depth = stripped.count("{") - stripped.count("}")
            method_depth = 0
        elif in_class:
            if "{" in line:
                if method_depth == 0 and re.search(r"\)\s*\{", line):
                    method_depth = depth + line.count("{") - line.count("}")
                elif method_depth > 0:
                    method_depth += line.count("{") - line.count("}")
            depth += line.count("{") - line.count("}")
            if "}" in line and method_depth > 0:
                method_depth = max(0, method_depth + line.count("}") - line.count("{"))
            if depth <= 0:
                in_class = False
                method_depth = 0

        at_class_level = in_class and method_depth == 0
        if at_class_level and re.match(
            r"^(\s+)((?:static\s+)?(?:boolean|int|long|double|void|String|ListNode|TreeNode|Trie|HashMap|HashSet|LinkedList|PriorityQueue|Deque|Queue|ReentrantLock|Condition|Semaphore|int\[\]|int\[\]\[\]|String\[\]|Trie\[\])\s+\w+)",
            line,
        ):
            if "public " not in line and "private " not in line and "(" not in line.split("=")[0]:
                line = re.sub(
                    r"^(\s+)((?:static\s+)?(?:boolean|int|long|double|void|String|ListNode|TreeNode|Trie|HashMap|HashSet|LinkedList|PriorityQueue|Deque|Queue|ReentrantLock|Condition|Semaphore|int\[\]|int\[\]\[\]|String\[\]|Trie\[\])\s+)",
                    r"\1public \2",
                    line,
                )
        if at_class_level and re.match(
            r"^(\s+)((?:static\s+)?(?:boolean|int|long|double|void|String|ListNode|TreeNode|Trie)\s+\w+\s*\()",
            line,
        ):
            if "public " not in line:
                line = re.sub(
                    r"^(\s+)((?:static\s+)?(?:boolean|int|long|double|void|String|ListNode|TreeNode|Trie)\s+)",
                    r"\1public \2",
                    line,
                )
        if at_class_level and re.match(r"^(\s+)(\w+)\s*\(([^)]*)\)\s*\{", line):
            name = re.match(r"^(\s+)(\w+)\s*\(", line).group(2)
            if name[0].isupper() and "public " not in line:
                line = re.sub(r"^(\s+)(\w+)\s*\(", r"\1public \2(", line)

        out_lines.append(line.rstrip())
    result = "\n".join(out_lines)

    # Standalone top-level functions
    if re.search(r"^\s*(int|boolean|void|String|long|double)\s+\w+\s*\(", result, re.M):
        if not re.search(r"^\s*class\s+", result, re.M):
            result = re.sub(
                r"^(\s*)((?:int|boolean|void|String|long|double)\s+\w+\s*\()",
                r"\1static \2",
                result,
                flags=re.M,
            )

    # Trailing C++ class semicolon
    result = re.sub(r"\};\s*$", "}", result, flags=re.M)
    result = re.sub(r"\};\s*\n", "}\n", result)

    # Cleanup leftovers
    result = cleanup_java(result)

    # Import hints
    imports: list[str] = []
    if re.search(r"\b(Arrays|Collections)\b", result):
        imports.append("java.util.Arrays")
        imports.append("java.util.Collections")
    if re.search(r"\b(HashMap|HashSet|LinkedList|PriorityQueue|ArrayDeque|Queue|Deque|TreeMap|TreeSet|List)\b", result):
        imports.append("java.util.*")
    if re.search(r"\b(IntStream|Collectors)\b", result):
        imports.append("java.util.stream.*")
    if re.search(r"\b(ReentrantLock|Condition|Semaphore)\b", result):
        imports.append("java.util.concurrent.*")
    if imports:
        header = "\n".join(f"// import {imp};" for imp in sorted(set(imports)))
        if not result.startswith("// import"):
            result = header + "\n" + result

    return result.strip() + "\n"


def cleanup_java(code: str) -> str:
    result = code

    # Fix merged identifiers from bad pointer conversion
    result = re.sub(r"\bListNodenext\b", "ListNode next", result)
    result = re.sub(r"\bTreeNodeleft\b", "TreeNode left", result)
    result = re.sub(r"\bTreeNoderight\b", "TreeNode right", result)

    # Leftover C++ iterator / constructor syntax
    result = re.sub(r"\.begin\(\)\s*,\s*(\w+)\.end\(\)", r" /* elements of \1 */", result)
    result = re.sub(
        r"HashSet<Integer>\s*\(\s*(\w+)\s*/\*\s*elements of \1\s*\*/\s*\)\.size\(\)\s*!=\s*(\w+)\.length",
        r"IntStream.of(\1).distinct().count() != \2.length",
        result,
    )
    result = re.sub(
        r"return\s+HashSet<Integer>\s*\(\s*(\w+)\s*/\*\s*elements of \1\s*\*/\s*\)\.size\(\)\s*!=\s*(\w+)\.length",
        r"return IntStream.of(\1).distinct().count() != \2.length",
        result,
    )

    # Array helpers
    result = re.sub(r"\b(\w+)\.isEmpty\(\)", r"\1.length == 0", result)
    for name in ("values", "nums", "words", "arr", "grid", "intervals"):
        result = re.sub(rf"\b{name}\.size\(\)", f"{name}.length", result)

    # Default parameters (avoid matching == 0)
    result = re.sub(
        r"\(([^)=]*[^=])\s*=\s*0\)",
        lambda m: "(" + m.group(1).strip() + ")",
        result,
    )
    result = re.sub(
        r"\(([^)=]*[^=])\s*=\s*nullptr\)",
        lambda m: "(" + m.group(1).strip() + ")",
        result,
    )

    # Fix accidental == mangling
    result = re.sub(r"\.length\s*=\)", ".length == 0)", result)

    # Concurrency: FooBar pattern
    if "class FooBar" in result:
        result = re.sub(
            r"class FooBar \{.*?\n\}",
            """class FooBar {
    private int n;
    private final Object lock = new Object();
    private boolean fooTurn = true;

    public FooBar(int n) {
        this.n = n;
    }

    public void foo(Runnable printFoo) {
        for (int i = 0; i < n; i++) {
            synchronized (lock) {
                while (!fooTurn) {
                    try { lock.wait(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                }
                printFoo.run();
                fooTurn = false;
                lock.notifyAll();
            }
        }
    }

    public void bar(Runnable printBar) {
        for (int i = 0; i < n; i++) {
            synchronized (lock) {
                while (fooTurn) {
                    try { lock.wait(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                }
                printBar.run();
                fooTurn = true;
                lock.notifyAll();
            }
        }
    }
}""",
            result,
            flags=re.S,
        )

    # mutex -> ReentrantLock pattern (generic)
    result = re.sub(r"\block\s+mtx\b", "ReentrantLock lock = new ReentrantLock()", result)
    result = re.sub(r"unique_lock<[^>]+>\s+\w+\s*\([^)]+\)\s*;", "", result)

    # Remove erroneous 'public' on local vars
    result = re.sub(
        r"^(\s+)public (Trie|ListNode|TreeNode|int|boolean|long|String) (\w+ =)",
        r"\1\2 \3",
        result,
        flags=re.M,
    )

    # C++ deref on max_element
    result = re.sub(r"\*\s*max_element\([^)]+\)", "Arrays.stream(dp).max().getAsInt()", result)

    # LeetCode Solution / design classes: ensure public methods
    result = re.sub(
        r"(class Solution \{[^}]*?)(\n\s+)(boolean|int|long|void|String|ListNode|TreeNode|List<List)",
        r"\1\2public \3",
        result,
        flags=re.S,
    )
    result = re.sub(
        r"(class (?:Trie|LRUCache|MinStack|FooBar|SnapshotArray|HitCounter|RandomizedSet|WordDictionary) \{[^}]*?)(\n\s+)(boolean|int|long|void|String|Trie)",
        r"\1\2public \3",
        result,
        flags=re.S,
    )
    result = re.sub(
        r"(class ListNode \{[^}]*?)(\n\s+)(ListNode\()",
        r"\1\2public \3",
        result,
        flags=re.S,
    )

    return result


def convert_python_to_java(code: str) -> str:
    result = code
    result = re.sub(r"\bdef\s+(\w+)\s*\(", r"public static void \1(", result)
    result = re.sub(r"\bTrue\b", "true", result)
    result = re.sub(r"\bFalse\b", "false", result)
    result = re.sub(r"\bNone\b", "null", result)
    result = re.sub(r"\bself\b", "this", result)
    result = re.sub(r"\blen\s*\(\s*(\w+)\s*\)", r"\1.length", result)
    result = re.sub(r"\bprint\s*\(", "System.out.println(", result)
    return result


def convert_codeblock(match: re.Match[str]) -> str:
    fence_open, lang, newline, body, fence_close = match.groups()
    lang = lang.lower()
    if lang in ("cpp", "c++"):
        return f"{fence_open}java{newline}{convert_cpp_to_java(body)}{fence_close}"
    if lang == "python":
        return f"{fence_open}java{newline}{convert_python_to_java(body)}{fence_close}"
    return match.group(0)


def update_site_references(text: str) -> str:
    text = text.replace("blog_leetcode/", "blog_leetcode_java/")
    text = text.replace('blog_leetcode"', 'blog_leetcode_java"')
    text = text.replace("blog_leetcode'", "blog_leetcode_java'")
    text = re.sub(r"\bcopy-paste C\+\+", "copy-paste Java", text, flags=re.I)
    text = re.sub(r"\bC\+\+ code\b", "Java code", text, flags=re.I)
    text = re.sub(r"\bC\+\+ for\b", "Java for", text, flags=re.I)
    text = re.sub(r"\bcpp design\b", "java design", text, flags=re.I)
    text = re.sub(r"\bcpp\b", "java", text, flags=re.I)
    text = re.sub(r"```cpp\b", "```java", text)
    text = re.sub(r"```c\+\+\b", "```java", text)
    return text


def process_file(path: Path) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    updated = CODE_BLOCK_RE.sub(convert_codeblock, original)
    updated = update_site_references(updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return len(CODE_BLOCK_RE.findall(original)), 1 if updated != original else 0


def main() -> int:
    total_blocks = 0
    changed_files = 0
    for pattern in ("**/*.md", "**/*.html", "**/*.yml", "**/*.sh"):
        for path in ROOT.glob(pattern):
            if path.is_file() and "scripts" not in path.parts:
                blocks, changed = process_file(path)
                total_blocks += blocks
                changed_files += changed
    print(f"Processed code blocks: {total_blocks}")
    print(f"Changed files: {changed_files}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
