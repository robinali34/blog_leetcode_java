#!/usr/bin/env python3
"""Generate neetcode-150-tracker.md from Beginner's Guide + _posts permalinks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://robinali34.github.io/blog_leetcode_java"
GUIDE = ROOT / "_posts/2026-06-25-leetcode-beginners-guide.md"
OUT = ROOT / "neetcode-150-tracker.md"

TEMPLATE_LINKS = {
    "Arrays & Hashing": "/posts/2025-11-24-leetcode-templates-string-processing/",
    "Two Pointers": "/posts/2025-11-24-leetcode-templates-array-matrix/",
    "Sliding Window": "/posts/2025-11-24-leetcode-templates-string-processing/",
    "Stack": "/posts/2025-11-13-leetcode-templates-stack/",
    "Binary Search": "/posts/2026-01-20-leetcode-templates-search/",
    "Linked List": "/posts/2025-11-24-leetcode-templates-linked-list/",
    "Trees": "/posts/2025-10-29-leetcode-templates-trees/",
    "Tries": "/posts/2025-10-29-leetcode-templates-data-structures/",
    "Heap / Priority Queue": "/posts/2026-01-05-leetcode-templates-heap/",
    "Backtracking": "/posts/2025-11-24-leetcode-templates-backtracking/",
    "Graphs": "/posts/2025-10-29-leetcode-templates-graph/",
    "Advanced Graphs": "/posts/2025-10-29-leetcode-templates-graph/",
    "1-D Dynamic Programming": "/posts/2025-10-29-leetcode-templates-dp/",
    "2-D Dynamic Programming": "/posts/2025-10-29-leetcode-templates-dp/",
    "Greedy": "/posts/2025-12-14-leetcode-templates-greedy/",
    "Intervals": "/posts/2025-12-14-leetcode-templates-greedy/",
    "Math & Geometry": "/posts/2025-10-29-leetcode-templates-math-geometry/",
    "Bit Manipulation": "/posts/2025-11-24-leetcode-templates-math-bit-manipulation/",
}


def build_problem_url_map() -> dict[int, str]:
    mapping: dict[int, str] = {}
    for path in (ROOT / "_posts").glob("*.md"):
        m = re.match(r"\d{4}-\d{2}-\d{2}-(easy|medium|hard)-(\d+)-", path.name)
        if not m:
            continue
        num = int(m.group(2))
        text = path.read_text(encoding="utf-8")
        pm = re.search(r"^permalink:\s*(.+)$", text, re.M)
        if not pm:
            continue
        perm = pm.group(1).strip().strip('"').strip("'")
        if not perm.endswith("/"):
            perm += "/"
        mapping[num] = perm
    return mapping


def parse_neetcode_sections(text: str) -> list[tuple[str, list[tuple[int, str, str]]]]:
    """Return [(category, [(num, title, slug)])]."""
    section = text.split("#### Complete problem list (150)")[1]
    section = section.split("#### How to use NeetCode 150 effectively")[0]
    categories: list[tuple[str, list[tuple[int, str, str]]]] = []
    current = ""
    rows: list[tuple[int, str, str]] = []
    for line in section.splitlines():
        if line.startswith("**") and line.endswith("**"):
            if current and rows:
                categories.append((current, rows))
            current = line.strip("*").split(" (")[0]
            rows = []
            continue
        m = re.match(
            r"\|\s*\[(\d+)\]\(https://leetcode\.com/problems/([^/)]+)/?\)\s*(†)?\s*\|\s*(.+?)\s*\|",
            line,
        )
        if m:
            rows.append((int(m.group(1)), m.group(4).strip(), m.group(2)))
    if current and rows:
        categories.append((current, rows))
    return categories


def blog_cell(num: int, urls: dict[int, str]) -> str:
    perm = urls.get(num)
    if perm:
        return f"[Solution]({BASE}{perm})"
    return "—"


def main() -> None:
    urls = build_problem_url_map()
    guide = GUIDE.read_text(encoding="utf-8")
    categories = parse_neetcode_sections(guide)

    all_nums = [n for _, rows in categories for n, _, _ in rows]
    covered = sum(1 for n in all_nums if n in urls)
    total = len(all_nums)

    lines = [
        "---",
        "layout: page",
        'title: "NeetCode 150 Tracker"',
        "permalink: /neetcode-150-tracker.html",
        "date: 2026-06-25 12:00:00 -0700",
        "categories: leetcode interview-prep neetcode guide",
        "---",
        "",
        "# NeetCode 150 Tracker",
        "",
        "Track your progress through the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150) interview roadmap. "
        f"**{covered} of {total}** problems have a detailed Java solution on this blog; the rest link to LeetCode until a post is added.",
        "",
        "> New to the roadmap? Read the [Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/) "
        "or start from the [Interview Prep Hub](/blog_leetcode_java/interview-prep/).",
        "",
        "## Progress summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total problems | {total} |",
        f"| Blog solutions available | {covered} |",
        f"| Not yet on blog | {total - covered} |",
        f"| Coverage | {100 * covered // total}% |",
        "",
        "**How to use:** Solve on [LeetCode](https://leetcode.com/problemset/) (pick **Java**). "
        "If a **Blog Solution** exists, read it after your attempt for the full interview-style walkthrough.",
        "",
        "---",
        "",
    ]

    for cat, rows in categories:
        tmpl = TEMPLATE_LINKS.get(cat, "/leetcode-templates/")
        lines.append(f"## {cat}")
        lines.append("")
        lines.append(
            f"Template: [{cat}]({BASE}{tmpl}) · "
            f"Blog coverage: **{sum(1 for n, _, _ in rows if n in urls)}/{len(rows)}**"
        )
        lines.append("")
        lines.append("| LC | Problem | LeetCode | Blog Solution |")
        lines.append("|:--:|---------|----------|---------------|")
        for num, title, slug in rows:
            lc = f"[{num}](https://leetcode.com/problems/{slug}/)"
            lines.append(
                f"| {lc} | {title} | [Solve](https://leetcode.com/problems/{slug}/) | {blog_cell(num, urls)} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Related resources",
            "",
            "| Resource | Description |",
            "|----------|-------------|",
            "| [Interview Prep Hub](/blog_leetcode_java/interview-prep/) | Central hub for interview study |",
            "| [Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/) | Phased roadmap and study tips |",
            "| [LeetCode Templates](/blog_leetcode_java/leetcode-templates/) | Pattern templates by category |",
            "| [All Solved Problems](/blog_leetcode_java/leetcode-questions-list.html) | Full list of blog solutions |",
            "| [Meta Question List](/blog_leetcode_java/posts/2025-09-24-meta-question-list/) | Company-style practice list |",
            "",
            f"*Auto-generated from post permalinks. Last updated: June 25, 2026*",
            "",
        ]
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({covered}/{total} covered)")


if __name__ == "__main__":
    main()
