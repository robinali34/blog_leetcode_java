---
layout: post
title: "Java Guide: Language Basics"
date: 2026-06-24 10:00:00 -0700
categories: java guide reference tutorial programming fundamentals
permalink: /posts/2026-06-24-java-guide-basics/
tags: [java, guide, basics, tutorial, leetcode, collections, arrays, strings, oop, templates, java-25, java-26]
---

{% raw %}
# Java Guide: Language Basics

Part of the [Java Guide](/blog_leetcode_java/java-guide/) — practical Java for algorithm problems, from language fundamentals to copy-paste templates and modern releases. For a compact API lookup, see the [Java Collections Quick Reference](/blog_leetcode_java/posts/2025-09-23-java-cheatsheet/).

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

{% endraw %}

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

{% raw %}

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

{% endraw %}

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

{% raw %}

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

{% endraw %}

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

{% raw %}

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
