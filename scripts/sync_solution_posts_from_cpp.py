#!/usr/bin/env python3
"""Sync solution post prose/SVG from C++ blog; preserve Java code blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_template_content_from_cpp import adapt_prose, strip_front_matter, strip_liquid_raw_tags  # noqa: E402

CPP_ROOT = Path("/home/robina/rli/blog_leetcode/_posts")
JAVA_ROOT = Path(__file__).resolve().parent.parent / "_posts"

SKIP = {
    "2025-09-23-cpp-cheatsheet.md",
    "2025-09-23-java-cheatsheet.md",
    "2026-06-24-java-basics.md",
    "2026-06-24-java-guide-basics.md",
    "2026-06-25-leetcode-beginners-guide.md",
}

URL_REPLACEMENTS = [
    (r"robinali34\.github\.io/blog_leetcode/", "robinali34.github.io/blog_leetcode_java/"),
    (r"(?<![\w])\/blog_leetcode\/", "/blog_leetcode_java/"),
    (r"www\.leetcode\.com", "leetcode.com"),
]


def extract_code_blocks(text: str, lang: str) -> list[str]:
    blocks = re.findall(rf"```{lang}\n[\s\S]*?```", text)
    if lang != "java":
        return blocks
    solution = [b for b in blocks if "class Solution" in b]
    if solution:
        return solution
    return blocks


def inject_java_code(cpp_body: str, java_blocks: list[str]) -> str:
    idx = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal idx
        if idx < len(java_blocks):
            block = java_blocks[idx]
            idx += 1
            return block
        return match.group(0)

    body = re.sub(r"```(?:cpp|c\+\+|java)\n[\s\S]*?```", repl, cpp_body)
    return re.sub(r"```python\n[\s\S]*?```", "", body)


def adapt_body(text: str) -> str:
    """Adapt URLs and prose outside code fences (never rewrite ```cpp`` to ```java``)."""

    def adapt_outside_fences(src: str) -> str:
        parts = re.split(r"(```[\s\S]*?```)", src)
        out: list[str] = []
        for part in parts:
            if part.startswith("```"):
                out.append(part)
                continue
            chunk = strip_liquid_raw_tags(part)
            for pattern, repl in URL_REPLACEMENTS:
                chunk = re.sub(pattern, repl, chunk)
            out.append(adapt_prose(chunk))
        return "".join(out)

    return adapt_outside_fences(text)


def wrap_raw_if_needed(body: str) -> str:
    if "<svg" not in body:
        return body
    if body.lstrip().startswith("{% raw %}"):
        if "{% endraw %}" not in body:
            return body.rstrip() + "\n{% endraw %}\n"
        return body
    return "{% raw %}\n" + body.rstrip() + "\n{% endraw %}\n"


def sync_file(name: str, dry_run: bool = False) -> bool:
    if name in SKIP or "leetcode-templates" in name:
        return False
    cpp_path = CPP_ROOT / name
    java_path = JAVA_ROOT / name
    if not cpp_path.exists() or not java_path.exists():
        return False

    java_fm, java_body = strip_front_matter(java_path.read_text(encoding="utf-8"))
    _, cpp_body = strip_front_matter(cpp_path.read_text(encoding="utf-8"))

    java_blocks = extract_code_blocks(java_body, "java")
    merged = inject_java_code(cpp_body, java_blocks)
    merged = adapt_body(merged)
    merged = wrap_raw_if_needed(merged)

    new_text = java_fm.rstrip() + "\n\n" + merged.lstrip()
    old_text = java_path.read_text(encoding="utf-8")
    if new_text == old_text:
        return False

    if not dry_run:
        java_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not names:
        names = sorted(
            p.name
            for p in CPP_ROOT.glob("*.md")
            if (JAVA_ROOT / p.name).exists() and p.name not in SKIP
        )

    updated = 0
    for name in names:
        if sync_file(name, dry_run=dry_run):
            updated += 1
            print(f"{'[dry-run] ' if dry_run else ''}updated: {name}")

    print(f"Done. {updated} file(s) {'would be ' if dry_run else ''}updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
