---
layout: post
title: "Java Guide: Language Basics"
date: 2026-06-24 10:00:00 -0700
categories: java guide reference tutorial programming fundamentals
permalink: /posts/2026-06-24-java-guide-basics/
tags: [java, guide, basics, tutorial, leetcode, collections, arrays, strings, oop, templates, java-21, java-25, java-26]
---

{% raw %}
# Java Guide: Language Basics

A practical reference for learning C++ with a focus on competitive programming and technical interviews. Whether you're picking up C++ for the first time or brushing up before a contest, this page covers what matters.

> **New to LeetCode?** Start with the [Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/) to understand the platform, difficulty levels, and which problems to solve first.

<svg viewBox="0 0 740 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <defs>
    <marker id="guide-arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#8B8680"/>
    </marker>
  </defs>

  <text x="370" y="22" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">How This Guide Is Organized</text>

  <!-- Part boxes - top row -->
  <rect x="10" y="38" width="120" height="52" rx="8" fill="#E8D5D0" stroke="#C08070" stroke-width="1.8"/>
  <text x="70" y="60" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 1</text>
  <text x="70" y="78" font-size="9" fill="#7A7772" text-anchor="middle">Language Basics</text>

  <rect x="145" y="38" width="120" height="52" rx="8" fill="#D4D8D0" stroke="#6B8B6B" stroke-width="1.8"/>
  <text x="205" y="60" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 2</text>
  <text x="205" y="78" font-size="9" fill="#7A7772" text-anchor="middle">Collections Toolkit</text>

  <rect x="280" y="38" width="120" height="52" rx="8" fill="#D4D8E0" stroke="#7080A0" stroke-width="1.8"/>
  <text x="340" y="60" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 3</text>
  <text x="340" y="78" font-size="9" fill="#7A7772" text-anchor="middle">Patterns</text>

  <rect x="415" y="38" width="120" height="52" rx="8" fill="#E8E3D8" stroke="#B8A880" stroke-width="1.8"/>
  <text x="475" y="60" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 4</text>
  <text x="475" y="78" font-size="9" fill="#7A7772" text-anchor="middle">Solution Template</text>

  <!-- Arrows top row -->
  <line x1="130" y1="64" x2="143" y2="64" stroke="#8B8680" stroke-width="1.5" marker-end="url(#guide-arr)"/>
  <line x1="265" y1="64" x2="278" y2="64" stroke="#8B8680" stroke-width="1.5" marker-end="url(#guide-arr)"/>
  <line x1="400" y1="64" x2="413" y2="64" stroke="#8B8680" stroke-width="1.5" marker-end="url(#guide-arr)"/>

  <!-- Part boxes - bottom row -->
  <rect x="145" y="115" width="150" height="52" rx="8" fill="#E8D5D0" stroke="#C08070" stroke-width="1.8"/>
  <text x="220" y="137" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 5</text>
  <text x="220" y="155" font-size="9" fill="#7A7772" text-anchor="middle">Learning Path (Roadmap)</text>

  <rect x="320" y="115" width="150" height="52" rx="8" fill="#D4D8D0" stroke="#6B8B6B" stroke-width="1.8"/>
  <text x="395" y="137" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Part 6</text>
  <text x="395" y="155" font-size="9" fill="#7A7772" text-anchor="middle">Modern Java (21+)</text>

  <rect x="495" y="115" width="150" height="52" rx="8" fill="#D4D8E0" stroke="#7080A0" stroke-width="1.8"/>
  <text x="570" y="137" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Quick Ref</text>
  <text x="570" y="155" font-size="9" fill="#7A7772" text-anchor="middle">Quick Reference</text>

  <!-- Vertical connections -->
  <line x1="205" y1="90" x2="220" y2="113" stroke="#8B8680" stroke-width="1.2" stroke-dasharray="4"/>
  <line x1="340" y1="90" x2="395" y2="113" stroke="#8B8680" stroke-width="1.2" stroke-dasharray="4"/>
  <line x1="475" y1="90" x2="570" y2="113" stroke="#8B8680" stroke-width="1.2" stroke-dasharray="4"/>

  <!-- Legend -->
  <text x="370" y="192" font-size="10" fill="#9A9792" text-anchor="middle">Top row: learn in order → Bottom row: reference anytime</text>
</svg>

---
## Why Java for Algorithms?

