#!/usr/bin/env python3
"""Validate internal links against built Jekyll site."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urldefrag

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
BASEURL = "/blog_leetcode_java"
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "vendor", "node_modules", ".jdk", "scripts"}
SKIP_FILES = {"check_links.py", "fix_all_links.py", "fix_internal_links.py"}

# href="...", markdown links, bare absolute URLs
LINK_RE = re.compile(
    r"""(?:href\s*=\s*["']|]\()(?P<url>[^"')\s]+)""",
    re.I,
)


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


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".html"}:
            continue
        if path.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def normalize_site_path(url: str) -> tuple[str | None, str]:
    """Return (site-relative path with trailing slash, fragment) or (None, frag) if external."""
    url, frag = urldefrag(url)
    url = unquote(url.strip())

    if url.startswith("#") or not url:
        return None, frag

    if url.startswith("mailto:") or url.startswith("http://") or url.startswith("https://"):
        if "robinali34.github.io/blog_leetcode_java" in url:
            idx = url.index("/blog_leetcode_java")
            url = url[idx + len("/blog_leetcode_java") :]
        elif url.startswith("http"):
            return None, frag
        else:
            return None, frag

    if url.startswith(BASEURL):
        url = url[len(BASEURL) :]

    if not url.startswith("/"):
        return None, frag

    if url.endswith(".html"):
        return url, frag

    if not url.endswith("/"):
        url += "/"

    return url, frag


def site_path_exists(path: str) -> bool:
    if path.endswith(".html"):
        return (SITE / path.lstrip("/")).is_file()
    rel = path.lstrip("/")
    return (SITE / rel / "index.html").is_file() or (SITE / rel).is_file()


def check_links() -> tuple[list[tuple[Path, str, str]], list[tuple[Path, str, str, str]]]:
    """Return (broken, wrong_permalink) where wrong_permalink is (file, url, expected, slug)."""
    broken: list[tuple[Path, str, str]] = []
    wrong: list[tuple[Path, str, str, str]] = []
    slug_map = build_slug_permalink_map()

    for src in iter_source_files():
        text = src.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            raw = m.group("url")
            path, frag = normalize_site_path(raw)
            if path is None:
                continue

            slug = path.strip("/").split("/")[-1]
            if slug in slug_map and path != slug_map[slug]:
                expected = slug_map[slug]
                if not site_path_exists(path) or path != expected:
                    wrong.append((src, raw, expected, slug))
                continue

            if not site_path_exists(path):
                broken.append((src, raw, path))

    return broken, wrong


def main() -> int:
    if not SITE.is_dir():
        print("Run `bundle exec jekyll build` first.", file=sys.stderr)
        return 1

    broken, wrong = check_links()
  # dedupe
    broken = list({(str(f), u, p) for f, u, p in broken})
    wrong = list({(str(f), u, e, s) for f, u, e, s in wrong})

    print(f"Broken links (no built page): {len(broken)}")
    for f, u, p in sorted(broken)[:40]:
        print(f"  {f}: {u}  -> {p}")
    if len(broken) > 40:
        print(f"  ... and {len(broken) - 40} more")

    print(f"\nWrong permalink (slug exists, path mismatch): {len(wrong)}")
    for f, u, e, s in sorted(wrong)[:40]:
        print(f"  {f}: {u}")
        print(f"    expected: {BASEURL}{e}")
    if len(wrong) > 40:
        print(f"  ... and {len(wrong) - 40} more")

    return 1 if broken or wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())
