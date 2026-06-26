#!/usr/bin/env python3
"""Fix common broken internal links in the Java blog."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "vendor", "node_modules", ".jdk"}
BASEURL = "/blog_leetcode_java"

BEGINNERS_OLD = "/2026/06/25/leetcode-beginners-guide/"
BEGINNERS_NEW = "/posts/2026-06-25-leetcode-beginners-guide/"


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".html"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def build_slug_permalink_map() -> dict[str, str]:
    slug_map: dict[str, str] = {}
    for path in (ROOT / "_posts").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^permalink:\s*(.+)$", text, re.M)
        if not m:
            continue
        perm = m.group(1).strip().strip('"').strip("'")
        if not perm.endswith("/"):
            perm += "/"
        key = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        slug_map[key] = perm
    return slug_map


def fix_post_urls(text: str, slug_map: dict[str, str]) -> str:
    """Rewrite solution/post links to match each post's actual permalink."""

    def replace_path(path: str) -> str:
        if path.endswith(".html"):
            return path
        if not path.endswith("/"):
            path += "/"
        slug = path.strip("/").split("/")[-1]
        actual = slug_map.get(slug)
        if actual and actual != path:
            return actual
        return path

    def repl_abs(m: re.Match[str]) -> str:
        prefix, path = m.group(1), m.group(2)
        new_path = replace_path(path)
        return prefix + new_path

    text = re.sub(
        r"(https://robinali34\.github\.io/blog_leetcode_java)(/[^)\s\"']+)",
        repl_abs,
        text,
    )

    def repl_root(m: re.Match[str]) -> str:
        path = m.group(2)
        new_path = replace_path(path)
        return BASEURL + new_path

    text = re.sub(
        rf"({re.escape(BASEURL)})(/[^)\s\"']+)",
        repl_root,
        text,
    )

    # Date-based root-relative paths in markdown tables (no baseurl prefix)
    def repl_date(m: re.Match[str]) -> str:
        path = m.group(0)
        new_path = replace_path(path)
        if new_path != path:
            return new_path
        return path

    # Only rewrite date-style paths when the slug maps to a different permalink.
    text = re.sub(
        r"/\d{4}/\d{2}/\d{2}/[a-z0-9][a-z0-9-]*/",
        repl_date,
        text,
    )
  # /posts/YYYY-MM-DD-slug/ that may point at wrong filename date
    text = re.sub(
        r"/posts/\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*/",
        repl_date,
        text,
    )

    return text


def fix_text(text: str, slug_map: dict[str, str] | None = None) -> str:
    # C++ blog absolute URLs -> Java blog
    text = re.sub(
        r"https://robinali34\.github\.io/blog_leetcode(?!_java)/",
        "https://robinali34.github.io/blog_leetcode_java/",
        text,
    )
    # Root-relative C++ blog paths (not already java)
    text = re.sub(r"(?<![\w])\/blog_leetcode\/", f"{BASEURL}/", text)

    # Beginners guide: date URL -> posts permalink
    text = text.replace(f"{BASEURL}{BEGINNERS_OLD}", f"{BASEURL}{BEGINNERS_NEW}")
    text = text.replace(BEGINNERS_OLD, f"{BASEURL}{BEGINNERS_NEW}")

    if slug_map:
        text = fix_post_urls(text, slug_map)

    return text


def add_missing_permalinks() -> int:
    posts_dir = ROOT / "_posts"
    updated = 0
    for path in sorted(posts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        fm = text[3:end]
        if re.search(r"^permalink:", fm, re.M):
            continue
        if re.search(r"^published:\s*false", fm, re.M):
            continue
        slug = path.stem
        permalink = f"/posts/{slug}/"
        new_fm = fm.rstrip() + f"\npermalink: {permalink}"
        path.write_text("---\n" + new_fm + "\n---" + text[end + 4 :], encoding="utf-8")
        updated += 1
        print(f"added permalink: {path.name} -> {permalink}")
    return updated


def main() -> None:
    slug_map = build_slug_permalink_map()
    changed = 0
    for path in iter_source_files():
        original = path.read_text(encoding="utf-8")
        updated = fix_text(original, slug_map)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
    perm_added = add_missing_permalinks()
    print(f"\nUpdated {changed} files; added {perm_added} permalinks")


if __name__ == "__main__":
    main()
