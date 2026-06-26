#!/usr/bin/env python3
"""Merge prose, callouts, and SVG diagrams from C++ template posts into Java posts.

Preserves ```java code blocks in the Java version; only updates non-code content.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CPP_ROOT = Path("/home/robina/rli/blog_leetcode/_posts")
JAVA_ROOT = Path("/home/robina/rli/blog_leetcode_java/_posts")

PROSE_SUBS = [
    (r"\bC\+\+\b", "Java"),
    (r"\bcpp\b", "java"),
    (r"\bSTL\b", "Java Collections"),
    (r"battle-tested C\+\+ snippets", "battle-tested Java snippets"),
    (r"battle-tested C\+\+ templates", "battle-tested Java templates"),
    (r"ready-to-use C\+\+ snippets", "ready-to-use Java snippets"),
    (r"ready-to-use C\+\+ templates", "ready-to-use Java templates"),
    (r"essential C\+\+ templates", "essential Java templates"),
    (r"complete, tested C\+\+ implementations", "complete, tested Java implementations"),
    (r"self-contained C++ you", "self-contained Java you"),
    (r"production-ready C\+\+ templates", "production-ready Java templates"),
    (r"copy-paste C\+\+", "copy-paste Java"),
    (r"In C\+\+, `java\.util\.priority_queue`", "In Java, `PriorityQueue`"),
    (r"In C\+\+, `std::priority_queue`", "In Java, `PriorityQueue`"),
    (r"In Java, `PriorityQueue` is a max-heap by default", "In Java, `PriorityQueue` is a min-heap by default"),
    (r"`std::priority_queue`", "`PriorityQueue`"),
    (r"pass `greater<int>`", "use the default constructor for a min-heap, or pass `Comparator.reverseOrder()` for max-heap"),
    (r"`push\(x\)`", "`offer(x)`"),
    (r"`pop\(\)`", "`poll()`"),
    (r"`top\(\)`", "`peek()`"),
    (r"`empty\(\)`", "`isEmpty()`"),
    (r"struct, lambda", "Comparator, lambda"),
]


def strip_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    fm = text[: end + 4]
    body = text[end + 4 :].lstrip("\n")
    return fm, body


def adapt_prose(text: str) -> str:
    for pattern, repl in PROSE_SUBS:
        text = re.sub(pattern, repl, text)
    return text


def strip_liquid_raw_tags(text: str) -> str:
    text = re.sub(r"\{%\s*raw\s*%\}\s*\n?", "", text)
    text = re.sub(r"\s*\{%\s*endraw\s*%\}\s*\n?", "\n", text)
    return text


def needs_raw_wrapper(body: str) -> bool:
    return bool(re.search(r"\{\{|\{%", body))


def split_sections(body: str) -> list[str]:
    if not body.strip():
        return []
    if not body.startswith("## "):
        idx = body.find("\n## ")
        if idx == -1:
            return [body]
        intro = body[:idx]
        rest = body[idx + 1 :]
        return [intro, *re.split(r"(?=^## )", rest, flags=re.M)]
    return re.split(r"(?=^## )", body, flags=re.M)


def section_header(section: str) -> str | None:
    m = re.match(r"^(## .+?)(?:\n|$)", section)
    return m.group(1).strip() if m else None


def split_header_body(section: str) -> tuple[str, str]:
    m = re.match(r"^(## .+?\n)([\s\S]*)$", section)
    if m:
        return m.group(1), m.group(2)
    return "", section


def extract_code_block(rest: str) -> tuple[str, str]:
    fence = rest.find("```")
    if fence == -1:
        preamble = rest.rstrip()
        if preamble:
            preamble += "\n"
        return preamble, ""
    return rest[:fence], rest[fence:]


def sections_by_header(sections: list[str]) -> tuple[list[str | None], dict[str | None, str]]:
    order: list[str | None] = []
    by_header: dict[str | None, str] = {}
    for sec in sections:
        if not sec.strip():
            continue
        h = section_header(sec) if sec.lstrip().startswith("## ") else None
        if h not in by_header:
            order.append(h)
            by_header[h] = sec
        elif h is None:
            by_header[h] = by_header[h].rstrip() + "\n\n" + sec.lstrip()
        else:
            by_header[h] = by_header[h].rstrip() + "\n\n" + sec.lstrip()
    return order, by_header


def normalize_header(name: str | None) -> str | None:
    if name is None:
        return None
    s = name.lower()
    s = re.sub(r"^##\s*", "", s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def index_by_normalized(
    order: list[str | None], by_header: dict[str | None, str]
) -> tuple[list[str | None], dict[str | None, str]]:
    norm_order: list[str | None] = []
    norm_by: dict[str | None, str] = {}
    for h in order:
        key = normalize_header(h)
        if key not in norm_by:
            norm_order.append(key)
            norm_by[key] = by_header[h]
    return norm_order, norm_by


def extract_svgs(text: str) -> list[str]:
    return re.findall(r"<svg[\s\S]*?</svg>", text, flags=re.I)


def strip_code_fences(text: str, langs: frozenset[str]) -> str:
    def repl(match: re.Match[str]) -> str:
        lang = match.group(1) or ""
        if lang in langs:
            return ""
        return match.group(0)

    return re.sub(r"```(\w*)\n[\s\S]*?```", repl, text)


def cpp_prose_for_section(cpp_rest: str, java_rest: str) -> str:
    stripped = strip_code_fences(cpp_rest, frozenset({"cpp", "java", "c++"}))
    stripped = adapt_prose(strip_liquid_raw_tags(stripped)).strip()
    if stripped:
        return stripped + "\n\n"
    return ""


def merge_bodies(cpp_body: str, java_body: str) -> str:
    cpp_order, cpp_by_header = sections_by_header(split_sections(cpp_body))
    java_order, java_by_header = sections_by_header(split_sections(strip_liquid_raw_tags(java_body)))

    cpp_norm_order, cpp_norm_by = index_by_normalized(cpp_order, cpp_by_header)
    java_norm_order, java_norm_by = index_by_normalized(java_order, java_by_header)

    out: list[str] = []

    cpp_intro = cpp_by_header.get(None, "")
    java_intro = java_by_header.get(None, "")

    if cpp_intro.strip():
        raw_prefix = "{% raw %}\n" if "<svg" in cpp_body or java_intro.lstrip().startswith("{% raw %}") else ""
        cpp_rest = strip_liquid_raw_tags(cpp_intro)
        cpp_intro_text = adapt_prose(cpp_rest.strip())
        out.append((raw_prefix + cpp_intro_text + "\n") if cpp_intro_text else "")
    elif java_intro.strip():
        intro = strip_liquid_raw_tags(java_intro)
        out.append(intro if intro.endswith("\n") else intro + "\n")

    contents_key = normalize_header("## Contents")
    for key in cpp_norm_order:
        if key is None or key == contents_key:
            continue
        if key in java_norm_order:
            continue
        sec = cpp_norm_by[key]
        _, rest = split_header_body(sec)
        preamble, code = extract_code_block(rest)
        if code.strip():
            continue
        block = adapt_prose(strip_liquid_raw_tags(sec))
        if block.strip():
            out.append(block if block.endswith("\n") else block + "\n")

    for h in java_order:
        if h is None:
            continue
        java_sec = java_by_header[h]
        key = normalize_header(h)
        cpp_sec = cpp_norm_by.get(key)
        if not cpp_sec:
            sec = java_sec if java_sec.endswith("\n") else java_sec + "\n"
            out.append(sec)
            continue

        java_hdr, java_rest = split_header_body(java_sec)
        _, cpp_rest = split_header_body(cpp_sec)

        cpp_preamble = cpp_prose_for_section(cpp_rest, java_rest)
        _, java_code = extract_code_block(java_rest)
        merged = java_hdr + cpp_preamble + java_code
        if not merged.endswith("\n"):
            merged += "\n"
        out.append(merged)

    body = "".join(out)
    if "<svg" in body and not body.lstrip().startswith("{% raw %}"):
        body = "{% raw %}\n" + body.rstrip() + "\n{% endraw %}\n"
    elif body.lstrip().startswith("{% raw %}") and "{% endraw %}" not in body:
        body = body.rstrip() + "\n{% endraw %}\n"
    return body


def sync_file(name: str, dry_run: bool = False) -> bool:
    cpp_path = CPP_ROOT / name
    java_path = JAVA_ROOT / name
    if not cpp_path.exists() or not java_path.exists():
        return False

    cpp_fm, cpp_body = strip_front_matter(cpp_path.read_text(encoding="utf-8"))
    java_fm, java_body = strip_front_matter(java_path.read_text(encoding="utf-8"))

    merged_body = merge_bodies(cpp_body, java_body)
    if merged_body == java_body:
        return False

    if not dry_run:
        java_path.write_text(java_fm + "\n" + merged_body, encoding="utf-8")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not names:
        names = sorted(p.name for p in CPP_ROOT.glob("*leetcode-templates*.md"))

    updated = 0
    for name in names:
        if sync_file(name, dry_run=dry_run):
            updated += 1
            print(f"{'[dry-run] ' if dry_run else ''}updated: {name}")

    print(f"Done. {updated} file(s) {'would be ' if dry_run else ''}updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
