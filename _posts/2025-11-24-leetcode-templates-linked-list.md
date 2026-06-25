---
layout: post
title: "Algorithm Templates: Linked List"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates linked-list
permalink: /posts/2025-11-24-leetcode-templates-linked-list/
tags: [leetcode, templates, linked-list]
---

{% raw %}
Minimal, copy-paste Java for traversal, two pointers, dummy node, reversal, merge, cycle detection, and circular list.

## Contents

- [ListNode Definition](#listnode-definition)
- [Basic Operations](#basic-operations)
- [Two Pointers](#two-pointers)
- [Dummy Node Pattern](#dummy-node-pattern)
- [Reversal](#reversal)
- [Merge](#merge)
- [Cycle Detection](#cycle-detection)
- [Circular Linked List](#circular-linked-list)

## ListNode Definition

### Standard Definition

```java
// Standard ListNode definition used in LeetCode
class ListNode {
    public int val;
    public ListNode next;
    public ListNode() { this.val = 0; this.next = null; }
    ListNode(int x) { this.val = x; this.next = null; }
    ListNode(int x, ListNode next) { this.val = x; this.next = next; }
}
```

### Alternative Definitions

```java
// Without default constructor
class ListNode {
    public int val;
    public ListNode next;
    public ListNode(int x) { this.val = x; this.next = null; }
}
// With pointer initialization
class ListNode {
    public int val;
    public ListNode next;
    public ListNode(int x) { this.val = x; this.next = null; }
}
```

### Common Construction Methods

```java
// Method 1: Manual construction
ListNode createList(int[] values) {
    if (values.length == 0) return null;

    ListNode head = new ListNode(values[0]);
    ListNode cur = head;

    for (int i = 1; i < values.length; ++i) {
        cur.next = new ListNode(values[i]);
        cur = cur.next;
    }

    return head;
}

// Method 2: Recursive construction
ListNode createListRecursive(int[] values, int index) {
    if (index >= values.length) return null;
    ListNode node = new ListNode(values[index]);
    node.next = createListRecursive(values, index + 1);
    return node;
}

// Method 3: Using dummy node
ListNode createListWithDummy(int[] values) {
    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;

    for (int val : values) {
        cur.next = new ListNode(val);
        cur = cur.next;
    }

    return dummy.next;
}

// Method 4: Create list from array
ListNode createListFromArray(int arr[], int n) {
    if (n == 0) return null;

    ListNode head = new ListNode(arr[0]);
    ListNode cur = head;

    for (int i = 1; i < n; ++i) {
        cur.next = new ListNode(arr[i]);
        cur = cur.next;
    }

    return head;
}
```

### Utility Functions

```java
// Print linked list (for debugging)
static void printList(ListNode head) {
    ListNode cur = head;
    while (cur != null) {
        cout << cur.val;
        if (cur.next != null) cout << " . ";
        cur = cur.next;
    }
    cout << endl;
}

// Get length of linked list
static int getLength(ListNode head) {
    int length = 0;
    ListNode cur = head;
    while (cur != null) {
        length++;
        cur = cur.next;
    }
    return length;
}

// Convert linked list to vector
int[]listToVector(ListNode head) {
    int[]result;
    ListNode cur = head;
    while (cur != null) {
        result.add(cur.val);
        cur = cur.next;
    }
    return result;
}

// Delete entire linked list (free memory)
static void deleteList(ListNode head) {
    while (head != null) {
        ListNode temp = head;
        head = head.next;
        delete temp;
    }
}
```

### Example Usage

```java
// Example: Create list [1, 2, 3, 4, 5]
int[]values = {1, 2, 3, 4, 5}
ListNode head = createList(values);

// Print the list
printList(head);  // Output: 1 . 2 . 3 . 4 . 5

// Get length
int len = getLength(head);  // len = 5

// Convert to vector
int[]vec = listToVector(head);  // vec = [1, 2, 3, 4, 5]

// Clean up
deleteList(head);
```

## Basic Operations

### Traversal

```java
// Iterative traversal
static void traverse(ListNode head) {
    ListNode cur = head;
    while (cur != null) {
        // Process cur.val
        cur = cur.next;
    }
}

// Recursive traversal
static void traverseRecursive(ListNode head) {
    if (head == null) return;
    // Process head.val
    traverseRecursive(head.next);
}
```

### Insertion

```java
// Insert at head
ListNode insertAtHead(ListNode head, int val) {
    ListNode newNode = new ListNode(val);
    newNode.next = head;
    return newNode;
}

// Insert after node
static void insertAfter(ListNode node, int val) {
    ListNode newNode = new ListNode(val);
    newNode.next = node.next;
    node.next = newNode;
}
```

### Deletion

```java
// Delete node (given node to delete, not head)
static void deleteNode(ListNode node) {
    node.val = node.next.val;
    node.next = node.next.next;
}

// Delete node with value
ListNode deleteNode(ListNode head, int val) {
    if (head == null) return null;
    if (head.val == val) return head.next;

    ListNode cur = head;
    while (cur.next != null) {
        if (cur.next.val == val) {
            cur.next = cur.next.next;
            break;
        }
        cur = cur.next;
    }
    return head;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 203 | Remove Linked List Elements | [Link](https://leetcode.com/problems/remove-linked-list-elements/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-18-easy-203-remove-linked-list-elements/) |
| 237 | Delete Node in a Linked List | [Link](https://leetcode.com/problems/delete-node-in-a-linked-list/) | - |

## Two Pointers

### Fast and Slow Pointers

```java
// Find middle node
ListNode findMiddle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}

// Find kth node from end
ListNode findKthFromEnd(ListNode head, int k) {
    ListNode fast = head;
    for (int i = 0; i < k; ++i) {
        if (fast == null) return null;
        fast = fast.next;
    }
    ListNode slow = head;
    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }
    return slow;
}
```

### Two Pointers for Partitioning

```java
// Partition list around value x
ListNode partition(ListNode head, int x) {
    ListNode less = new ListNode(0);
    ListNode greater = new ListNode(0);
    ListNode lessCur = less;
    ListNode greaterCur = greater;

    while (head != null) {
        if (head.val < x) {
            lessCur.next = head;
            lessCur = lessCur.next;
        } else {
            greaterCur.next = head;
            greaterCur = greaterCur.next;
        }
        head = head.next;
    }

    greaterCur.next = null;
    lessCur.next = greater.next;
    return less.next;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 876 | Middle of the Linked List | [Link](https://leetcode.com/problems/middle-of-the-linked-list/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/10/easy-876-middle-of-the-linked-list/) |
| 19 | Remove Nth Node From End of List | [Link](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | - |

## Dummy Node Pattern

Use dummy node to simplify edge cases (empty list, head deletion).

```java
// Remove elements with dummy node
ListNode removeElements(ListNode head, int val) {
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    ListNode cur = dummy;

    while (cur.next != null) {
        if (cur.next.val == val) {
            cur.next = cur.next.next;
        } else {
            cur = cur.next;
        }
    }

    return dummy.next;
}
```

**Key Benefits:**
- Handles empty list case
- Simplifies head deletion
- Reduces special case handling

| ID | Title | Link | Solution |
|---|---|---|---|
| 203 | Remove Linked List Elements | [Link](https://leetcode.com/problems/remove-linked-list-elements/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-18-easy-203-remove-linked-list-elements/) |

## Reversal

### Reverse Entire List

```java
// Iterative reversal
ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode cur = head;
    while (cur != null) {
        ListNode next = cur.next;
        cur.next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}

// Recursive reversal
ListNode reverseListRecursive(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode newHead = reverseListRecursive(head.next);
    head.next.next = head;
    head.next = null;
    return newHead;
}
```

### Reverse Between Positions

```java
// Reverse nodes from position left to right
ListNode reverseBetween(ListNode head, int left, int right) {
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    ListNode prev = dummy;

    // Move to left position
    for (int i = 1; i < left; ++i) {
        prev = prev.next;
    }

    // Reverse
    ListNode cur = prev.next;
    for (int i = 0; i < right - left; ++i) {
        ListNode next = cur.next;
        cur.next = next.next;
        next.next = prev.next;
        prev.next = next;
    }

    return dummy.next;
}
```

### Reverse in Groups

```java
// Reverse nodes in k-group
ListNode reverseKGroup(ListNode head, int k) {
    ListNode cur = head;
    int count = 0;
    while (cur != null && count < k) {
        cur = cur.next;
        count++;
    }

    if (count == k) {
        cur = reverseKGroup(cur, k);
        while (count-- > 0) {
            ListNode next = head.next;
            head.next = cur;
            cur = head;
            head = next;
        }
        head = cur;
    }
    return head;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 206 | Reverse Linked List | [Link](https://leetcode.com/problems/reverse-linked-list/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-16-easy-206-reverse-linked-list/) |
| 92 | Reverse Linked List II | [Link](https://leetcode.com/problems/reverse-linked-list-ii/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/16/medium-92-reverse-linked-list-ii/) |
| 25 | Reverse Nodes in k-Group | [Link](https://leetcode.com/problems/reverse-nodes-in-k-group/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/09/24/hard-25-reverse-nodes-in-k-group/) |
| 24 | Swap Nodes in Pairs | [Link](https://leetcode.com/problems/swap-nodes-in-pairs/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/09/24/medium-23-swap-nodes-in-pairs/) |

## Merge

### Merge Two Sorted Lists

```java
// Merge two sorted lists
ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;

    while (list1 != null && list2 != null) {
        if (list1.val <= list2.val) {
            cur.next = list1;
            list1 = list1.next;
        } else {
            cur.next = list2;
            list2 = list2.next;
        }
        cur = cur.next;
    }

    cur.next = (list1 != null) ? list1 : list2;
    return dummy.next;
}
```

### Merge K Sorted Lists

```java
// Merge k sorted lists using divide and conquer
ListNode mergeKLists(ListNode[]& lists) {
    if (lists.length == 0) return null;
    return mergeKListsHelper(lists, 0, lists.size() - 1);
}

ListNode mergeKListsHelper(ListNode[]& lists, int left, int right) {
    if (left == right) return lists[left];
    int mid = left + (right - left) / 2;
    ListNode leftList = mergeKListsHelper(lists, left, mid);
    ListNode rightList = mergeKListsHelper(lists, mid + 1, right);
    return mergeTwoLists(leftList, rightList);
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 21 | Merge Two Sorted Lists | [Link](https://leetcode.com/problems/merge-two-sorted-lists/) | - |
| 23 | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/02/15/hard-23-merge-k-sorted-lists/) |
| 2 | Add Two Numbers | [Link](https://leetcode.com/problems/add-two-numbers/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-18-medium-2-add-two-numbers/) |
| 1669 | Merge In Between Linked Lists | [Link](https://leetcode.com/problems/merge-in-between-linked-lists/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/15/medium-1669-merge-in-between-linked-lists/) |

## Cycle Detection

### Detect Cycle (Floyd's Algorithm)

```java
// Detect cycle using Floyd's cycle detection
static boolean hasCycle(ListNode head) {
    if (head == null || head.next == null) return false;

    ListNode slow = head;
    ListNode fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }

    return false;
}

// Find cycle start node
ListNode detectCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;

    // Find meeting point
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) break;
    }

    if (fast == null || fast.next == null) return null;

    // Find cycle start
    slow = head;
    while (slow != fast) {
        slow = slow.next;
        fast = fast.next;
    }

    return slow;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 141 | Linked List Cycle | [Link](https://leetcode.com/problems/linked-list-cycle/) | - |
| 142 | Linked List Cycle II | [Link](https://leetcode.com/problems/linked-list-cycle-ii/) | - |

## Circular Linked List

### Insert into Sorted Circular List

```java
// Insert into sorted circular linked list
ListNode insert(ListNode head, int insertVal) {
    if (head == null) {
        ListNode newNode = new ListNode(insertVal);
        newNode.next = newNode;
        return newNode;
    }

    ListNode prev = head;
    ListNode cur = head.next;

    while (cur != head) {
        // Normal insertion point
        if (prev.val <= insertVal && insertVal <= cur.val) {
            break;
        }
        // At the boundary (largest to smallest)
        if (prev.val > cur.val && (insertVal >= prev.val || insertVal <= cur.val)) {
            break;
        }
        prev = cur;
        cur = cur.next;
    }

    prev.next = new ListNode(insertVal);
    prev.next.next = cur;
    return head;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 708 | Insert into a Sorted Circular Linked List | [Link](https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-27-medium-708-insert-into-a-sorted-circular-linked-list/) |
| 382 | Linked List Random Node | [Link](https://leetcode.com/problems/linked-list-random-node/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/08/medium-382-linked-list-random-node/) |

## More templates

- **Data structures (pointers, recursion):** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
- **Graph, Search:** [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/), [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}

