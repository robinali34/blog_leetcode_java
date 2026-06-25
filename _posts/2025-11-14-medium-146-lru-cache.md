---
layout: post
title: "[Medium] 146. LRU Cache"
date: 2025-11-15 00:00:00 -0800
categories: leetcode algorithm medium java design data-structures hash-map linked-list problem-solving
---

# [Medium] 146. LRU Cache

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.

Implement the `LRUCache` class:

- `LRUCache(int capacity)` Initialize the LRU cache with **positive** size `capacity`.
- `int get(int key)` Return the value of the `key` if the key exists, otherwise return `-1`.
- `void put(int key, int value)` Update the value of the `key` if the `key` exists. Otherwise, add the `key-value` pair to the cache. If the number of keys exceeds the `capacity` from this operation, **evict** the least recently used key.

The functions `get` and `put` must each run in **O(1)** average time complexity.

## Examples

**Example 1:**
```
Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
```

## Constraints

- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`
- `0 <= value <= 10^5`
- At most `2 * 10^5` calls will be made to `get` and `put`.

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **LRU definition**: What does "Least Recently Used" mean? (Assumption: The item that hasn't been accessed for the longest time - need to track access order)

2. **Cache operations**: What operations should the cache support? (Assumption: get(key) - retrieve value, put(key, value) - insert/update, both operations mark item as recently used)

3. **Eviction policy**: When should we evict items? (Assumption: When cache is full and we need to add a new item, evict the least recently used item)

4. **Capacity**: What is the cache capacity? (Assumption: Fixed capacity specified in constructor - cannot exceed this limit)

5. **Return values**: What should get() return if key doesn't exist? (Assumption: Return -1 - key not found in cache)

## Interview Deduction Process (20 minutes)

**Step 1: Brute-Force Approach (5 minutes)**

Use a hash map to store key-value pairs and a list/array to track access order. For `get`, search the list to find the key, move it to the end, and return the value. For `put`, add/update the hash map and move the key to the end of the list. When capacity is exceeded, remove the first element from the list. This approach has O(n) time for `get` operations due to list searching, which doesn't meet the O(1) requirement.

**Step 2: Semi-Optimized Approach (7 minutes)**

Use a hash map and a doubly linked list: hash map stores key-to-node mappings, doubly linked list maintains access order. For `get`, use hash map to find the node in O(1), move it to the end of the list. For `put`, add/update hash map, add node to end of list, remove head if capacity exceeded. However, implementing a doubly linked list from scratch requires careful pointer management and can be error-prone.

**Step 3: Optimized Solution (8 minutes)**

Use hash map + `LinkedList` / `LinkedHashMap`: hash map stores `key -> iterator` mappings, `LinkedList` / `LinkedHashMap` maintains access order with pairs `(key, value)`. For `get`, use hash map to get iterator in O(1), use `splice` to move node to end in O(1). For `put`, if key exists, update value and move to end. If new key, add to end and remove head if capacity exceeded. This achieves O(1) for both operations using standard library containers. The key insight is that `LinkedHashMap` move-to-end allows O(1) node movement, and hash map provides O(1) lookup, combining to achieve O(1) operations.

## Solution: Hash Map + Doubly Linked List (Java Optimized)

**Time Complexity:** O(1) for both `get` and `put`  
**Space Complexity:** O(capacity)

We use a combination of hash map and doubly linked list to achieve O(1) operations. The hash map stores key-to-node mappings, and the doubly linked list maintains the order of recently used items.

### Solution 1: Using list (Recommended - Java Optimized)

```java
// import java.util.*;
class LRUCache {
    public int capacity_;
    unordered_map<int, LinkedList<int[]>::iterator> cache_;
    LinkedList<int[]> lru_list_ = new LinkedList<int[]>();

    // Helper to move node to front (most recently used)
    public void moveToFront(LinkedList<int[]>::iterator it) {
        if (it != lru_list_.iterator()) {
            /* move to end */, lru_list_, it);
        }
    }
    explicit LRUCache(int capacity) {
        cache_.reserve(capacity_);  // Pre-allocate hash map
    }

    int get(int key) {
        var it = cache_.find(key);
        if (it == cache_.iterator()) {
            return -1;
        }

        // Move to front (most recently used)
        moveToFront(it.second);
        return it.second.second;
    }

    void put(int key, int value) {
        var it = cache_.find(key);

        if (it != cache_.iterator()) {
            // Update existing key
            it.second.second = value;
            moveToFront(it.second);
        } else {
            // Add new key
            if (cache_.size() >= capacity_) {
                // Evict least recently used (back of list)
                auto [lru_key, _] = lru_list_.getLast();
                cache_.remove(lru_key);
                lru_list_.removeLast();
            }

            // Insert at front
            lru_list_.emplace_front(key, value);
            cache_[key] = lru_list_.iterator();
        }
    }
}
```

### Solution 2: Custom Doubly Linked List (Java Optimized)

```java
class LRUCache {
    class Node {
        public int key;
        public int value;
        Node next;
        Node prev;

        Node(int k, int v) {}
    }
    int capacity_;
    unordered_map<int, Node> cache_;

    // Dummy head and tail for easier list manipulation
    unique_ptr<Node> head_;
    unique_ptr<Node> tail_;

