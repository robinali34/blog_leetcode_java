---

layout: post
title: "Java Collections Quick Reference for LeetCode"
date: 2025-09-23 23:33:00 -0000
categories: leetcode algorithm java data-structures reference cheat-sheet programming java-collections containers iterators algorithms competitive-programming
permalink: /posts/2025-09-23-java-cheatsheet/
---

# Java Collections Quick Reference for LeetCode

Part of the [Java Guide]({{ '/java-guide/' | relative_url }}). See also [Language Basics]({{ '/posts/2026-06-24-java-guide-basics/' | relative_url }}) for a full tutorial.

---

## Strings

```java
String s = "abc";
s.length();
s.isEmpty();
s.charAt(i);
s.substring(start, end);
s.indexOf("ab");
s.equals("abc");
s + "def";
String.valueOf(42);
Integer.parseInt("42");
```

---

## Arrays

```java
int[] a = new int[n];
int[] b = {1, 2, 3};
a.length;
a[i] = 10;
Arrays.sort(a);
Arrays.fill(a, 0);
Arrays.copyOf(a, a.length);
Arrays.binarySearch(a, key);
```

---

## ArrayList / List

```java
List<Integer> list = new ArrayList<>();
list.add(x);
list.get(i);
list.set(i, x);
list.size();
list.remove(list.size() - 1);
Collections.sort(list);
```

---

## HashMap / HashSet

```java
Map<String, Integer> map = new HashMap<>();
map.put(key, val);
map.get(key);
map.getOrDefault(key, 0);
map.containsKey(key);
for (var e : map.entrySet()) { e.getKey(); e.getValue(); }

Set<Integer> set = new HashSet<>();
set.add(x);
set.contains(x);
```

---

## TreeMap / TreeSet (sorted)

```java
TreeMap<Integer, Integer> tm = new TreeMap<>();
tm.floorKey(x);
tm.ceilingKey(x);
TreeSet<Integer> ts = new TreeSet<>();
```

---

## Stack / Queue / Deque

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.offer(x);
stack.poll();
stack.peek();

Queue<Integer> q = new LinkedList<>();
q.offer(x);
q.poll();
q.peek();
```

---

## PriorityQueue (heap)

```java
// min-heap (default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
// max-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
minHeap.offer(x);
minHeap.poll();
minHeap.peek();
```

---

## Sorting & binary search

```java
Arrays.sort(arr);
Arrays.sort(arr, Collections.reverseOrder());
Collections.sort(list);
int idx = Arrays.binarySearch(arr, key); // arr must be sorted
Math.max(a, b);
Math.min(a, b);
Math.abs(x);
```

---

## Bit tricks

```java
Integer.bitCount(x);
Integer.numberOfLeadingZeros(x);
x & (x - 1);   // clear lowest set bit
x & -x;        // isolate lowest set bit
```

---

## Common LeetCode structures

| Concept    | Java equivalent        |
|-----------|-------------------------|
| Hash map  | `HashMap<K,V>`          |
| Hash set  | `HashSet<T>`            |
| Min heap  | `PriorityQueue<T>`      |
| Max heap  | `PriorityQueue` + `Comparator.reverseOrder()` |
| Stack     | `Deque<T>` / `ArrayDeque` |
| Queue     | `Queue<T>` / `LinkedList` |
| String builder | `StringBuilder`    |

---

## Imports (local development)

```java
import java.util.*;
```
