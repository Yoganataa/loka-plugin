#!/usr/bin/env python3
"""Fail when a folder, file, or declared identifier carries the brand name.

Brand names belong in user-visible text, the applicationId/package namespace, and the
``loka://`` URL scheme, not in paths or in class, function, or variable names.

Usage: check_naming.py [root]
Exit codes: 0 ok, 1 violations, 2 usage error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BRAND = re.compile(r"loka(?!si)", re.IGNORECASE)
SKIP_DIRS = {".git", "node_modules", ".build"}
CODE_SUFFIXES = {".js", ".mjs", ".ts", ".kt", ".kts", ".py", ".java", ".sh"}
DECLARATION = re.compile(r"\b(?:function|class|object|interface|fun|def|const|let|var|val|enum)\s+([A-Za-z_$][\w$]*)")
HTML_SCRIPT = re.compile(r"<script[^>]*>(.*?)</script>", re.DOTALL)


def walk(root: Path):
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path, rel


def declared_names(text: str) -> list[str]:
    return DECLARATION.findall(text)


def check(root: Path) -> list[str]:
    problems: list[str] = []
    for path, rel in walk(root):
        if any(BRAND.search(part) for part in rel.parts):
            problems.append(f"{rel}: path contains the brand name")
            continue
        if not path.is_file():
            continue
        text = ""
        if path.suffix in CODE_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
        elif path.suffix == ".html":
            text = "\n".join(HTML_SCRIPT.findall(path.read_text(encoding="utf-8", errors="replace")))
        for name in declared_names(text):
            if BRAND.search(name):
                problems.append(f"{rel}: declared name '{name}' contains the brand name")
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    problems = check(root)
    for line in problems:
        print(f"FAIL {line}")
    if not problems:
        print("PASS naming: no brand names in paths or declared identifiers")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
