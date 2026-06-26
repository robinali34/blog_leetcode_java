#!/usr/bin/env python3
"""Compile-check ```java blocks and report failures."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_BLOCK_RE = re.compile(r"```java\s*\n(.*?)```", re.DOTALL)
SKIP_DIRS = {"scripts", ".git", "_site", ".jekyll-cache", "vendor", "node_modules"}

CPP_MARKERS = re.compile(
    r"vector<|unordered_map|push_back|begin\(|to_string\(|priority_queue<|"
    r"__builtin_|cin >>|#include|pair<|greater<|binary search \(lower|FIXME: was Python",
)

STUB = """
import java.util.*;
import java.util.stream.*;

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val; this.left = left; this.right = right;
    }
}
class Node {
    int val;
    List<Node> neighbors;
    Node(int val) { this.val = val; neighbors = new ArrayList<>(); }
}
class NestedInteger {
    private Integer single;
    private List<NestedInteger> list;
    public NestedInteger() {}
    public NestedInteger(int value) { single = value; }
    public boolean isInteger() { return single != null; }
    public Integer getInteger() { return single; }
    public List<NestedInteger> getList() { return list; }
    public void setInteger(int value) { single = value; }
    public void add(NestedInteger ni) {
        if (list == null) list = new ArrayList<>();
        list.add(ni);
    }
}
class Employee {
    public int id;
    public int importance;
    public List<Integer> subordinates = new ArrayList<>();
}
"""


def wrap_java(code: str) -> str:
    code = re.sub(r"^// import [^;]+;\s*\n", "", code, flags=re.M)
    if re.search(r"^\s*class\s+", code, re.M):
        return STUB + "\n" + code
    if re.search(r"^\s*(?:static\s+)?(?:int|long|void|boolean|double|String|List|int\[\])\s+\w+\s*\(", code, re.M):
        return STUB + "\nclass Snippet {\n" + code + "\n}\n"
    return STUB + "\nclass Solution {\n" + code + "\n}\n"


def try_compile(code: str) -> str | None:
    src = wrap_java(code)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "Main.java"
        path.write_text(src, encoding="utf-8")
        proc = subprocess.run(
            ["javac", "-encoding", "UTF-8", str(path)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return proc.stderr.strip()[:500]
    return None


def main() -> None:
    failures: list[tuple[str, int, str, str]] = []
    cpp_remnants: list[tuple[str, int]] = []
    total = 0

    for path in sorted(ROOT.rglob("*.md")):
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for i, block in enumerate(JAVA_BLOCK_RE.findall(text), 1):
            total += 1
            if CPP_MARKERS.search(block):
                cpp_remnants.append((str(path.relative_to(ROOT)), i))
            err = try_compile(block)
            if err:
                failures.append((str(path.relative_to(ROOT)), i, err, block[:120]))

    print(f"Checked {total} Java blocks")
    print(f"C++ remnants: {len(cpp_remnants)}")
    print(f"Compile failures: {len(failures)}")
    print()

    if cpp_remnants[:30]:
        print("=== C++ remnants (first 30) ===")
        for f, i in cpp_remnants[:30]:
            print(f"  {f} block {i}")
        print()

    if failures[:40]:
        print("=== Compile failures (first 40) ===")
        for f, i, err, _ in failures[:40]:
            print(f"--- {f} block {i} ---")
            print(err)
            print()


if __name__ == "__main__":
    main()