<svg viewBox="0 0 740 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <!-- Central node -->
  <rect x="275" y="10" width="190" height="44" rx="22" fill="#D4D8E0" stroke="#7080A0" stroke-width="2"/>
  <text x="370" y="37" font-size="14" fill="#3A3530" font-weight="700" text-anchor="middle">Java for Algorithms</text>

  <!-- Branches -->
  <line x1="275" y1="32" x2="145" y2="80" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="325" y1="54" x2="295" y2="80" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="415" y1="54" x2="445" y2="80" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="465" y1="32" x2="595" y2="80" stroke="#B8B5B0" stroke-width="1.5"/>

  <!-- Speed -->
  <rect x="40" y="78" width="150" height="40" rx="8" fill="#E8D5D0" stroke="#B8B5B0" stroke-width="1.2"/>
  <text x="115" y="97" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Fastest Runtime</text>
  <text x="115" y="112" font-size="9" fill="#9A9792" text-anchor="middle">compiled to native code</text>

  <!-- Java Collections -->
  <rect x="220" y="78" width="150" height="40" rx="8" fill="#D4D8D0" stroke="#B8B5B0" stroke-width="1.2"/>
  <text x="295" y="97" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Rich Java Collections</text>
  <text x="295" y="112" font-size="9" fill="#9A9792" text-anchor="middle">containers + algorithms</text>

  <!-- Control -->
  <rect x="400" y="78" width="150" height="40" rx="8" fill="#D4D8E0" stroke="#B8B5B0" stroke-width="1.2"/>
  <text x="475" y="97" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Fine Control</text>
  <text x="475" y="112" font-size="9" fill="#9A9792" text-anchor="middle">pointers, bits, memory</text>

  <!-- Platform standard -->
  <rect x="560" y="78" width="150" height="40" rx="8" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1.2"/>
  <text x="635" y="97" font-size="11" fill="#5A5752" font-weight="700" text-anchor="middle">Industry Standard</text>
  <text x="635" y="112" font-size="9" fill="#9A9792" text-anchor="middle">ICPC, CF, LC, interviews</text>

  <!-- Bottom bar -->
  <rect x="80" y="140" width="580" height="28" rx="14" fill="#FAF8F5" stroke="#D4D1CC" stroke-width="1.2"/>
  <text x="370" y="159" font-size="11" fill="#5A5752" font-weight="600" text-anchor="middle">Result: Write less code → Run faster → Solve harder problems</text>
</svg>

| Advantage | Details |
|---|---|
| **Speed** | Compiled to native code -- fastest runtime of any mainstream language |
| **Java Collections** | The Standard Template Library provides battle-tested containers and algorithms |
| **Industry standard for CP** | Codeforces, ICPC, AtCoder, and LeetCode all favor C++ |
| **Fine-grained control** | Pointers, memory layout, and bit manipulation are first-class citizens |
| **Interview-friendly** | Many interviewers are comfortable reading C++ |

---

## Part 5: Learning Path

Follow these stages in order. Each one builds on the last — don't skip ahead.

