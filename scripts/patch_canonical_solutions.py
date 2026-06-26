#!/usr/bin/env python3
"""Replace broken primary Java solutions with canonical LeetCode implementations."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK = re.compile(r"```java\s*\n.*?```", re.DOTALL)
CPP = re.compile(
    r"vector<|unordered_map|push_back|begin\(|to_string\(|priority_queue<|"
    r"__builtin_|pair<|greater<|for\s*\(\s*auto\b|count_map\[|\.first\b|\.second\b",
)

# problem_number -> canonical Solution (must compile on LeetCode)
CANONICAL: dict[str, str] = {
    "347": '''```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) {
            freq.put(num, freq.getOrDefault(num, 0) + 1);
        }
        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i <= nums.length; i++) {
            buckets.add(new ArrayList<>());
        }
        for (var e : freq.entrySet()) {
            buckets.get(e.getValue()).add(e.getKey());
        }
        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.size() - 1; i >= 0 && idx < k; i--) {
            for (int num : buckets.get(i)) {
                result[idx++] = num;
                if (idx == k) return result;
            }
        }
        return result;
    }
}
```''',
    "49": '''```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) count[c - 'a']++;
            StringBuilder key = new StringBuilder();
            for (int n : count) {
                key.append('#').append(n);
            }
            groups.computeIfAbsent(key.toString(), x -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(groups.values());
    }
}
```''',
    "146": '''```java
class LRUCache {
    private final int cap;
    private final Map<Integer, Integer> map = new LinkedHashMap<>(16, 0.75f, true);

    public LRUCache(int capacity) {
        cap = capacity;
    }

    public int get(int key) {
        return map.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            map.remove(key);
        } else if (map.size() == cap) {
            int eldest = map.keySet().iterator().next();
            map.remove(eldest);
        }
        map.put(key, value);
    }
}
```''',
    "20": '''```java
class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char ch : s.toCharArray()) {
            if (ch == '(') stack.push(')');
            else if (ch == '[') stack.push(']');
            else if (ch == '{') stack.push('}');
            else if (stack.isEmpty() || stack.pop() != ch) return false;
        }
        return stack.isEmpty();
    }
}
```''',
    "239": '''```java
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> dq = new ArrayDeque<>();
        int[] result = new int[nums.length - k + 1];
        for (int i = 0; i < nums.length; i++) {
            while (!dq.isEmpty() && dq.peekFirst() < i - k + 1) dq.pollFirst();
            while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
            dq.offerLast(i);
            if (i >= k - 1) result[i - k + 1] = nums[dq.peekFirst()];
        }
        return result;
    }
}
```''',
    "215": '''```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }
        return minHeap.peek();
    }
}
```''',
    "200": '''```java
class Solution {
    public int numIslands(char[][] grid) {
        int rows = grid.length, cols = grid[0].length, count = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    count++;
                    dfs(grid, r, c);
                }
            }
        }
        return count;
    }

    private void dfs(char[][] grid, int r, int c) {
        if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length || grid[r][c] != '1') return;
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
}
```''',
    "3": '''```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> last = new HashMap<>();
        int best = 0, left = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (last.containsKey(ch)) {
                left = Math.max(left, last.get(ch) + 1);
            }
            last.put(ch, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
}
```''',
}


def problem_number(path: Path) -> str | None:
    m = re.search(r"-(\d+)-", path.name)
    return m.group(1) if m else None


def patch_file(path: Path) -> bool:
    num = problem_number(path)
    if not num or num not in CANONICAL:
        return False
    text = path.read_text(encoding="utf-8")
    if not CPP.search(text):
        return False

    canonical = CANONICAL[num]
    # Replace first broken java block after "Solution in Java"
    marker = "## Solution in Java"
    if marker not in text:
        return False
    head, tail = text.split(marker, 1)
    m = JAVA_BLOCK.search(tail)
    if not m or not CPP.search(m.group(0)):
        return False
    new_tail = tail[: m.start()] + canonical + tail[m.end() :]
    path.write_text(head + marker + new_tail, encoding="utf-8")
    return True


def main() -> None:
    n = sum(1 for p in ROOT.glob("_posts/*.md") if patch_file(p))
    print(f"Patched {n} posts with canonical solutions")


if __name__ == "__main__":
    main()
