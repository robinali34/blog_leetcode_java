---
layout: post
title: "Algorithm Templates: Data Structure Design"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates design
permalink: /posts/2025-11-24-leetcode-templates-data-structure-design/
tags: [leetcode, templates, design, data-structures]
---

{% raw %}
Minimal, copy-paste Java for LRU/LFU cache, Trie, time-based key-value store, and common design patterns.

## Contents

- [Stack-based Design](#stack-based-design)
- [LRU Cache](#lru-cache)
- [LFU Cache](#lfu-cache)
- [Trie](#trie)
- [Time-based Key-Value Store](#time-based-key-value-store)
- [Design Patterns](#design-patterns)

## Stack-based Design

### Min Stack
Maintain a primary stack for data and an auxiliary stack to track the minimum value at each state.

```java
// import java.util.*;
class MinStack {
    Deque<Integer> stk, minStk;
    public void push(int val) {
        stk.offer(val);
        if (minStk.length == 0) minStk.offer(val);
        else minStk.offer(Math.min(minStk.peek(), val));
    }
    public void pop() { stk.poll(); minStk.poll(); }
        public int top() { return stk.peek(); }
        public int getMin() { return minStk.peek(); }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 155 | Min Stack | [Link](https://leetcode.com/problems/min-stack/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/02/11/medium-155-min-stack/) |

## LRU Cache

Least Recently Used cache using hash map + doubly linked list.

```java
// import java.util.*;
class LRUCache {
        int capacity_;
    LinkedList<Integer> keyList_ = new LinkedList<Integer>();
    unordered_map<int, pair<int, LinkedList<Integer>::iterator>> hashMap_;

    public void insert(int key, int value) {
        keyList_.add(key);
        hashMap_[key] = new int[] {value, --keyList_.end(});
    }
    LRUCache(int capacity) {
    }
        public int get(int key) {
        var it = hashMap_.find(key);
        if(it != hashMap_.iterator()) {
            /* move to end */, keyList_, it[1].second);
            return it[1][0];
        }
        return -1;
    }

    public void put(int key, int value) {
        if(get(key) != -1) {
            hashMap_[key].first = value;
            return;
        }
        if(hashMap_.size() < capacity_) {
            insert(key, value);
        } else {
            int removeKey = keyList_.get(0);
            keyList_.removeFirst();
            hashMap_.remove(removeKey);
            insert(key, value);
        }
    }
}
/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache = new new(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
```

### Thread-Safe LRU Cache

Thread-safe version using mutex for concurrent access.

```java
// import java.util.*;

class ThreadSafeLRUCache {
        int capacity_;
    LinkedList<Integer> keyList_ = new LinkedList<Integer>();
    unordered_map<int, pair<int, LinkedList<Integer>::iterator>> hashMap_;
    mutable shared_mutex mtx_; // Use shared_mutex for read-write lock

    void insert(int key, int value) {
        keyList_.add(key);
        hashMap_[key] = new int[] {value, --keyList_.end(});
    }

    boolean exists(int key) {
        return hashMap_.find(key) != hashMap_.iterator();
    }
    ThreadSafeLRUCache(int capacity) {
    }

    int get(int key) {
         // Exclusive lock for read+modify
        var it = hashMap_.find(key);
        if(it != hashMap_.iterator()) {
            /* move to end */, keyList_, it[1].second);
            return it[1][0];
        }
        return -1;
    }

    void put(int key, int value) {
         // Exclusive lock for write
        if(exists(key)) {
            hashMap_[key].first = value;
            /* move to end */, keyList_, hashMap_[key].second);
            return;
        }
        if(hashMap_.size() < capacity_) {
            insert(key, value);
        } else {
            int removeKey = keyList_.get(0);
            keyList_.removeFirst();
            hashMap_.remove(removeKey);
            insert(key, value);
        }
    }

    size_t size() {
        shared_lock<shared_mutex> lock(mtx_);
        return hashMap_.size();
    }
}
// Example usage:
// ThreadSafeLRUCache cache = new ThreadSafeLRUCache(2);
// cache.put(1, 1);
// cache.put(2, 2);
// int val = cache.get(1); // returns 1
// cache.put(3, 3); // evicts key 2
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 146 | LRU Cache | [Link](https://leetcode.com/problems/lru-cache/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-14-medium-146-lru-cache/) |

## LFU Cache

Least Frequently Used cache.

```java
// import java.util.*;
class LFUCache {
        int capacity, minFreq;
    HashMap<Integer, int[]> keyValFreq = new HashMap<Integer, int[]>(); // key . new int[] {value, frequency}
    HashMap<Integer, LinkedList<Integer>> freqKeys = new HashMap<>(); // frequency . list of keys
    unordered_map<int, LinkedList<Integer>::iterator> keyIter; // key . iterator in freqKeys list

    void updateFreq(int key) {
        int freq = keyValFreq[key].second;
        freqKeys[freq].erase(keyIter[key]);

        if (freqKeys[freq].empty() && freq == minFreq) {
            minFreq++;
        }

        freq++;
        keyValFreq[key].second = freq;
        freqKeys.computeIfAbsent(freq, k.new ArrayList<>()).add(key);
        keyIter.put(key, --freqKeys[freq].end());
    }
    LFUCache(int capacity) {}

    int get(int key) {
        if (keyValFreq.find(key) == keyValFreq.iterator()) return -1;
        updateFreq(key);
        return keyValFreq[key].first;
    }

    void put(int key, int value) {
        if (capacity == 0) return;

        if (keyValFreq.find(key) != keyValFreq.iterator()) {
            keyValFreq[key].first = value;
            updateFreq(key);
        } else {
            if (keyValFreq.size() >= capacity) {
                int evictKey = freqKeys[minFreq].front();
                freqKeys[minFreq].pop_front();
                keyValFreq.remove(evictKey);
                keyIter.remove(evictKey);
            }

            keyValFreq.put(key, new int[] {value, 1});
            freqKeys.computeIfAbsent(1, k.new ArrayList<>()).add(key);
            keyIter.put(key, --freqKeys[1].end());
            minFreq = 1;
        }
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 460 | LFU Cache | [Link](https://leetcode.com/problems/lfu-cache/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-14-hard-460-lfu-cache/) |

## Trie

Prefix tree for efficient string operations.

```java
class Trie {
    class TrieNode {
        vector<TrieNode*> children;
        boolean isEnd;
        public TrieNode() {}
    }
    TrieNode root;
    Trie() {
        root = new TrieNode();
    }

    public void insert(String word) {
        TrieNode node = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!node.children[idx]) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }
        public boolean search(String word) {
        TrieNode node = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!node.children[idx]) return false;
            node = node.children[idx];
        }
        return node.isEnd;
    }
        public boolean startsWith(String prefix) {
        TrieNode node = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!node.children[idx]) return false;
            node = node.children[idx];
        }
        return true;
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 208 | Implement Trie (Prefix Tree) | [Link](https://leetcode.com/problems/implement-trie-prefix-tree/) | - |
| 211 | Design Add and Search Words Data Structure | [Link](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | - |

## Time-based Key-Value Store

```java
// import java.util.*;
class TimeMap {
    unordered_map<String, List<int[]>> store;
    TimeMap() {}

    void set(String key, String value, int timestamp) {
        store.computeIfAbsent(key, k.new ArrayList<>()).add(new int[] {timestamp, value});
    }

    String get(String key, int timestamp) {
        if (store.find(key) == store.iterator()) return "";

        var pairs = store[key];
        int left = 0, right = pairs.size() - 1;
        String result = "";

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (pairs[mid].first <= timestamp) {
                result = pairs[mid].second;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return result;
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 981 | Time Based Key-Value Store | [Link](https://leetcode.com/problems/time-based-key-value-store/) | - |
| 362 | Design Hit Counter | [Link](https://leetcode.com/problems/design-hit-counter/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/18/medium-362-design-hit-counter/) |
| 1146 | Snapshot Array | [Link](https://leetcode.com/problems/snapshot-array/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/19/medium-1146-snapshot-array/) |

## Design Patterns

### Random Pick with Weight

```java
class Solution {
    List<Integer> prefixSum = new ArrayList<>();
    Solution(int[] w) {
        prefixSum.add(0);
        for (int weight : w) {
            prefixSum.add(prefixSum.get(prefixSum.size() - 1) + weight);
        }
    }
        public int pickIndex() {
        int target = new Random().nextInt() % prefixSum.get(prefixSum.size() - 1);
        return binary search (upper bound)(prefixSum /* elements of prefixSum */, target) - prefixSum.iterator() - 1;
    }
}
```

### Design Tic-Tac-Toe

```java
class TicTacToe {
    int[]rows, cols;
        int diagonal, antiDiagonal;
        int n;
    TicTacToe(int n) {}

    int move(int row, int col, int player) {
        int add = (player == 1) ? 1 : -1;

        rows.put(row, rows.getOrDefault(row, 0) + add;
        cols.put(col, cols.getOrDefault(col, 0) + add;

        if (row == col) diagonal += add;
        if (row + col == n - 1) antiDiagonal += add;

        if (abs(rows[row]) == n || abs(cols[col]) == n ||
            abs(diagonal) == n || abs(antiDiagonal) == n) {
            return player;
        }

        return 0;
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 528 | Random Pick with Weight | [Link](https://leetcode.com/problems/random-pick-with-weight/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-24-medium-528-random-pick-with-weight/) |
| 348 | Design Tic-Tac-Toe | [Link](https://leetcode.com/problems/design-tic-tac-toe/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/04/medium-348-design-tic-tac-toe/) |
| 1275 | Find Winner on a Tic Tac Toe Game | [Link](https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/04/easy-1275-find-winner-on-a-tic-tac-toe-game/) |
| 398 | Random Pick Index | [Link](https://leetcode.com/problems/random-pick-index/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-24-medium-398-random-pick-index/) |
| 2043 | Simple Bank System | [Link](https://leetcode.com/problems/simple-bank-system/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/20/medium-2043-simple-bank-system/) |
| 281 | Zigzag Iterator | [Link](https://leetcode.com/problems/zigzag-iterator/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-10-medium-281-zigzag-iterator/) |
| 1206 | Design Skiplist | [Link](https://leetcode.com/problems/design-skiplist/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-03-hard-1206-design-skiplist/) |
| 341 | Flatten Nested List Iterator | [Link](https://leetcode.com/problems/flatten-nested-list-iterator/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/24/medium-341-flatten-nested-list-iterator/) |
| 1115 | Print FooBar Alternately | [Link](https://leetcode.com/problems/print-foobar-alternately/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/28/medium-1115-print-foobar-alternately/) |
| 1188 | Design Bounded Blocking Queue | [Link](https://leetcode.com/problems/design-bounded-blocking-queue/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/29/medium-1188-design-bounded-blocking-queue/) |

## More templates

- **Data structures (Trie, segment tree):** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}

