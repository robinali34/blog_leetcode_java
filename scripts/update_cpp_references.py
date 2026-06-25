#!/usr/bin/env python3
"""Replace C++/STL/cpp references in titles and post prose with Java equivalents."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: more specific patterns first.
REPLACEMENTS: list[tuple[str, str]] = [
    # Headings
    (r"## Solution in C\+\+", "## Solution in Java"),
    (r"## Template in C\+\+", "## Template in Java"),
    (r"## C\+\+ Solution", "## Java Solution"),
    (r"### C\+\+ Approach:", "### Java Approach:"),
    (r"### C\+\+ `std::partial_sum`", "### Java prefix-sum approach"),
    (r"### Using `<random>` \(Modern C\+\+\)", "### Using `java.util.Random` (Modern Java)"),
    (r"### C\+\+20 contains\(\) Method", "### `HashSet.contains()` Method"),
    (r"### Using `std::accumulate` \(C\+\+\)", "### Using `Arrays.stream().sum()` (Java)"),
    (r"### Using `starts_with\(\)` \(C\+\+\)", "### Using `String.startsWith()` (Java)"),
    (r"### Solution: Using std::list with splice", "### Solution: Using `LinkedHashMap` move-to-end"),
    (r"### Solution: Ordered Set \(std::set\) with Binary Search", "### Solution: `TreeSet` with Binary Search"),
    (r"### Approach 3: Using STL remove", "### Approach 3: Using two-pointer compaction"),
    (r"### Approach 2: Using STL reverse", "### Approach 2: Using `Collections.reverse()`"),
    (r"### Approach 3: Using STL Stack", "### Approach 3: Using `Deque` / `Stack`"),
    (r"## Solution 2: Using STL lower_bound", "## Solution 2: Using `Collections.binarySearch()`"),
    (r"## Solution 3: Using STL upper_bound", "## Solution 3: Using binary search (upper bound)"),
    (r"## Solution 1: Using std::stack", "## Solution 1: Using `Deque` as stack"),
    (r"## Why std::list is Preferred", "## Why `LinkedHashMap` is Preferred"),
    (r"### ✅ Vectors \(`std::vector`\)", "### ✅ Dynamic Arrays (`ArrayList` / `int[]`)"),
    (r"\| Concept       \| STL Equivalent", "| Concept       | Java Equivalent"),
    # Versioned C++ labels
    (r"\(C\+\+20 Optimized\)", "(Java Optimized)"),
    (r"Optimized C\+\+20 Version", "Optimized Java Version"),
    (r"C\+\+20 Optimizations:", "Java Optimizations:"),
    (r"C\+\+20 compatible", "Java compatible"),
    (r"C\+\+20 Optimized", "Java Optimized"),
    (r"Key Optimizations \(C\+\+20\)", "Key Optimizations (Java)"),
    (r"Backtracking with C\+\+20 Optimizations", "Backtracking with Java Optimizations"),
    (r"Binary Semaphores \(C\+\+20\)", "Binary Semaphores (Java)"),
    (r"Three Counting Semaphores \(C\+\+20\)", "Three Counting Semaphores (Java)"),
    (r"Mutex \+ Two Condition Variables \(C\+\+11\)", "Mutex + Two Condition Variables (Java)"),
    (r"// Modern C\+\+20 \(your code\)", "// Modern Java (your code)"),
    (r"// Alternative \(C\+\+17 and earlier\)", "// Alternative (manual approach)"),
    (r"// Min heap using greater<> \(C\+\+14\+\)", "// Min heap using `PriorityQueue` with comparator"),
    (r"// structured binding \(C\+\+17\)", "// Map entry iteration"),
    (r"Requires C\+\+20", "Requires Java 5+"),
    (r"Requires C\+\+11\+", "Works in all Java versions"),
    (r"Works in C\+\+11\+", "Works in all Java versions"),
    (r"Alternative \(C\+\+11/14\):", "Alternative (Java):"),
    (r"\(C\+\+17\)", "(Java)"),
    (r"C\+\+17", "Java"),
    (r"C\+\+20", "Modern Java"),
    (r"C\+\+14\+", "Java"),
    (r"C\+\+11\+", "Java"),
    (r"C\+\+11/14", "Java"),
    (r"C\+\+11", "Java"),
    (r"C\+\+14", "Java"),
    (r"Modern C\+\+", "Modern Java"),
    (r"C\+\+ Version", "Java Version"),
    (r"C\+\+ behavior", "Java behavior"),
    (r"C\+\+ doesn't", "Java doesn't"),
    (r"C\+\+ stringstream", "Java `StringTokenizer` / `Scanner`"),
    (r"C\+\+ STL's", "Java Collections'"),
    (r"C\+\+ STL", "Java Collections"),
    (r"battle‑tested C\+\+ templates", "battle‑tested Java templates"),
    (r"battle-tested C\+\+ templates", "battle-tested Java templates"),
    (r"C\+\+ templates", "Java templates"),
    (r"idiomatic C\+\+", "idiomatic Java"),
    (r"memory management in C\+\+", "object references in Java"),
    (r"Not deleting trie nodes in C\+\+", "Relying on garbage collection in Java (no manual node deletion)"),
    (r"in C\+\+", "in Java"),
    (r"C\+\+ & Systems Blog", "Java LeetCode Blog"),
    (r"C\+\+ Approach:", "Java Approach:"),
    (r"C\+\+ `std::partial_sum`", "Java prefix-sum loop"),
    (r"C\+\+ `partial_sum`", "Java prefix-sum loop"),
    (r"default in C\+\+", "default in Java (`PriorityQueue` is a min-heap)"),
    (r"The `priority_queue` in C\+\+ is a max-heap by default, so we reverse the comparison \(`a->val > b->val`\) to get min-heap behavior.",
     "Use `PriorityQueue` with a comparator (Java's default `PriorityQueue` is a min-heap)."),
    (r"In C\+\+, the `%` operator", "In Java, the `%` operator"),
    # STL references
    (r"STL next_permutation", "permutation generation (library or backtracking)"),
    (r"STL approach", "library approach"),
    (r"STL Approach", "Library Approach"),
    (r"STL Advantage:", "Library Advantage:"),
    (r"STL Efficiency:", "Library efficiency:"),
    (r"STL Functions:", "Arrays/Collections utilities:"),
    (r"STL max_element", "`Arrays.stream().max()`"),
    (r"STL remove", "two-pointer remove"),
    (r"STL Stack", "`Deque` / `Stack`"),
    (r"STL dependency", "JDK dependency"),
    (r"Requires STL", "Uses JDK"),
    (r"No STL dependency", "No external dependencies"),
    (r"uses only STL algorithms", "uses only JDK utilities"),
    (r"STL is performance-tuned", "JDK utilities are well optimized"),
    (r"STL Alternatives:", "JDK Alternatives:"),
    (r"STL's `lower_bound`", "`Collections.binarySearch()`"),
    (r"Built into STL function", "Built into JDK utility"),
    (r"Use STL when:", "Use library approach when:"),
    (r"Use STL ", "Use JDK "),
    (r"No STL scan", "No JDK scan helper"),
    # std:: library names
    (r"`std::list::splice`", "`LinkedHashMap` move-to-end"),
    (r"std::list::splice", "LinkedHashMap move-to-end"),
    (r"`std::list`", "`LinkedList` / `LinkedHashMap`"),
    (r"std::list", "LinkedList"),
    (r"`std::map`", "`TreeMap`"),
    (r"std::map", "TreeMap"),
    (r"`std::set`", "`TreeSet`"),
    (r"std::set", "TreeSet"),
    (r"`std::vector<int>`", "`int[]` / `ArrayList<Integer>`"),
    (r"std::vector<int>", "int[]"),
    (r"`std::vector`", "`ArrayList` / array"),
    (r"std::vector", "ArrayList"),
    (r"`std::stack`", "`Deque`"),
    (r"std::stack", "Deque"),
    (r"`std::partial_sum`", "prefix-sum loop"),
    (r"std::partial_sum", "prefix-sum loop"),
    (r"`std::inclusive_scan`", "prefix-sum loop"),
    (r"std::inclusive_scan", "prefix-sum loop"),
    (r"`std::execution::par`", "`parallelStream()`"),
    (r"std::execution::par", "parallelStream()"),
    (r"`std::accumulate`", "`Arrays.stream().sum()`"),
    (r"std::accumulate", "Arrays.stream().sum()"),
    (r"`std::mutex`", "`ReentrantLock` / `synchronized`"),
    (r"std::mutex", "ReentrantLock"),
    (r"string_view", "String.substring"),
    (r"lower_bound", "binary search (lower bound)"),
    (r"upper_bound", "binary search (upper bound)"),
    # Table cells in cheatsheet
    (r"`unordered_map<K, V>`", "`HashMap<K, V>`"),
    (r"`unordered_set<T>`", "`HashSet<T>`"),
    (r"`map<K, V>`", "`TreeMap<K, V>`"),
    (r"`set<T>`", "`TreeSet<T>`"),
    (r"`priority_queue<T, vector<T>, greater<T>>`", "`PriorityQueue<T>` with comparator"),
    (r"`priority_queue<T>`", "`PriorityQueue<T>`"),
    (r"`stack<T>`", "`Deque<T>`"),
    (r"`queue<T>`", "`Queue<T>`"),
    (r"`deque<T>`", "`ArrayDeque<T>`"),
    (r"`ostringstream` or `\+=`", "`StringBuilder`"),
    (r"`vector<vector<int>>`", "`int[][]` / `List<List<Integer>>`"),
    # Categories / misc
    (r"\bstl\b", "java-collections"),
    (r"Convert std::vector<int> → ListNode\* \(linked list\)", "Convert `int[]` → `ListNode` (linked list)"),
    (r"Convert ListNode\* → std::vector<int>", "Convert `ListNode` → `int[]`"),
    (r"4\. \*\*STL Alternatives\*\*:", "4. **JDK Alternatives**:"),
    (r"4\. \*\*STL Functions\*\*:", "4. **Arrays/Collections utilities**:"),
    (r"- Uses STL functions", "- Uses JDK utility methods"),
    (r"- Requires understanding of STL iterators", "- Requires understanding of collection iteration"),
    (r"\*\*Why STL works", "**Why the library approach works"),
    (r"\| \*\*STL\*\* \|", "| **Library** |"),
    (r"\| \*\*Solution 2: STL\*\* \|", "| **Solution 2: Library** |"),
    (r"- \*\*Slower than STL\*\*", "- **Slower than library approach**"),
    (r"\*\*Solution 2 \(STL\)\:\*\*", "**Solution 2 (Library):**"),
    (r"Use Solution 2 \(STL\)", "Use Solution 2 (library approach)"),
    (r"4\. \*\*Lexicographic Order:\*\* STL generates", "4. **Lexicographic Order:** Library approach generates"),
    (r"// Modern C\+\+20 \(your code\)", "// Modern Java (your code)"),
    (r"// Alternative \(C\+\+17 and earlier\)", "// Alternative (manual approach)"),
    (r"// Min heap using greater<> \(C\+\+14\+\)", "// Min heap using PriorityQueue comparator"),
    (r"// structured binding \(C\+\+17\)", "// iterate map entries"),
    (r"gcd\(a, b\);   // C\+\+17", "Math.gcd(a, b);   // Java"),
    (r"lcm\(a, b\);   // C\+\+17", "// lcm: a * b / gcd(a, b)   // Java"),
    (r"## 🔄 Algorithms \(`<algorithm>`\)", "## 🔄 Algorithms (`java.util.Arrays` / `Collections`)"),
    (r"## 📐 Math Utilities \(`<cmath>`, `<numeric>`\)", "## 📐 Math Utilities (`Math` class)"),
]

# Lines to skip transforming (false positives)
SKIP_LINE_PATTERNS = [
    re.compile(r"dec\+\+"),
    re.compile(r"for \(int c ="),
    re.compile(r"sparse vector", re.I),
]


def should_skip_line(line: str) -> bool:
    return any(p.search(line) for p in SKIP_LINE_PATTERNS)


def transform_java_block(code: str) -> str:
    """Update C++/STL mentions inside converted Java code blocks."""
    updated = code
    for pattern, repl in REPLACEMENTS:
        updated = re.sub(pattern, repl, updated)
    return updated


def transform_text(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_java_fence = False
    java_block_lines: list[str] = []

    def flush_java_block() -> None:
        if java_block_lines:
            block = "\n".join(java_block_lines)
            out.append(transform_java_block(block))
            java_block_lines.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```java"):
            flush_java_block()
            in_java_fence = True
            out.append(line)
            continue
        if stripped == "```" and in_java_fence:
            flush_java_block()
            in_java_fence = False
            out.append(line)
            continue

        if in_java_fence:
            java_block_lines.append(line)
            continue

        if should_skip_line(line):
            out.append(line)
            continue

        updated = line
        for pattern, repl in REPLACEMENTS:
            updated = re.sub(pattern, repl, updated)
        out.append(updated)

    flush_java_block()
    return "\n".join(out)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = transform_text(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    patterns = ("**/*.md", "**/*.html")
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file() and "scripts" not in path.parts and "_site" not in path.parts:
                if process_file(path):
                    changed += 1
                    print(path.relative_to(ROOT))
    print(f"\nUpdated {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