<svg viewBox="0 0 780 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <defs>
    <marker id="lp-arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#8B8680"/>
    </marker>
  </defs>

  <!-- Stage 1 -->
  <rect x="10" y="30" width="140" height="70" rx="10" fill="#E8D5D0" stroke="#C08070" stroke-width="2"/>
  <text x="80" y="55" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">Stage 1</text>
  <text x="80" y="73" font-size="10" fill="#7A7772" text-anchor="middle">Syntax &amp; Basics</text>
  <text x="80" y="88" font-size="9" fill="#9A9792" text-anchor="middle">1-2 weeks</text>

  <!-- Arrow 1→2 -->
  <line x1="150" y1="65" x2="168" y2="65" stroke="#8B8680" stroke-width="1.8" marker-end="url(#lp-arr)"/>

  <!-- Stage 2 -->
  <rect x="170" y="30" width="140" height="70" rx="10" fill="#D4D8D0" stroke="#6B8B6B" stroke-width="2"/>
  <text x="240" y="55" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">Stage 2</text>
  <text x="240" y="73" font-size="10" fill="#7A7772" text-anchor="middle">Java Collections Mastery</text>
  <text x="240" y="88" font-size="9" fill="#9A9792" text-anchor="middle">2-3 weeks</text>

  <!-- Arrow 2→3 -->
  <line x1="310" y1="65" x2="328" y2="65" stroke="#8B8680" stroke-width="1.8" marker-end="url(#lp-arr)"/>

  <!-- Stage 3 -->
  <rect x="330" y="30" width="140" height="70" rx="10" fill="#D4D8E0" stroke="#7080A0" stroke-width="2"/>
  <text x="400" y="55" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">Stage 3</text>
  <text x="400" y="73" font-size="10" fill="#7A7772" text-anchor="middle">Pointers &amp; Memory</text>
  <text x="400" y="88" font-size="9" fill="#9A9792" text-anchor="middle">1-2 weeks</text>

  <!-- Arrow 3→4 -->
  <line x1="470" y1="65" x2="488" y2="65" stroke="#8B8680" stroke-width="1.8" marker-end="url(#lp-arr)"/>

  <!-- Stage 4 -->
  <rect x="490" y="30" width="140" height="70" rx="10" fill="#E8E3D8" stroke="#B8A880" stroke-width="2"/>
  <text x="560" y="55" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">Stage 4</text>
  <text x="560" y="73" font-size="10" fill="#7A7772" text-anchor="middle">Modern C++</text>
  <text x="560" y="88" font-size="9" fill="#9A9792" text-anchor="middle">1 week</text>

  <!-- Arrow 4→5 -->
  <line x1="630" y1="65" x2="648" y2="65" stroke="#8B8680" stroke-width="1.8" marker-end="url(#lp-arr)"/>

  <!-- Stage 5 -->
  <rect x="650" y="30" width="120" height="70" rx="10" fill="#D4D1CC" stroke="#8B8680" stroke-width="2"/>
  <text x="710" y="55" font-size="13" fill="#5A5752" font-weight="700" text-anchor="middle">Stage 5</text>
  <text x="710" y="73" font-size="10" fill="#7A7772" text-anchor="middle">Algorithms</text>
  <text x="710" y="88" font-size="9" fill="#9A9792" text-anchor="middle">Ongoing</text>

  <!-- Details below each stage -->
  <rect x="10" y="120" width="140" height="95" rx="8" fill="#FAF8F5" stroke="#E0DDD8" stroke-width="1"/>
  <text x="20" y="138" font-size="9" fill="#5A5752">variables, types</text>
  <text x="20" y="152" font-size="9" fill="#5A5752">if/else, for, while</text>
  <text x="20" y="166" font-size="9" fill="#5A5752">functions, references</text>
  <text x="20" y="180" font-size="9" fill="#5A5752">arrays, cin/cout</text>
  <text x="20" y="200" font-size="9" fill="#3A6B3A" font-weight="600">10-15 Easy problems</text>

  <rect x="170" y="120" width="140" height="95" rx="8" fill="#FAF8F5" stroke="#E0DDD8" stroke-width="1"/>
  <text x="180" y="138" font-size="9" fill="#5A5752">vector, string, pair</text>
  <text x="180" y="152" font-size="9" fill="#5A5752">map, set, unordered_*</text>
  <text x="180" y="166" font-size="9" fill="#5A5752">stack, queue, pq</text>
  <text x="180" y="180" font-size="9" fill="#5A5752">sort, lower_bound</text>
  <text x="180" y="200" font-size="9" fill="#3A6B3A" font-weight="600">20-30 Easy/Med</text>

  <rect x="330" y="120" width="140" height="95" rx="8" fill="#FAF8F5" stroke="#E0DDD8" stroke-width="1"/>
  <text x="340" y="138" font-size="9" fill="#5A5752">pointers vs refs</text>
  <text x="340" y="152" font-size="9" fill="#5A5752">ListNode*, TreeNode*</text>
  <text x="340" y="166" font-size="9" fill="#5A5752">new/delete (avoid)</text>
  <text x="340" y="180" font-size="9" fill="#5A5752">smart pointers</text>
  <text x="340" y="200" font-size="9" fill="#3A6B3A" font-weight="600">LL + Tree problems</text>

  <rect x="490" y="120" width="140" height="95" rx="8" fill="#FAF8F5" stroke="#E0DDD8" stroke-width="1"/>
  <text x="500" y="138" font-size="9" fill="#5A5752">auto, structured bindings</text>
  <text x="500" y="152" font-size="9" fill="#5A5752">lambdas, captures</text>
  <text x="500" y="166" font-size="9" fill="#5A5752">initializer_list</text>
  <text x="500" y="180" font-size="9" fill="#5A5752">range-based for</text>
  <text x="500" y="200" font-size="9" fill="#3A6B3A" font-weight="600">Refactor solutions</text>

  <rect x="650" y="120" width="120" height="95" rx="8" fill="#FAF8F5" stroke="#E0DDD8" stroke-width="1"/>
  <text x="660" y="138" font-size="9" fill="#5A5752">two pointers</text>
  <text x="660" y="152" font-size="9" fill="#5A5752">BFS, DFS</text>
  <text x="660" y="166" font-size="9" fill="#5A5752">DP patterns</text>
  <text x="660" y="180" font-size="9" fill="#5A5752">graph, backtracking</text>
  <text x="660" y="200" font-size="9" fill="#3A6B3A" font-weight="600">Templates blog</text>

  <!-- Timeline bar -->
  <rect x="10" y="240" width="760" height="30" rx="15" fill="#F0EBE6" stroke="#D4D1CC" stroke-width="1"/>
  <rect x="10" y="240" width="140" height="30" rx="15" fill="#E8D5D0"/>
  <rect x="150" y="240" width="180" height="30" fill="#D4D8D0"/>
  <rect x="330" y="240" width="140" height="30" fill="#D4D8E0"/>
  <rect x="470" y="240" width="120" height="30" fill="#E8E3D8"/>
  <rect x="590" y="240" width="180" height="30" rx="15" fill="#D4D1CC"/>

  <text x="80" y="260" font-size="10" fill="#5A5752" font-weight="600" text-anchor="middle">Week 1-2</text>
  <text x="240" y="260" font-size="10" fill="#5A5752" font-weight="600" text-anchor="middle">Week 3-5</text>
  <text x="400" y="260" font-size="10" fill="#5A5752" font-weight="600" text-anchor="middle">Week 6-7</text>
  <text x="530" y="260" font-size="10" fill="#5A5752" font-weight="600" text-anchor="middle">Week 8</text>
  <text x="680" y="260" font-size="10" fill="#5A5752" font-weight="600" text-anchor="middle">Week 9+</text>

  <!-- Milestone markers -->
  <text x="390" y="305" font-size="12" fill="#3A6B3A" font-weight="700" text-anchor="middle">Milestones</text>
  <text x="80" y="325" font-size="10" fill="#5A5752" text-anchor="middle">"I can write C++"</text>
  <text x="240" y="325" font-size="10" fill="#5A5752" text-anchor="middle">"I know which container"</text>
  <text x="400" y="325" font-size="10" fill="#5A5752" text-anchor="middle">"I get pointers"</text>
  <text x="560" y="325" font-size="10" fill="#5A5752" text-anchor="middle">"Cleaner code"</text>
  <text x="710" y="325" font-size="10" fill="#5A5752" text-anchor="middle">"Interview ready"</text>
