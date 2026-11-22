#!/usr/bin/env python3
"""Build the static catalog (index.json + packages/*.zip) from sources/.

Usage: build_index.py <base_url> [--sources DIR] [--out DIR] [--name NAME]

Packages are deterministic zips (fixed timestamps, sorted entries) holding exactly
manifest.json and source.js. The index format is the proposal in docs/DATA_FORMATS.md.
Run tools/validate.py first; this script re-checks the manifest fields it publishes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

FIXED_TIME = (2020, 1, 1, 0, 0, 0)
PACKAGE_FILES = ("manifest.json", "source.js")


def build_package(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in PACKAGE_FILES:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, (src / name).read_bytes())
    return hashlib.sha256(dest.read_bytes()).hexdigest()


def build(sources: Path, out: Path, base_url: str, name: str) -> dict:
    base = base_url.rstrip("/")
    entries = []
    for src in sorted(p for p in sources.iterdir() if p.is_dir()):
        manifest = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
        sid, version = manifest["id"], manifest["version"]
        rel = f"packages/{sid}-{version}.zip"
        digest = build_package(src, out / rel)
        entries.append({
            "id": sid,
            "name": manifest["name"],
            "version": version,
            "lang": manifest["lang"],
            "type": manifest["type"],
            "apiVersion": manifest["apiVersion"],
            "package": f"{base}/{rel}",
            "sha256": digest,
            "hosts": manifest["hosts"],
            "permissions": manifest["permissions"],
        })
    index = {"catalogVersion": 1, "name": name, "sources": entries}
    (out / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--sources", default=str(Path(__file__).resolve().parent.parent / "sources"))
    parser.add_argument("--out", default="dist")
    parser.add_argument("--name", default="Loka Plugin")
    args = parser.parse_args()
    if not args.base_url.startswith("https://"):
        print("base_url must be https", file=sys.stderr)
        return 2
    sources, out = Path(args.sources), Path(args.out)
    if not sources.is_dir():
        print(f"sources directory not found: {sources}", file=sys.stderr)
        return 2
    try:
        index = build(sources, out, args.base_url, args.name)
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out / 'index.json'} with {len(index['sources'])} source(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