    // Add node right before tail (most recently used)
    void addNode(Node node) {
        Node prev_end = tail_.prev;
        prev_end.next = node;
        node.prev = prev_end;
        node.next = tail_.get();
        tail_.prev = node;
    }

    // Remove node from list
    void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    // Move node to end (most recently used)
    void moveToEnd(Node node) {
        removeNode(node);
        addNode(node);
    }
    explicit LRUCache(int capacity) {
        head_.next = tail_.get();
        tail_.prev = head_.get();
        cache_.reserve(capacity_);
    }
    }

    // Delete copy constructor and assignment
    LRUCache(LRUCache) = delete;
    LRUCache operator=(LRUCache) = delete;

    int get(int key) {
        var it = cache_.find(key);
        if (it == cache_.iterator()) {
            return -1;
        }

        Node node = it.second;
        moveToEnd(node);
        return node.value;
    }

    void put(int key, int value) {
        var it = cache_.find(key);

        if (it != cache_.iterator()) {
            // Update existing
            Node node = it.second;
            node.value = value;
            moveToEnd(node);
        } else {
            // Add new
            if (cache_.size() >= capacity_) {
                // Evict least recently used (head.next)
                Node lru = head_.next;
                removeNode(lru);
                cache_.remove(lru.key);
                delete lru;
            }

            Node newNode = new Node(key, value);
            addNode(newNode);
            cache_[key] = newNode;
        }
    }
}
```

### Solution 3: Most Optimized with Move Semantics

```java
class LRUCache {
    public int capacity_;
    unordered_map<int, list<int[]>::iterator> cache_;
    list<int[]> lru_list_;
    explicit LRUCache(int capacity) {
        cache_.reserve(capacity_);
    }

    [[nodiscard]] int get(int key) {
        var it = cache_.find(key);
        if (it == cache_.iterator()) {
            return -1;
        }

        // Move to front using splice (O(1))
        /* move to end */, lru_list_, it.second);
        return it.second.second;
    }

    void put(int key, int value) {
        var it = cache_.find(key);

        if (it != cache_.iterator()) {
            // Update and move to front
            it.second.second = value;
            /* move to end */, lru_list_, it.second);
        } else {
            // Check capacity
            if (cache_.size() >= capacity_) {
                // Evict LRU (back of list)
                cache_.remove(lru_list_.getLast().first);
                lru_list_.removeLast();
            }

            // Insert at front
            lru_list_.emplace_front(key, value);
            cache_[key] = lru_list_.iterator();
        }
    }
}
```

## Key Optimizations (Java)

1. **`list::splice()`**: O(1) operation to move nodes without copying
2. **`unordered_map::reserve()`**: Pre-allocates hash map to avoid rehashing
3. **`explicit` constructor**: Prevents implicit conversions
4. **Structured bindings**: Cleaner code with `auto [key, value]`
5. **`emplace_front()`**: Constructs in-place, avoiding copies
6. **Move semantics**: Efficient transfer of ownership

## How the Algorithm Works

### Data Structure Design

```
Hash Map:          Doubly Linked List:
key -> iterator    [head] <-> [1,1] <-> [2,2] <-> [tail]
                   (LRU)                (MRU)
```

### Operation Flow

**Get Operation:**
1. Look up key in hash map → O(1)
2. If found, move node to front (most recently used) → O(1)
3. Return value

**Put Operation:**
1. Look up key in hash map → O(1)
2. If exists: update value and move to front → O(1)
3. If new:
   - Check capacity
   - If full: remove back node (LRU) → O(1)
   - Insert at front → O(1)

### Example Walkthrough

```
capacity = 2

put(1, 1):  cache = {1: [1,1]}
            list: [head] <-> [1,1] <-> [tail]

put(2, 2):  cache = {1: [1,1], 2: [2,2]}
            list: [head] <-> [1,1] <-> [2,2] <-> [tail]

get(1):     Move [1,1] to front
            list: [head] <-> [2,2] <-> [1,1] <-> [tail]
            return 1

put(3, 3):  Evict [2,2] (LRU), add [3,3] at front
            cache = {1: [1,1], 3: [3,3]}
            list: [head] <-> [3,3] <-> [1,1] <-> [tail]
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| `get(key)` | O(1) | O(1) |
| `put(key, value)` | O(1) | O(1) |
| **Overall** | **O(1)** | **O(capacity)** |

## Why `LinkedHashMap` is Preferred

1. **`splice()` is O(1)**: Moves nodes without copying
2. **Automatic memory management**: No manual node deletion
3. **Less error-prone**: No pointer management
4. **Better cache locality**: Standard library optimizations
5. **Cleaner code**: Less boilerplate

## Edge Cases

1. **Capacity = 1**: Only one item can exist
2. **Get non-existent key**: Returns -1
3. **Update existing key**: Moves to front, doesn't increase size
4. **Multiple puts**: Evicts oldest when capacity exceeded

## Common Mistakes

1. **Not moving to front on get**: Must update access order
2. **Wrong eviction order**: Remove from back (LRU), not front
3. **Memory leaks**: Forgetting to delete nodes in custom implementation
4. **Not updating iterator**: After list modification, iterators may be invalid
5. **Copying instead of moving**: Use `splice()` or move semantics

## Related Problems

- [460. LFU Cache](https://leetcode.com/problems/lfu-cache/) - Least Frequently Used
- [432. All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/)
- [588. Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/)