</svg>

### Stage 1 — Syntax & Basics (1-2 weeks)

- [ ] Variables, types, operators
- [ ] Control flow (if/else, for, while)
- [ ] Functions (pass by value, reference, const reference)
- [ ] Arrays and strings
- [ ] Basic I/O (`cin`, `cout`)

**Practice:** Solve 10-15 LeetCode Easy problems using C++.

### Stage 2 — Java Collections Mastery (2-3 weeks)

- [ ] `vector`, `string`, `pair`
- [ ] `unordered_map`, `unordered_set`
- [ ] `set`, `map`, `multiset`
- [ ] `stack`, `queue`, `deque`
- [ ] `priority_queue` (min-heap, max-heap)
- [ ] `sort`, `lower_bound`, `upper_bound`
- [ ] Iterators and range-based for loops

**Practice:** Solve 20-30 LeetCode Easy/Medium problems. For each one, ask: "Which Java Collections container makes this easier?"

### Stage 3 — Pointers & Memory (1-2 weeks)

- [ ] Pointers vs references
- [ ] `new` / `delete` (and why to avoid them)
- [ ] `ListNode*`, `TreeNode*` patterns
- [ ] Smart pointers (`unique_ptr`, `shared_ptr`) — for real projects, not LeetCode

**Practice:** Solve linked list and tree problems (LC 206, 21, 141, 104, 226, 102).

### Stage 4 — Modern C++ Features (1 week)

- [ ] `auto` type deduction
- [ ] Structured bindings (`auto& [k, v]`)
- [ ] Lambda functions and captures
- [ ] `initializer_list` (`min({a, b, c})`)
- [ ] Range-based for with references

### Stage 5 — Algorithm Templates (Ongoing)

At this point, you're ready to focus on algorithms rather than language features. Work through the [LeetCode Templates](/blog_leetcode_java/leetcode-templates/) on this blog:

1. [Arrays & Strings](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-arrays-strings/) — two pointers, sliding window
2. [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/) — binary search patterns
3. [DFS](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-dfs/) / [BFS](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-bfs/) — graph and tree traversal
4. [Dynamic Programming](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-dp/) — 1D, 2D, bitmask
5. [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/) — topological sort, Dijkstra, DSU

---

## Resources

