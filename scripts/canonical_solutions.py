"""Known-good Java solutions keyed by LeetCode problem number (from post filenames)."""

CANONICAL: dict[str, list[str]] = {
    "3": [
        """class Solution {
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
}"""
    ],
    "20": [
        """class Solution {
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
}"""
    ],
    "49": [
        """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) count[c - 'a']++;
            StringBuilder key = new StringBuilder();
            for (int n : count) key.append('#').append(n);
            groups.computeIfAbsent(key.toString(), x -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(groups.values());
    }
}"""
    ],
    "133": [
        """class Solution {
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Node, Node> map = new HashMap<>();
        return dfs(node, map);
    }

    private Node dfs(Node node, Map<Node, Node> map) {
        if (map.containsKey(node)) return map.get(node);
        Node copy = new Node(node.val);
        map.put(node, copy);
        for (Node nei : node.neighbors) {
            copy.neighbors.add(dfs(nei, map));
        }
        return copy;
    }
}"""
    ],
    "146": [
        """class LRUCache {
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
}""",
        """class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);

    public LRUCache(int capacity) {
        cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToEnd(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToEnd(node);
            return;
        }
        if (map.size() == cap) {
            Node lru = head.next;
            remove(lru);
            map.remove(lru.key);
        }
        Node node = new Node(key, value);
        map.put(key, node);
        insertEnd(node);
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertEnd(Node node) {
        node.prev = tail.prev;
        node.next = tail;
        tail.prev.next = node;
        tail.prev = node;
    }

    private void moveToEnd(Node node) {
        remove(node);
        insertEnd(node);
    }
}""",
    ],
    "200": [
        """class Solution {
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
}"""
    ],
    "207": [
        """class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        int[] indeg = new int[numCourses];
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        for (int[] p : prerequisites) {
            graph.get(p[1]).add(p[0]);
            indeg[p[0]]++;
        }
        ArrayDeque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < numCourses; i++) if (indeg[i] == 0) q.offer(i);
        int seen = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            seen++;
            for (int v : graph.get(u)) {
                if (--indeg[v] == 0) q.offer(v);
            }
        }
        return seen == numCourses;
    }
}"""
    ],
    "215": [
        """class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }
        return minHeap.peek();
    }
}"""
    ],
    "239": [
        """class Solution {
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
}"""
    ],
    "347": [
        """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i <= nums.length; i++) buckets.add(new ArrayList<>());
        for (var e : freq.entrySet()) buckets.get(e.getValue()).add(e.getKey());
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
}""",
        """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        List<Integer> unique = new ArrayList<>(freq.keySet());
        quickselect(unique, freq, 0, unique.size() - 1, unique.size() - k);
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = unique.get(unique.size() - k + i);
        return result;
    }

    private void quickselect(List<Integer> arr, Map<Integer, Integer> freq, int l, int r, int k) {
        if (l >= r) return;
        int pivot = l + new Random().nextInt(r - l + 1);
        int p = partition(arr, freq, l, r, pivot);
        if (p == k) return;
        if (k < p) quickselect(arr, freq, l, p - 1, k);
        else quickselect(arr, freq, p + 1, r, k);
    }

    private int partition(List<Integer> arr, Map<Integer, Integer> freq, int l, int r, int pivotIdx) {
        int pivotFreq = freq.get(arr.get(pivotIdx));
        swap(arr, pivotIdx, r);
        int store = l;
        for (int i = l; i < r; i++) {
            if (freq.get(arr.get(i)) < pivotFreq) {
                swap(arr, store, i);
                store++;
            }
        }
        swap(arr, store, r);
        return store;
    }

    private void swap(List<Integer> arr, int i, int j) {
        int tmp = arr.get(i);
        arr.set(i, arr.get(j));
        arr.set(j, tmp);
    }
}""",
        """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        for (var e : freq.entrySet()) {
            minHeap.offer(new int[] {e.getValue(), e.getKey()});
            if (minHeap.size() > k) minHeap.poll();
        }
        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) result[i] = minHeap.poll()[1];
        return result;
    }
}""",
        """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        for (var e : freq.entrySet()) maxHeap.offer(new int[] {e.getValue(), e.getKey()});
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = maxHeap.poll()[1];
        return result;
    }
}""",
    ],
    "460": [
        """class LFUCache {
    private final int cap;
    private int minFreq;
    private final Map<Integer, Integer> keyToVal = new HashMap<>();
    private final Map<Integer, Integer> keyToFreq = new HashMap<>();
    private final Map<Integer, LinkedHashSet<Integer>> freqToKeys = new HashMap<>();

    public LFUCache(int capacity) {
        cap = capacity;
    }

    public int get(int key) {
        if (!keyToVal.containsKey(key)) return -1;
        bump(key);
        return keyToVal.get(key);
    }

    public void put(int key, int value) {
        if (cap == 0) return;
        if (keyToVal.containsKey(key)) {
            keyToVal.put(key, value);
            bump(key);
            return;
        }
        if (keyToVal.size() == cap) {
            int evict = freqToKeys.get(minFreq).iterator().next();
            freqToKeys.get(minFreq).remove(evict);
            keyToVal.remove(evict);
            keyToFreq.remove(evict);
        }
        keyToVal.put(key, value);
        keyToFreq.put(key, 1);
        freqToKeys.computeIfAbsent(1, x -> new LinkedHashSet<>()).add(key);
        minFreq = 1;
    }

    private void bump(int key) {
        int f = keyToFreq.get(key);
        freqToKeys.get(f).remove(key);
        if (freqToKeys.get(f).isEmpty() && f == minFreq) minFreq++;
        keyToFreq.put(key, f + 1);
        freqToKeys.computeIfAbsent(f + 1, x -> new LinkedHashSet<>()).add(key);
    }
}"""
    ],
    "692": [
        """class Solution {
    public List<String> topKFrequent(String[] words, int k) {
        Map<String, Integer> freq = new HashMap<>();
        for (String w : words) freq.put(w, freq.getOrDefault(w, 0) + 1);
        PriorityQueue<String> pq = new PriorityQueue<>((a, b) -> {
            int fa = freq.get(a), fb = freq.get(b);
            if (fa != fb) return Integer.compare(fa, fb);
            return b.compareTo(a);
        });
        for (String w : freq.keySet()) {
            pq.offer(w);
            if (pq.size() > k) pq.poll();
        }
        List<String> result = new ArrayList<>();
        while (!pq.isEmpty()) result.add(pq.poll());
        Collections.reverse(result);
        return result;
    }
}"""
    ],
    "743": [
        """class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        List<List<int[]>> graph = new ArrayList<>();
        for (int i = 0; i <= n; i++) graph.add(new ArrayList<>());
        for (int[] t : times) graph.get(t[0]).add(new int[] {t[1], t[2]});
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.offer(new int[] {0, k});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int d = cur[0], u = cur[1];
            if (d > dist[u]) continue;
            for (int[] e : graph.get(u)) {
                int v = e[0], w = e[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.offer(new int[] {dist[v], v});
                }
            }
        }
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) return -1;
            ans = Math.max(ans, dist[i]);
        }
        return ans;
    }
}"""
    ],
    "787": [
        """class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;
        for (int i = 0; i <= k; i++) {
            int[] next = dist.clone();
            for (int[] f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < next[v]) {
                    next[v] = dist[u] + w;
                }
            }
            dist = next;
        }
        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }
}"""
    ],
    "973": [
        """class Solution {
    public int[][] kClosest(int[][] points, int k) {
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> {
            int da = a[0] * a[0] + a[1] * a[1];
            int db = b[0] * b[0] + b[1] * b[1];
            return Integer.compare(db, da);
        });
        for (int[] p : points) {
            maxHeap.offer(p);
            if (maxHeap.size() > k) maxHeap.poll();
        }
        int[][] result = new int[k][2];
        for (int i = k - 1; i >= 0; i--) result[i] = maxHeap.poll();
        return result;
    }
}"""
    ],
    "721": [
        """class Solution {
    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        Map<String, String> parent = new HashMap<>();
        Map<String, String> emailToName = new HashMap<>();
        for (List<String> acc : accounts) {
            String name = acc.get(0);
            for (int i = 1; i < acc.size(); i++) {
                emailToName.put(acc.get(i), name);
                if (i == 1) parent.put(acc.get(i), acc.get(i));
                else union(parent, acc.get(1), acc.get(i));
            }
        }
        Map<String, TreeSet<String>> groups = new HashMap<>();
        for (String email : parent.keySet()) {
            String root = find(parent, email);
            groups.computeIfAbsent(root, x -> new TreeSet<>()).add(email);
        }
        List<List<String>> result = new ArrayList<>();
        for (var e : groups.entrySet()) {
            List<String> row = new ArrayList<>();
            row.add(emailToName.get(e.getKey()));
            row.addAll(e.getValue());
            result.add(row);
        }
        return result;
    }

    private String find(Map<String, String> p, String x) {
        if (!p.get(x).equals(x)) p.put(x, find(p, p.get(x)));
        return p.get(x);
    }

    private void union(Map<String, String> p, String a, String b) {
        p.put(find(p, b), find(p, a));
    }
}"""
    ],
    "323": [
        """class Solution {
    public int countComponents(int n, int[][] edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int comps = n;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a != b) {
                parent[a] = b;
                comps--;
            }
        }
        return comps;
    }

    private int find(int[] p, int x) {
        if (p[x] != x) p[x] = find(p, p[x]);
        return p[x];
    }
}"""
    ],
    "684": [
        """class Solution {
    public int[] findRedundantConnection(int[][] edges) {
        int[] parent = new int[edges.length + 1];
        for (int i = 0; i < parent.length; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a == b) return e;
            parent[a] = b;
        }
        return new int[0];
    }

    private int find(int[] p, int x) {
        if (p[x] != x) p[x] = find(p, p[x]);
        return p[x];
    }
}"""
    ],
    "399": [
        """class Solution {
    public double[] calcEquation(List<List<String>> equations, double[] values,
                                 List<List<String>> queries) {
        Map<String, Map<String, Double>> graph = new HashMap<>();
        for (int i = 0; i < equations.size(); i++) {
            String a = equations.get(i).get(0), b = equations.get(i).get(1);
            graph.computeIfAbsent(a, k -> new HashMap<>()).put(b, values[i]);
            graph.computeIfAbsent(b, k -> new HashMap<>()).put(a, 1.0 / values[i]);
        }
        double[] result = new double[queries.size()];
        for (int i = 0; i < queries.size(); i++) {
            String s = queries.get(i).get(0), t = queries.get(i).get(1);
            if (!graph.containsKey(s) || !graph.containsKey(t)) result[i] = -1.0;
            else {
                Set<String> seen = new HashSet<>();
                result[i] = dfs(graph, s, t, 1.0, seen);
            }
        }
        return result;
    }

    private double dfs(Map<String, Map<String, Double>> g, String cur, String target,
                       double prod, Set<String> seen) {
        if (cur.equals(target)) return prod;
        seen.add(cur);
        for (var e : g.get(cur).entrySet()) {
            if (!seen.contains(e.getKey())) {
                double res = dfs(g, e.getKey(), target, prod * e.getValue(), seen);
                if (res != -1.0) return res;
            }
        }
        return -1.0;
    }
}"""
    ],
    "690": [
        """class Solution {
    public int getImportance(List<Employee> employees, int id) {
        Map<Integer, Employee> map = new HashMap<>();
        for (Employee e : employees) map.put(e.id, e);
        return dfs(map, id);
    }

    private int dfs(Map<Integer, Employee> map, int id) {
        Employee e = map.get(id);
        int sum = e.importance;
        for (int sub : e.subordinates) sum += dfs(map, sub);
        return sum;
    }
}"""
    ],
    "1976": [
        """class Solution {
    private static final int MOD = 1_000_000_007;

    public int countPaths(int n, int[][] roads) {
        List<List<long[]>> g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        for (int[] r : roads) {
            g.get(r[0]).add(new long[] {r[1], r[2]});
            g.get(r[1]).add(new long[] {r[0], r[2]});
        }
        long[] dist = new long[n];
        long[] ways = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        ways[0] = 1;
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[] {0, 0});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d > dist[u]) continue;
            for (long[] e : g.get(u)) {
                int v = (int) e[0];
                long w = e[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    ways[v] = ways[u];
                    pq.offer(new long[] {dist[v], v});
                } else if (dist[u] + w == dist[v]) {
                    ways[v] = (ways[v] + ways[u]) % MOD;
                }
            }
        }
        return (int) ways[n - 1];
    }
}"""
    ],
    "261": [
        """class Solution {
    public boolean validTree(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a == b) return false;
            parent[a] = b;
        }
        return true;
    }

    private int find(int[] p, int x) {
        if (p[x] != x) p[x] = find(p, p[x]);
        return p[x];
    }
}"""
    ],
    "22": [
        """class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(result, new StringBuilder(), 0, 0, n);
        return result;
    }

    private void backtrack(List<String> result, StringBuilder cur, int open, int close, int n) {
        if (cur.length() == 2 * n) {
            result.add(cur.toString());
            return;
        }
        if (open < n) {
            cur.append('(');
            backtrack(result, cur, open + 1, close, n);
            cur.deleteCharAt(cur.length() - 1);
        }
        if (close < open) {
            cur.append(')');
            backtrack(result, cur, open, close + 1, n);
            cur.deleteCharAt(cur.length() - 1);
        }
    }
}"""
    ],
    "208": [
        """class Trie {
    private final Trie[] children = new Trie[26];
    private boolean end;

    public void insert(String word) {
        Trie node = this;
        for (char ch : word.toCharArray()) {
            int i = ch - 'a';
            if (node.children[i] == null) node.children[i] = new Trie();
            node = node.children[i];
        }
        node.end = true;
    }

    public boolean search(String word) {
        Trie node = find(word);
        return node != null && node.end;
    }

    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }

    private Trie find(String s) {
        Trie node = this;
        for (char ch : s.toCharArray()) {
            int i = ch - 'a';
            if (node.children[i] == null) return null;
            node = node.children[i];
        }
        return node;
    }
}"""
    ],
    "310": [
        """class Solution {
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        if (n == 1) return List.of(0);
        List<Set<Integer>> adj = new ArrayList<>();
        int[] deg = new int[n];
        for (int i = 0; i < n; i++) adj.add(new HashSet<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
            deg[e[0]]++;
            deg[e[1]]++;
        }
        ArrayDeque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < n; i++) if (deg[i] == 1) q.offer(i);
        int rem = n;
        while (rem > 2) {
            int sz = q.size();
            rem -= sz;
            for (int i = 0; i < sz; i++) {
                int leaf = q.poll();
                for (int nei : adj.get(leaf)) {
                    if (--deg[nei] == 1) q.offer(nei);
                }
            }
        }
        return new ArrayList<>(q);
    }
}"""
    ],
    "150": [
        """class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stk = new ArrayDeque<>();
        Set<String> ops = Set.of("+", "-", "*", "/");
        for (String token : tokens) {
            if (!ops.contains(token)) {
                stk.push(Integer.parseInt(token));
            } else {
                int b = stk.pop();
                int a = stk.pop();
                switch (token) {
                    case "+" -> stk.push(a + b);
                    case "-" -> stk.push(a - b);
                    case "*" -> stk.push(a * b);
                    case "/" -> stk.push(a / b);
                }
            }
        }
        return stk.pop();
    }
}""",
        """class Solution {
    public int evalRPN(String[] tokens) {
        int[] stk = new int[(tokens.length + 1) / 2];
        int top = -1;
        for (String token : tokens) {
            if (token.charAt(0) == '+' || token.charAt(0) == '-' ||
                token.charAt(0) == '*' || token.charAt(0) == '/') {
                int b = stk[top--];
                int a = stk[top--];
                int val = switch (token) {
                    case "+" -> a + b;
                    case "-" -> a - b;
                    case "*" -> a * b;
                    default -> a / b;
                };
                stk[++top] = val;
            } else {
                stk[++top] = Integer.parseInt(token);
            }
        }
        return stk[0];
    }
}""",
    ],
    "794": [
        """class Solution {
    public boolean validTicTacToe(String[] board) {
        int x = 0, o = 0;
        for (String row : board) {
            for (char c : row.toCharArray()) {
                if (c == 'X') x++;
                if (c == 'O') o++;
            }
        }
        if (x != o && x != o + 1) return false;
        boolean xWin = win(board, 'X');
        boolean oWin = win(board, 'O');
        if (xWin && o != x - 1) return false;
        if (oWin && o != x) return false;
        return !(xWin && oWin);
    }

    private boolean win(String[] board, char p) {
        for (int i = 0; i < 3; i++) {
            if (board[i].charAt(0) == p && board[i].charAt(1) == p && board[i].charAt(2) == p) return true;
            if (board[0].charAt(i) == p && board[1].charAt(i) == p && board[2].charAt(i) == p) return true;
        }
        if (board[0].charAt(0) == p && board[1].charAt(1) == p && board[2].charAt(2) == p) return true;
        if (board[0].charAt(2) == p && board[1].charAt(1) == p && board[2].charAt(0) == p) return true;
        return false;
    }
}""",
    ],
    "62": [
        """class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) dp[j] += dp[j - 1];
        }
        return dp[n - 1];
    }
}""",
    ],
    "48": [
        """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = tmp;
            }
        }
        for (int[] row : matrix) {
            for (int l = 0, r = row.length - 1; l < r; l++, r--) {
                int tmp = row[l];
                row[l] = row[r];
                row[r] = tmp;
            }
        }
    }
}""",
    ],
    "50": [
        """class Solution {
    public double myPow(double x, int n) {
        long N = n;
        if (N < 0) {
            x = 1 / x;
            N = -N;
        }
        double ans = 1, cur = x;
        for (long i = N; i > 0; i /= 2) {
            if ((i & 1) == 1) ans *= cur;
            cur *= cur;
        }
        return ans;
    }
}""",
    ],
    "54": [
        """class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        if (matrix.length == 0) return result;
        int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) result.add(matrix[top][j]);
            top++;
            for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
            right--;
            if (top <= bottom) {
                for (int j = right; j >= left; j--) result.add(matrix[bottom][j]);
                bottom--;
            }
            if (left <= right) {
                for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
                left++;
            }
        }
        return result;
    }
}""",
    ],
    "89": [
        """class Solution {
    public List<Integer> grayCode(int n) {
        List<Integer> result = new ArrayList<>();
        result.add(0);
        for (int i = 0; i < n; i++) {
            int size = result.size();
            for (int j = size - 1; j >= 0; j--) {
                result.add(result.get(j) | (1 << i));
            }
        }
        return result;
    }
}""",
    ],
}


def problem_number(filename: str) -> str | None:
    import re
    m = re.search(r"-(?:easy|medium|hard)-(\d+)-", filename)
    if m:
        return m.group(1)
    m = re.search(r"-lcr(\d+)-", filename)
    return m.group(1) if m else None
