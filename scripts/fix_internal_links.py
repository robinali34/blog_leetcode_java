#!/usr/bin/env python3
"""Prefix root-relative internal links with site baseurl."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASEURL = "/blog_leetcode_java"
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "vendor", "node_modules", "scripts"}

MARKDOWN_LINK_RE = re.compile(r"\]\((/[^)]+)\)")
HTML_HREF_RE = re.compile(r'href="(/[^"#]+)"')


def needs_prefix(path: str) -> bool:
    if path.startswith(f"{BASEURL}/"):
        return False
    if path.startswith(("http://", "https://", "mailto:", "#", "//")):
        return False
    return path.startswith(
        (
            "/posts/",
            "/2020/",
            "/2021/",
            "/2022/",
            "/2023/",
            "/2024/",
            "/2025/",
            "/2026/",
            "/2027/",
            "/leetcode-templates/",
            "/leetcode-questions-list",
            "/assets/",
        )
    ) or path == "/"


def prefix_path(path: str) -> str:
    return f"{BASEURL}{path}" if needs_prefix(path) else path


def fix_markdown_links(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f"]({prefix_path(match.group(1))})"

    return MARKDOWN_LINK_RE.sub(repl, text)


def fix_html_hrefs(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f'href="{prefix_path(match.group(1))}"'

    return HTML_HREF_RE.sub(repl, text)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = fix_html_hrefs(fix_markdown_links(text))
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".html"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if fix_file(path):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"\nFixed {changed} files")


if __name__ == "__main__":
    main()