- [cppreference.com](https://en.cppreference.com/) — the definitive C++ reference
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) — best practices by Bjarne Stroustrup
- [Compiler Explorer (Godbolt)](https://godbolt.org/) — see what your C++ compiles to
- [LeetCode Templates on this blog](/blog_leetcode_java/leetcode-templates/) — algorithm patterns in C++
- [LeetCode Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/) — getting started with the platform
## Contents

- [Why these features exist](#why-these-features-exist)
- [Program structure](#program-structure)
- [Types and variables](#types-and-variables)
- [Arrays](#arrays)
- [Strings](#strings)
- [Control flow](#control-flow)
- [Methods and classes](#methods-and-classes)
- [Collections framework](#collections-framework)
- [Sorting and binary search](#sorting-and-binary-search)
- [Common LeetCode definitions](#common-leetcode-definitions)
- [Sample usages](#sample-usages)
- [Common LeetCode templates](#common-leetcode-templates)
- [Modern Java (21 → 26)](#modern-java-21--26)
- [Tips and pitfalls](#tips-and-pitfalls)

## Why these features exist

Java’s core types and `java.util` collections are not random — each one maps to a recurring need in algorithm problems. Before memorizing APIs, ask **what operation you need** (index access, uniqueness, ordering, LIFO, etc.) and pick the matching tool.
<section class="template-diagrams" aria-label="Why Java features exist">
  <div class="template-diagram-grid">
    <figure class="template-diagram-card template-diagram-card-wide">
      <figcaption>
        <strong>Need → feature</strong>
        <span>Match the algorithm requirement to the right Java API.</span>
      </figcaption>
      {% include diagrams/java-feature-why.svg.html %}
    </figure>
  </div>
</section>

**Quick decision guide**

| You need… | Reach for… |
|-----------|------------|
| Index `i` in O(1) | `int[]`, `int[][]` |
| Unknown final size | `ArrayList` |
| “Have I seen this?” | `HashSet` |
| Count / map value → index | `HashMap` |
| Sorted next / floor / ceiling | `TreeSet`, `TreeMap` |
| Next smallest / largest repeatedly | `PriorityQueue` |
| Undo / nesting / DFS stack | `Deque` as stack |
| Level-order / shortest path | `Queue` + BFS |
| Concatenate many characters | `StringBuilder` |

## Program structure

LeetCode solutions are usually written inside a class. On the platform you often only fill in a method; locally, a minimal program looks like this:

```java
// import java.util.Arrays;
// import java.util.Collections;
public class Main {
    public static void main(String[] args) {
        Solution sol = new Solution();
        int[] nums = {2, 7, 11, 15}
        System.out.println(Arrays.toString(sol.twoSum(nums, 9)));
    }
}

class Solution {
    public int[] twoSum(int[] nums, int target) {
        // your algorithm here
        return new int[] {0, 1}
    }
}
```

Key ideas:

- `public` — visible from other classes.
- `static` — belongs to the class, not an instance (used for `main` and utility helpers).
- `void` / `int` / `int[]` — return type of a method.

## Types and variables

### Primitives

| Type      | Size   | Example        | Notes                          |
|-----------|--------|----------------|--------------------------------|
| `boolean` | 1 bit  | `true`         | Condition flags                |
| `byte`    | 8 bit  | `(byte) 127`   | Rare in LeetCode               |
| `short`   | 16 bit | `(short) 1000` | Rare in LeetCode               |
| `int`     | 32 bit | `42`           | Default for counting, indices  |
| `long`    | 64 bit | `1_000_000_000L` | Large sums, timestamps       |
| `float`   | 32 bit | `3.14f`        | Rare; prefer `double`          |
| `double`  | 64 bit | `3.14159`      | Geometry, floating math        |
| `char`    | 16 bit | `'a'`          | Single Unicode character       |

Use `long` when intermediate results can overflow `int` (roughly ±2.1 billion):

```java
long total = 0;
for (int x : nums) {
    total += x;
}
```

### Wrapper classes

Primitives auto-box to objects when needed:

```java
a = 10; // boxed
b = a; // unboxed

// null-safe comparison for objects
x = null; // x == 10;       // NullPointerException
Objects.equals(x, 10);
```

For maps and sets, use wrapper types as keys when required: `Map<Integer, Integer>`, `Set<Character>`.

### `var` (Java 10+)

Local type inference — useful for long generic types:

```java
// import java.util.*;
var freq = new HashMap<Integer, Integer>();
var list = new ArrayList<List<Integer>>();
```

## Arrays

Fixed-size, ordered, indexable. Fast random access.

```java
int[] nums = new int[5];          // {0, 0, 0, 0, 0}
int[] vals = {1, 2, 3, 4, 5};     // initializer
int len = nums.length;            // note: .length, not .length()
nums[0] = 10;

// 2D array
int[][] grid = new int[3][4];
int[][] board = {new int[] {1, 2}, new int[] {3, 4}}
```

Copy and fill:

```java
// import java.util.Arrays;
// import java.util.Collections;
int[] copy = nums.clone();
int[] copy2 = Arrays.copyOf(nums, nums.length);
Arrays.fill(nums, -1);
```

Iterate:

```java
for (int i = 0; i < nums.length; i++) {
    System.out.println(nums[i]);
}

for (int x : nums) {
    System.out.println(x);
}
```

### `ArrayList` (dynamic array)

Use when size is unknown or you need `add` / `remove`.

```java
// import java.util.*;
import java.util.ArrayList;
import java.util.List;

List<Integer> list = new ArrayList<>();
list.add(1);
list.add(2);
list.get(0);           // 1
list.set(0, 10);
list.size();
list.remove(list.size() - 1);

// from array
List<Integer> fromArr = new ArrayList<>();
for (int x : nums) fromArr.add(x);
```

## Strings

`String` is **immutable** — every “change” creates a new object.

```java
String s = "hello";
int n = s.length();
char c = s.charAt(0);           // 'h'
String sub = s.substring(1, 3); // "el"
int idx = s.indexOf("ll");      // 2
boolean ok = s.equals("hello"); // always use .equals for content
```

Build strings efficiently with `StringBuilder`:

```java
StringBuilder sb = new StringBuilder();
sb.append('a');
sb.append("bc");
sb.reverse();
String result = sb.toString();
```

Convert between numbers and strings:

```java
int x = Integer.parseInt("42");
String str = String.valueOf(42);
```

Character helpers:

```java
char ch = 'A';
boolean letter = Character.isLetter(ch);
char lower = Character.toLowerCase(ch);
int digit = Character.getNumericValue('7'); // 7
```

## Control flow

```java
if (x > 0) {
    // ...
} else if (x < 0) {
    // ...
} else {
    // ...
}

for (int i = 0; i < n; i++) { }

for (int x : arr) { }

while (left < right) {
    left++;
}

do {
    // runs at least once
} while (condition);
```

`switch` (modern style):

```java
switch (ch) {
    case 'a', 'e', 'i', 'o', 'u' . vowelCount++;
    case ' ' . {}
    default . consonantCount++;
}
```

## Methods and classes

### Instance vs static

```java
class Counter {
    int value = 0;

    void increment() {   // instance method
        value++;
    }

    static int add(int a, int b) {  // static — no instance needed
        return a + b;
    }
}
```

### Defining a simple data class

```java
class Pair {
        int first;
        int second;

    Pair(int first, int second) {
        this[0] = first;
        this[1] = second;
    }
}
```

Java 16+ records are concise for immutable carriers:

```java
record Point(int x, int y) {}
```

### Interfaces and `Comparator`

```java
// import java.util.Arrays;
// import java.util.Collections;
import java.util.Comparator;

// Sort intervals by start, then by end
Arrays.sort(intervals, (a, b) . {
    if (a[0] != b[0]) return Integer.compare(a[0], b[0]);
    return Integer.compare(a[1], b[1]);
});

// Or with Comparator.comparing
Arrays.sort(people, Comparator.comparingInt(p . p[0]));
```

## Collections framework

Import from `java.util`.
<section class="template-diagrams" aria-label="Java collections map">
  <div class="template-diagram-grid">
    <figure class="template-diagram-card template-diagram-card-wide">
      <figcaption>
        <strong>Collections map</strong>
        <span>Interface hierarchy and the implementations you reach for on LeetCode.</span>
      </figcaption>
      {% include diagrams/java-collections-map.svg.html %}
    </figure>
  </div>
</section>

### `List` — ordered, allows duplicates

```java
// import java.util.*;
List<Integer> list = new ArrayList<>();
list.add(3);
list.add(1);
list.get(0);
```

### `Set` — unique elements

```java
// import java.util.*;
Set<Integer> set = new HashSet<>();      // O(1) average add/contains
set.add(1);
set.contains(1);

Set<Integer> tree = new TreeSet<>();     // sorted order
tree.add(5);
tree.add(2);
// iteration: 2, 5
```

### `Map` — key → value

```java
// import java.util.*;
Map<String, Integer> freq = new HashMap<>();
freq.put("a", 1);
freq.put("a", freq.getOrDefault("a", 0) + 1);
int count = freq.getOrDefault("z", 0);

for (Map.Entry<String, Integer> e : freq.entrySet()) {
    String key = e.getKey();
    int val = e.getValue();
}

for (String key : freq.keySet()) { }
for (int val : freq.values()) { }
```

`TreeMap` keeps keys sorted; `LinkedHashMap` preserves insertion order.

### Stack and queue

There is no `Stack` class in modern Java style — use `Deque`:

```java
// import java.util.*;
Deque<Integer> stack = new ArrayDeque<>();
stack.offer(1);
stack.poll();
stack.peek();

Queue<Integer> queue = new LinkedList<>();
queue.offer(1);
queue.poll();
queue.peek();
```

### Priority queue (heap)

Default is a **min-heap**:

```java
// import java.util.*;
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(3);
minHeap.offer(1);
minHeap.poll(); // 1

// max-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
```

Custom comparator (prefer `Integer.compare` over subtraction to avoid overflow):

```java
// import java.util.*;
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) . Integer.compare(a[0], b[0]));
```

## Sorting and binary search

```java
// import java.util.*;
// import java.util.Arrays;
// import java.util.Collections;
import java.util.Arrays;
import java.util.Collections;

int[] a = {3, 1, 4, 1, 5}
Arrays.sort(a);                          // ascending

Integer[] boxed = {3, 1, 4}
Arrays.sort(boxed, Collections.reverseOrder());

List<Integer> list = new ArrayList<>(List.of(3, 1, 4));
Collections.sort(list);

// binary search — array must be sorted
int idx = Arrays.binarySearch(a, 4);     // >= 0 if found, else insertion point
```

`Collections.binarySearch` works on sorted `List`s.

Math helpers:

```java
Math.max(a, b);
Math.min(a, b);
Math.abs(x);
(int) Math.sqrt(n);
```

## Common LeetCode definitions

These appear at the top of many problems:

```java
// Singly-linked list
class ListNode {
        int val;
    public ListNode next;
    public ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

// Binary tree
class TreeNode {
        int val;
    public TreeNode left;
    public TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

Graphs are usually `List<List<Integer>>` adjacency lists or `int[][]` grids.

## Sample usages

Short, complete examples showing how basics combine in real problems.

### HashMap — Two Sum (complement lookup)

```java
// import java.util.*;
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> index = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        if (index.containsKey(need)) {
            return new int[]{index.get(need), i}
        }
        index.put(nums[i], i);
    }
    return new int[]{}
}
```

**Why `HashMap`?** O(1) “have we seen `target - nums[i]`?” while scanning once.

### Deque — Valid Parentheses (stack)

```java
// import java.util.*;
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char ch : s.toCharArray()) {
        if (ch == '(') stack.offer(')');
        else if (ch == '[') stack.offer(']');
        else if (ch == '{') stack.offer('}');
        else if (stack.length == 0 || stack.poll() != ch) return false;
    }
    return stack.length == 0;
}
```

**Why `Deque`?** LIFO matching — push expected closing bracket, pop on open counterpart.

### HashMap — frequency count (anagram / ransom note)

```java
public boolean canConstruct(String ransomNote, String magazine) {
    int[] freq = new int[26];
    for (char ch : magazine.toCharArray()) freq[ch - 'a']++;
    for (char ch : ransomNote.toCharArray()) {
        if (--freq[ch - 'a'] < 0) return false;
    }
    return true;
}
```

**Why `int[26]`?** Fixed alphabet → array beats `HashMap` for speed and simplicity.

### BFS — grid shortest steps

```java
// import java.util.*;
public int orangesRotting(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    Queue<int[]> q = new LinkedList<>();
    int fresh = 0;
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 2) q.offer(new int[] {r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    }
    int minutes = 0;
    int[][] dirs = {new int[] {1, 0},{-1,0},new int[] {0, 1},{0,-1}}
    while (!q.isEmpty() && fresh > 0) {
        int size = q.size();
        for (int i = 0; i < size; i++) {
            int[] cell = q.poll();
            for (int[] d : dirs) {
                int nr = cell[0] + d[0], nc = cell[1] + d[1];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != 1) continue;
                grid[nr][nc] = 2;
                fresh--;
                q.offer(new int[] {nr, nc});
            }
        }
        minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

**Why `Queue`?** Process cells level by level — classic multi-source BFS.

### DFS + backtracking — subsets

```java
// import java.util.*;
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), res);
    return res;
}

private void dfs(int[] nums, int start, List<Integer> path, List<List<Integer>> res) {
    res.add(new ArrayList<>(path));
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);
        dfs(nums, i + 1, path, res);
        path.remove(path.size() - 1);
    }
}
```

**Why `ArrayList` path + copy?** Mutable path with undo (`remove`) and snapshot when recording a result.

## Common LeetCode templates

Copy-paste skeletons. Pair with the [LeetCode Templates](/blog_leetcode_java/leetcode-templates/) index for category-specific variants.
<section class="template-diagrams" aria-label="Java to LeetCode templates">
  <div class="template-diagram-grid">
    <figure class="template-diagram-card template-diagram-card-wide">
      <figcaption>
        <strong>Feature → template → problem</strong>
        <span>Same Java tools recur across many problem families.</span>
      </figcaption>
      {% include diagrams/java-leetcode-templates.svg.html %}
    </figure>
  </div>
</section>

### Two pointers (sorted array)

```java
int left = 0, right = nums.length - 1;
while (left < right) {
    int sum = nums[left] + nums[right];
    if (sum == target) { /* found */ break; }
    else if (sum < target) left++;
    else right--;
}
```

### Sliding window (variable size)

```java
// import java.util.*;
int left = 0, best = 0;
Map<Character, Integer> freq = new HashMap<>();
for (int right = 0; right < s.length(); right++) {
    char ch = s.charAt(right);
    freq.merge(ch, 1, Integer::sum);
    while (/* window invalid */) {
        char out = s.charAt(left++);
        freq.merge(out, -1, Integer::sum);
        if (freq.get(out) == 0) freq.remove(out);
    }
    best = Math.max(best, right - left + 1);
}
```

### Binary search (lower bound)

```java
int lo = 0, hi = n; // half-open [lo, hi)
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (predicate(mid)) hi = mid;
    else lo = mid + 1;
}
return lo; // first index where predicate is true
```

### Monotonic stack (next greater)

```java
// import java.util.*;
// import java.util.Arrays;
// import java.util.Collections;
Deque<Integer> stack = new ArrayDeque<>();
int[] ans = new int[n];
Arrays.fill(ans, -1);
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
        ans[stack.poll()] = nums[i];
    }
    stack.offer(i);
}
```

### Tree DFS (preorder)

```java
// import java.util.*;
static void dfs(TreeNode node, List<Integer> out) {
    if (node == null) return;
    out.add(node.val);
    dfs(node.left, out);
    dfs(node.right, out);
}
```

### Graph BFS (unweighted shortest path)

```java
// import java.util.*;
Queue<Integer> q = new LinkedList<>();
boolean[] seen = new boolean[n];
q.offer(start);
seen[start] = true;
while (!q.isEmpty()) {
    int u = q.poll();
    for (int v : graph.get(u)) {
        if (!seen[v]) {
            seen[v] = true;
            dist[v] = dist[u] + 1;
            q.offer(v);
        }
    }
}
```

### Dijkstra (non-negative weights)

```java
// import java.util.*;
// import java.util.Arrays;
// import java.util.Collections;
int[] dist = new int[n];
Arrays.fill(dist, Integer.MAX_VALUE);
dist[src] = 0;
PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a . a[1]));
pq.offer(new int[] {src, 0});
while (!pq.isEmpty()) {
    int[] cur = pq.poll();
    int u = cur[0], d = cur[1];
    if (d != dist[u]) continue;
    for (int[] e : adj.get(u)) {
        int v = e[0], w = e[1];
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            pq.offer(new int[]{v, dist[v]});
        }
    }
}
```

### Union-Find (connectivity)

```java
class DSU {
    public int[] parent, rank;
    DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (rank[ra] < rank[rb]) parent[ra] = rb;
        else if (rank[ra] > rank[rb]) parent[rb] = ra;
        else { parent[rb] = ra; rank.put(ra, rank.getOrDefault(ra, 0) + 1); }
        return true;
    }
}
```

## Modern Java (21 → 26)

LeetCode’s online judge typically supports a recent JDK (check the language dropdown on each problem). Locally, **Java 21** is a safe baseline; **Java 25** is the current LTS (Sept 2025); **Java 26** shipped March 2026 as the latest feature release.

### Release cadence

| Version | Type | GA date | Notes |
|---------|------|---------|-------|
| Java 21 | LTS | Sept 2023 | Records, pattern matching for `switch`, sequenced collections |
| Java 25 | LTS | Sept 2025 | Scoped values, compact main, module imports |
| Java 26 | Feature | Mar 2026 | HTTP/3 client, G1 tuning, preview JEPs |

### Features useful on LeetCode (Java 9–21)

Already widely available and worth using:

```java
// import java.util.*;
// Immutable small collections (Java 9+)
List<Integer> xs = List.of(1, 2, 3);
Map<String, Integer> m = Map.of("a", 1, "b", 2);

// var (Java 10+)
var map = new HashMap<String, List<Integer>>();

// Text block (Java 15+) — multi-line strings
String json = """
    {
      "key": "value"
    }
    """;

// Record (Java 16+)
record Edge(int to, int weight) {}

// Pattern matching for switch (Java 21, finalized)
static String classify(Object o) {
    return switch (o) {
        case Integer i when i < 0 . "negative";
        case Integer i . "non-negative int";
        case String s . "String: " + s;
        case null . "null";
        default . "other";
    }
}

// Sequenced collections (Java 21) — first/last on List/Deque
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
int first = list.get(0);
int last = list.get(list.size() - 1);
```

### Java 25 LTS highlights

Finalized in JDK 25 — mostly infrastructure, but a few affect how you write small programs:

- **JEP 506: Scoped Values** — safer alternative to `ThreadLocal` for passing context (less relevant to single-threaded LeetCode).
- **JEP 511: Module Import Declarations** — `import module java.base;` style bulk imports for scripts.
- **JEP 512: Compact Source Files and Instance Main Methods** — beginners can write `void main()` without `public static`.
- **JEP 513: Flexible Constructor Bodies** — run statements before `super()` / `this()` in constructors.
- **JEP 519: Compact Object Headers** — lower heap overhead (runtime, invisible in solutions).

**Preview in 25:** primitive types in `switch` / `instanceof` patterns (JEP 507) — evolves further in 26.

```java
// Preview: primitive pattern in switch (JDK 25+, preview feature)
static String sign(int x) {
    return switch (x) {
        case 0 . "zero";
        case int v when v > 0 . "positive";
        case int v . "negative";
    }
}
```

### Java 26 (current, June 2026)

Latest non-LTS release. Most changes are JVM, security, and HTTP client — not algorithm APIs:

| JEP | Area | Summary |
|-----|------|---------|
| 500 | Language | Prepare stricter `final` field semantics |
| 504 | Client | Remove Applet API |
| 516 | Runtime | AOT object caching with any GC |
| 517 | HTTP | HTTP/3 support in `HttpClient` |
| 522 | GC | G1 throughput improvements |
| 525 | Concurrency | Structured Concurrency (preview) |
| 526 | Language | Lazy Constants (preview) |
| 530 | Language | Primitive patterns in `switch` (4th preview) |

For competitive programming, **you rarely need preview features** — stick to finalized syntax unless you control the JDK flags. Records, modern `switch`, `List.of`, and `var` cover most readability wins.

### What to pick for interviews

1. **Default to Java 8–compatible style** if the platform is unknown (`Comparator`, classic loops).
2. **Use Java 11+** `var`, `List.of` when allowed — less boilerplate.
3. **Use records and pattern `switch`** when on Java 21+ — clearer state and branching.
4. **Avoid preview/incubator APIs** in timed contests unless explicitly enabled.

## Tips and pitfalls

**Equality**

- `==` compares references for objects; use `.equals()` for `String`, `Integer`, etc.
- Arrays: use `Arrays.equals(a, b)` and `Arrays.deepEquals` for 2D.

**Modifying while iterating**

```java
// import java.util.*;
// Safe: build a new collection
List<Integer> kept = new ArrayList<>();
for (int x : nums) {
    if (x > 0) kept.add(x);
}
```

**Integer overflow**

```java
// wrong for large sums
// int s = a + b;

long s = (long) a + b;
```

**Comparator overflow**

```java
// import java.util.*;
// risky: a[0] - b[0] overflows
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) . Integer.compare(a[0], b[0]));
```

**`int[]` vs `Integer[]`**

LeetCode usually uses `int[]`. Autoboxing to `Integer[]` adds overhead and is rarely needed.

**Imports on LeetCode**

Common imports are pre-added. Locally, keep these handy:

```java
import java.util.*;
```

**Bit tricks**

```java
int bits = Integer.bitCount(x);
int lowbit = x & -x;
int cleared = x & (x - 1);
```

---

## Next steps

- [← Java Guide hub](/blog_leetcode_java/java-guide/) — intro, learning path, and chapter index
- [Java Collections Quick Reference](/blog_leetcode_java/posts/2025-09-23-java-cheatsheet/) — cheat sheet for APIs used in contests
- [LeetCode Templates](/blog_leetcode_java/leetcode-templates/) — pattern index for common problem types
- [LeetCode Categories and Solution Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/) — master template guide
{% endraw %}
