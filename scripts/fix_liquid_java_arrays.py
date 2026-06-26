#!/usr/bin/env python3
"""Fix Java array literals that break Jekyll Liquid ({{ ... }})."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA = re.compile(r"```java\s*\n(.*?)```", re.S)


def fix_arrays(code: str) -> str:
    # {{1, 0}, {-1, 0}} -> new int[][] { new int[] {1, 0}, ... }
    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(",")]
        if len(parts) % 2 != 0:
            return m.group(0)
        pairs = []
        for i in range(0, len(parts), 2):
            pairs.append(f"new int[] {{{parts[i]}, {parts[i+1]}}}")
        return "new int[][] {" + ", ".join(pairs) + "}"

    # Escaped mess from bad conversion: {{\{1, 0\}, ...}}
    code = re.sub(r"\{\{\\\{([^}]+)\\\}[^}]*\}\}", repl, code)
    code = re.sub(
        r"\{\{(\s*-?\d+\s*,\s*-?\d+\s*)(?:,\s*\{?\s*-?\d+\s*,\s*-?\d+\s*\}?)+\}\}",
        repl,
        code,
    )
    # Simple {{a, b}, {c, d}} on one line
    code = re.sub(
        r"\{\{(\d+\s*,\s*-?\d+)\s*,\s*\{(-?\d+\s*,\s*-?\d+)\s*\}\s*,\s*\{(-?\d+\s*,\s*-?\d+)\s*\}\s*,\s*\{(-?\d+\s*,\s*-?\d+)\s*\}\}\}",
        r"new int[][] {new int[] {\1}, new int[] {\2}, new int[] {\3}, new int[] {\4}}",
        code,
    )
    code = re.sub(
        r"\{\{(\d+\s*,\s*\d+)\s*,\s*\{(\d+\s*,\s*\d+)\s*\}\}\}",
        r"new int[][] {new int[] {\1}, new int[] {\2}}",
        code,
    )
    return code


def process(path: Path) -> bool:
    if "{% raw %}" in path.read_text(encoding="utf-8"):
        return False
    text = path.read_text(encoding="utf-8")
    if "{{" not in text:
        return False

    def block_repl(m: re.Match[str]) -> str:
        fixed = fix_arrays(m.group(1))
        if "{{" in fixed:
            fixed = fixed.replace("{{", "{ {").replace("}}", "} }")
        return "```java\n" + fixed + "```"

    updated = JAVA.sub(block_repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = sum(1 for p in ROOT.glob("_posts/*.md") if process(p))
    print(f"Fixed Liquid-breaking arrays in {n} posts")


if __name__ == "__main__":
    main()
