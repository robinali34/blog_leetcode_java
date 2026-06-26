---

layout: post
title: "[Medium] 1242. Web Crawler Multithreaded"
date: 2025-09-24 18:00:00 -0000
categories: leetcode algorithm multithreading concurrency data-structures synchronization medium java web-crawler concurrent-programming problem-solving
permalink: /posts/2025-09-24-medium-1242-web-crawler-multithreaded/
---

{% raw %}
This is a multithreading problem that requires implementing a concurrent web crawler. The key insight is using proper synchronization mechanisms to avoid race conditions while crawling URLs from the same domain concurrently.

Given a start URL and an HTML parser, implement a multithreaded web crawler that:
1. Crawls all URLs from the same domain as the start URL
2. Uses multiple threads for concurrent crawling
3. Avoids visiting the same URL multiple times
4. Returns all discovered URLs

## Examples
**Example 1:**
```
Input: 
urls = [
  "http://news.yahoo.com",
  "http://news.yahoo.com/news",
  "http://news.yahoo.com/news/topics/",
  "http://news.google.com"
]
startUrl = "http://news.yahoo.com/news/topics/"
Output: [
  "http://news.yahoo.com",
  "http://news.yahoo.com/news",
  "http://news.yahoo.com/news/topics/"
]
```

**Example 2:**
```
Input:
urls = [
  "http://news.yahoo.com",
  "http://news.yahoo.com/news",
  "http://news.yahoo.com/news/topics/",
  "http://news.google.com"
]
startUrl = "http://news.google.com"
Output: ["http://news.google.com"]
```

## Constraints
- 1 <= urls.length <= 1000
- 1 <= urls[i].length <= 300
- startUrl is one of the urls
- All URLs have the same hostname

## Thinking Process

The solution involves:

1. **Domain Extraction**: Extract the base domain from the start URL
2. **Thread Pool**: Use multiple threads for concurrent crawling
3. **Synchronization**: Use locks to prevent race conditions
4. **URL Filtering**: Only crawl URLs from the same domain
5. **Visited Tracking**: Avoid revisiting the same URL

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 110" style="max-width:100%;height:auto;display:block;margin:1.5em auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
<text x="50%" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#5A5752">Array + hash map</text>

  <rect x="30" y="45" width="28" height="28" rx="3" fill="#E8E3D8" stroke="#B8B5B0"/><text x="44" y="61" text-anchor="middle" font-size="10">2</text>
  <rect x="62" y="45" width="28" height="28" rx="3" fill="#E0D8E4" stroke="#A098A8"/><text x="76" y="61" text-anchor="middle" font-size="10">7</text>
  <rect x="106" y="45" width="28" height="28" rx="3" fill="#E8E3D8" stroke="#B8B5B0"/><text x="120" y="61" text-anchor="middle" font-size="10">11</text>
  <rect x="150" y="40" width="60" height="38" rx="4" fill="#FAF8F5" stroke="#D4D1CC"/>
  <text x="180" y="61" text-anchor="middle" font-size="10" fill="#6B6560">map</text>
  <text x="110" y="100" text-anchor="middle" font-size="11" fill="#6B6560">hash map for O(1) lookups</text>

</svg>

## Common Approaches

Typical techniques for this pattern:

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| **Brute force** *(this problem)* | Often O(n^2) or O(2^n) | O(n) | Baseline; clarifies the optimization target |
| Sort + scan | O(n log n) | O(1) | Pairs, intervals, greedy ordering |
| Hash map / set | O(n) | O(n) | Frequency, membership, two-sum style |
| Single-pass linear | O(n) | O(1) | Two pointers, sliding window, Kadane |

## Solution
**Time Complexity:** O(n) where n is the number of URLs in the same domain  
**Space Complexity:** O(n) for storing visited URLs and results

