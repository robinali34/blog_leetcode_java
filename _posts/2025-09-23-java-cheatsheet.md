---
layout: post
title: "Java Collections Quick Reference for LeetCode"
date: 2025-09-23 23:33:00 -0000
categories: leetcode algorithm java data-structures reference cheat-sheet programming java-collections containers iterators algorithms competitive-programming
---

# 📚 Java Collections Quick Reference for LeetCode

---

## 🧰 Containers

### ✅ Strings

```java
s.length();         // Length of the String
s.size();           // Same as length()
s.length == 0;          // Checks if String is empty
s[i];               // Access character at index
s.substr(pos, len); // Substring
s.find("abc");      // Find position of substring
s.remove(pos, len);  // Erase part of String
s.add(pos, str); // Insert str at pos
s += "abc";         // Append
to_string(x);       // Convert int to String
stoi(s);            // Convert String to int
```

---

### ✅ Dynamic Arrays (`ArrayList` / `int[]`)

```java
// import java.util.Arrays;
// import java.util.Collections;
v.size();
v.length == 0;
v.add(x);
v.removeLast();
v[i];
v.getFirst();
v.getLast();
v.clear();
v.add(it, x);
v.remove(it);
Arrays.sort(v);
reverse(v /* elements of v */);
```

---

### ✅ Arrays

```java
int arr[100]; // C-style
array<int, 5> a = {1, 2, 3, 4, 5}
```

---

### ✅ Sets / Multisets

```java
// import java.util.*;
TreeSet<Integer> s;
s.add(x);
s.remove(x);
s.find(x);
s.count(x);          // 0 or 1 (set), >1 for multiset
s.binary search (lower bound)(x);    // >= x
s.binary search (upper bound)(x);    // > x
```

---

### ✅ Maps / Unordered Maps

```java
// import java.util.*;
TreeMap<Integer, Integer> m;
HashMap<Integer, Integer> um = new HashMap<Integer, Integer>();

m.put(key, val);
m.count(key);
m.find(key);
for (auto& [k, v] : m) {
    // Map entry iteration
}
```

---

## 🔄 Algorithms (`java.util.Arrays` / `Collections`)

### ✅ Sorting & Searching

```java
// import java.util.Arrays;
// import java.util.Collections;
Arrays.sort(v);
sort(v.rbegin(), v.rend());
reverse(v /* elements of v */);
binary_search(v /* elements of v */, x);
binary search (lower bound)(v /* elements of v */, x);
binary search (upper bound)(v /* elements of v */, x);
```

---

### ✅ Min / Max / Others

```java
Math.min(a, b);
Math.max(a, b);
swap(a, b);
accumulate(v /* elements of v */, 0); // Sum
count(v /* elements of v */, x);
next_permutation(v /* elements of v */);
prev_permutation(v /* elements of v */);
unique(v /* elements of v */); // Remove dupes (after sort)
rotate(v.iterator(), v.iterator() + k, v.iterator());
```

---

## 📐 Math Utilities (`Math` class)

```java
abs(x);
pow(a, b);
sqrt(x);
gcd(a, b);   // Java
lcm(a, b);   // Java
```

---

## 🧵 Queues, Stacks, Deques

### ✅ Queue

```java
// import java.util.*;
Queue<Integer> q = new LinkedList<>();
q.push(x);
q.pop();
q.getFirst();
q.getLast();
q.length == 0;
```

### ✅ Stack

```java
// import java.util.*;
Deque<Integer> s = new ArrayDeque<>();
s.push(x);
s.pop();
s.top();
s.length == 0;
```

### ✅ Deque

```java
// import java.util.*;
ArrayDeque<Integer> dq = new ArrayDeque<>();
dq.push_front(x);
dq.add(x);
dq.removeFirst();
dq.removeLast();
```

### ✅ Priority Queue (Heap)

```java
// import java.util.*;
PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>();
priority_queue<int, int[], greater<int>> minHeap;
```

---

## 🧠 Bit Manipulation

```java
Integer.bitCount(x);  // Count 1-bits
__builtin_clz(x);       // Leading zeros
__builtin_ctz(x);       // Trailing zeros
x & (x - 1);            // Remove lowest 1-bit
x & -x;                 // Isolate lowest 1-bit
```

---

## 📌 Common LeetCode Structures

| Concept       | Java Equivalent              |
|--------------|------------------------------|
| Hash Map     | `HashMap<K, V>`         |
| Hash Set     | `HashSet<T>`            |
| Tree Map     | `TreeMap<K, V>`                   |
| Tree Set     | `TreeSet<T>`                      |
| Min Heap     | `PriorityQueue<T>` with comparator |
| Max Heap     | `PriorityQueue<T>`           |
| Stack        | `Deque<T>`                    |
| Queue        | `Queue<T>`                    |
| Deque        | `ArrayDeque<T>`                    |
| StringBuilder| `StringBuilder`       |
| Graph        | `int[][]` / `List<List<Integer>>`         |

---

## ✍️ Input/Output Tips

```java
cin >> n;
getline(cin, s);      // Full line
stoi(s);              // String to int

// Fast IO
ios::sync_with_stdio(false);
cin.tie(0);
```

---
