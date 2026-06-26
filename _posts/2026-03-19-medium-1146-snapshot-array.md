---
layout: post
title: "[Medium] 1146. Snapshot Array"
date: 2026-03-19
categories: [leetcode, medium, design, binary-search]
tags: [leetcode, medium, design, binary-search, map]
permalink: /2026/03/19/medium-1146-snapshot-array/
---

Implement a `SnapshotArray` that supports:
- `SnapshotArray(int length)` -- initializes an array of the given length (all zeros)
- `void set(index, val)` -- sets the element at `index` to `val`
- `int snap()` -- takes a snapshot, returns the `snap_id` (starting from 0)
- `int get(index, snap_id)` -- returns the value at `index` at the time of the given snapshot

## Examples

**Example 1:**

```
Input:
  SnapshotArray(3), set(0,5), snap(), set(0,6), get(0,0)
Output:
  null, null, 0, null, 5
Explanation:
  set(0,5) → arr = [5,0,0]
  snap()   → snap_id 0 captures [5,0,0]
  set(0,6) → arr = [6,0,0]
  get(0,0) → value at index 0 in snap 0 = 5
```

## Constraints

- `1 <= length <= 5 * 10^4`
- `0 <= index < length`
- `0 <= val <= 10^9`
- `0 <= snap_id <` (number of times `snap()` was called)
- At most `5 * 10^4` calls to `set`, `snap`, and `get`

## Thinking Process

### Naive: Copy Entire Array -- $O(n)$ per snap

The simplest approach: maintain a working array and copy it on every `snap()`.

- `set`: $O(1)$
- `snap`: $O(n)$ -- copies the full array
- `get`: $O(1)$

This works but is **too slow and memory-heavy** when there are many snapshots and a large array, especially if only a few elements change between snaps.

### Bottleneck

Copying the entire array on every snapshot, even when most values haven't changed.

### Optimization: Store Only Changes

Instead of copying the full array, for each index store a **sorted log** of `(snap_id, value)` pairs -- only recording when a value actually changes.

On `get(index, snap_id)`: binary search for the latest entry at or before `snap_id`.

A `map<int,int>` per index gives this naturally with `binary search (upper bound)`.

## Solution 1: Naive (Copy Array) -- $O(n)$ per snap

{% raw %}
```java
class SnapshotArray {
    SnapshotArray(int length) {
        arr.resize(length);
    }

    void set(int index, int val) {
        arr[index] = val;
    }

    int snap() {
        int id = snaps.size();
        snaps.add(arr);
        return id;
    }

    int get(int index, int snap_id) {
        return snaps[snap_id][index];
    }
    List<int[]> snaps = new ArrayList<>();
    List<Integer> arr = new ArrayList<>();
}
```
{% endraw %}

| Operation | Time | Space |
|---|---|---|
| `set` | $O(1)$ | -- |
| `snap` | $O(n)$ | $O(n)$ per snapshot |
| `get` | $O(1)$ | -- |

Works for small inputs but TLEs / MLEs with many snapshots.

## Solution 2: Map per Index + Binary Search (Optimal) -- $O(\log S)$ per get

Each index stores a `map<snap_id, value>`. Only write when `set` is called. On `get`, find the latest snapshot at or before the queried `snap_id` using `binary search (upper bound)`.

{% raw %}
```java
// import java.util.*;
class SnapshotArray {
    SnapshotArray(int length) {
        snap_id = 0;
        data.resize(length);
        for (int i = 0; i < length; ++i) {
            data[i][0] = 0;
        }
    }

    void set(int index, int val) {
        data[index][snap_id] = val;
    }

    int snap() {
        return snap_id++;
    }

    int get(int index, int snap_id) {
        var it = data[index].binary search (upper bound)(snap_id);
        if (it == data[index].begin()) return 0;
        --it;
        return it[1];
    }
    int snap_id;
    vector<TreeMap<Integer, Integer>> data;
}
```
{% endraw %}

| Operation | Time | Space |
|---|---|---|
| `set` | $O(\log S)$ | -- |
| `snap` | $O(1)$ | -- |
| `get` | $O(\log S)$ | -- |

Where $S$ = number of `set` calls on that index.

### Why `binary search (upper bound)` then `--it`?

`binary search (upper bound)(snap_id)` returns the first entry **strictly greater** than `snap_id`. Stepping back one gives the latest entry at or before `snap_id` -- exactly the value that was active at that snapshot.

```
data[0] = {0: 5, 3: 10, 7: 2}

get(0, 5):
  binary search (upper bound)(5) → points to {7: 2}
  --it → {3: 10}
  return 10  ✓  (snap 3 was the last set before snap 5)
```

## Comparison

| Approach | `set` | `snap` | `get` | Space |
|---|---|---|---|---|
| Copy Array | $O(1)$ | $O(n)$ | $O(1)$ | $O(n \cdot \text{snaps})$ |
| Map + Binary Search | $O(\log S)$ | $O(1)$ | $O(\log S)$ | $O(\text{total sets})$ |

The map approach wins when snapshots are frequent but changes are sparse.

## Common Mistakes

- Forgetting to initialize `data[i][0] = 0` (without it, `get` on an index that was never set returns garbage)
- Using `binary search (lower bound)` instead of `binary search (upper bound)` (off-by-one on the snap boundary)
- Storing snapshots in the wrong direction (value at snap time, not snap at value time)

## Key Takeaways

- **"Versioned data with sparse updates"** = store change log per element + binary search
- `binary search (upper bound)` then decrement is the standard pattern for "latest version at or before X"
- The optimization from $O(n)$ snap to $O(1)$ snap comes from only recording diffs, not full copies

## Related Problems

- [981. Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) -- same binary search on timestamps
- [362. Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) -- time-based design
- [155. Min Stack](https://leetcode.com/problems/min-stack/) -- data structure design with history

## Template Reference

- [Data Structure Design](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-data-structure-design/)