```java
/**
 * // This is the HtmlParser's API interface.
 * // You should not implement it, or speculate about its implementation
 * interface HtmlParser {
 *     public List<String> getUrls(String url);
 * }
 */
class Solution {
    public List<String> crawl(String startUrl, HtmlParser htmlParser) {
        String hostname = getHostname(startUrl);
        Set<String> visited = ConcurrentHashMap.newKeySet();
        Queue<String> queue = new ConcurrentLinkedQueue<>();
        visited.add(startUrl);
        queue.offer(startUrl);

        ExecutorService pool = Executors.newFixedThreadPool(16);
        for (int i = 0; i < 16; i++) {
            pool.submit(() -> {
                while (true) {
                    String url = queue.poll();
                    if (url == null) {
                        break;
                    }
                    for (String next : htmlParser.getUrls(url)) {
                        if (!getHostname(next).equals(hostname)) {
                            continue;
                        }
                        if (visited.add(next)) {
                            queue.offer(next);
                        }
                    }
                }
            });
        }
        pool.shutdown();
        try {
            pool.awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return new ArrayList<>(visited);
    }

    private String getHostname(String url) {
        int start = url.indexOf("://") + 3;
        int end = url.indexOf('/', start);
        return end == -1 ? url.substring(start) : url.substring(start, end);
    }
}
```

### Solution Explanation

**Approach:** Brute force (this problem)

**Key idea:** The solution involves:

**How the code works:**
1. **Domain Extraction**: Extract the base domain from the start URL
2. **Thread Pool**: Use multiple threads for concurrent crawling
3. **Synchronization**: Use locks to prevent race conditions
4. **URL Filtering**: Only crawl URLs from the same domain
5. **Visited Tracking**: Avoid revisiting the same URL

**Walkthrough** — input `urls = [`, expected output `[`:

1. Initialize variables from the problem setup.
2. Apply the main loop / recursion until the condition is met.
3. Confirm the result matches the expected output.
## Step-by-Step Example

Let's trace through the Python solution with startUrl = "http://news.yahoo.com/news/topics/":

**Step 1:** Extract base domain
- `host("http://news.yahoo.com/news/topics/")` → "news.yahoo.com"
- `visited = {"http://news.yahoo.com/news/topics/"}`

**Step 2:** Start worker thread
- Submit initial URL to thread pool
- Worker calls `htmlParser.getUrls()` on startUrl

**Step 3:** Process discovered URLs
- For each URL from parser:
  - Check if host matches base domain
  - If yes, add to visited set (with lock)
  - Add to next_urls for further processing

**Step 4:** Continue until no more URLs
- Submit new URLs to thread pool
- Wait for completion and process results
- Repeat until all URLs are processed

## Synchronization Patterns

### C++ Approach:
- **Multiple Mutexes**: Separate locks for queue, map, and results
- **Manual Thread Management**: Create and join threads manually
- **Polling**: Sleep and check for work periodically

### Python Approach:
- **Single Lock**: One lock for the visited set
- **ThreadPoolExecutor**: Automatic thread management
- **Future-based**: Use futures for asynchronous execution

## Common Mistakes

- **Race Conditions**: Not properly synchronizing access to shared data
- **Deadlocks**: Incorrect lock ordering or holding multiple locks
- **Memory Leaks**: Not properly cleaning up thread resources
- **Infinite Loops**: Not handling empty queue conditions correctly
- **Domain Mismatch**: Processing URLs from different domains

---

## References

- [LC 1242: Web Crawler Multithreaded on LeetCode](https://leetcode.com/problems/web-crawler-multithreaded/)
- [LeetCode Discuss — LC 1242: Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded/discuss/)
- [LeetCode Editorial](https://leetcode.com/problems/web-crawler-multithreaded/editorial/) *(may require premium)*

## Key Takeaways

1. **Thread Safety**: Use locks to protect shared data structures
2. **Domain Filtering**: Only process URLs from the same domain
3. **Concurrent Processing**: Use thread pools for parallel execution
4. **Deadlock Prevention**: Careful lock ordering and timeout handling
5. **Memory Management**: Proper cleanup of thread resources
{% endraw %}
