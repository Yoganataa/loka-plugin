#!/usr/bin/env python3
"""Validate every source under sources/ against docs/SOURCE_PLUGIN_SPEC.md (apiVersion 1).

Usage: validate.py [sources_dir]
Exit codes: 0 ok, 1 validation errors, 2 usage/IO error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TYPES = {"komik", "anime", "film", "novel", "berita", "audio", "umum"}
PERMISSIONS = {"session", "storage"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,39}$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
HOST_RE = re.compile(r"^https://[a-z0-9.-]+\.[a-z]{2,}/\*$")
LANG_RE = re.compile(r"^(multi|[a-z]{2,3}(-[A-Za-z0-9]{2,8})?)$")
REQUIRED = ("id", "name", "version", "lang", "type", "apiVersion", "hosts", "permissions", "entry")
ALLOWED = set(REQUIRED) | {"description"}
MAX_SOURCE_BYTES = 1_000_000
MAX_JS_BYTES = 512_000
FORBIDDEN_JS = (
    (re.compile(r"\beval\s*\("), "eval() is not allowed"),
    (re.compile(r"\bnew\s+Function\s*\("), "new Function() is not allowed"),
    (re.compile(r"\bFunction\s*\(\s*['\"`]"), "Function() with a string body is not allowed"),
    (re.compile(r"\bimportScripts\s*\("), "importScripts() is not allowed"),
    (re.compile(r"\bimport\s*\(\s*['\"`]https?:"), "dynamic import from a URL is not allowed"),
)


def validate_manifest(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"]
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing field: {key}")
    for key in data:
        if key not in ALLOWED:
            errors.append(f"unknown field: {key}")
    if "id" in data and not (isinstance(data["id"], str) and ID_RE.match(data["id"])):
        errors.append("id must match ^[a-z0-9][a-z0-9-]{1,39}$")
    if "name" in data and not (isinstance(data["name"], str) and data["name"].strip()):
        errors.append("name must be a non-empty string")
    if "version" in data and not (isinstance(data["version"], str) and SEMVER_RE.match(data["version"])):
        errors.append("version must be semver MAJOR.MINOR.PATCH")
    if "lang" in data and not (isinstance(data["lang"], str) and LANG_RE.match(data["lang"])):
        errors.append("lang must be a language code or 'multi'")
    if "type" in data and data["type"] not in TYPES:
        errors.append(f"type must be one of: {', '.join(sorted(TYPES))}")
    api = data.get("apiVersion")
    if "apiVersion" in data and not (isinstance(api, int) and not isinstance(api, bool) and api >= 1):
        errors.append("apiVersion must be an integer >= 1")
    hosts = data.get("hosts")
    if "hosts" in data:
        if not isinstance(hosts, list) or not hosts:
            errors.append("hosts must be a non-empty array")
        else:
            for host in hosts:
                if not (isinstance(host, str) and HOST_RE.match(host)):
                    errors.append(f"host must be https and end with /*: {host!r}")
    perms = data.get("permissions")
    if "permissions" in data:
        if not isinstance(perms, list) or not all(isinstance(p, str) for p in perms):
            errors.append("permissions must be an array of strings")
        else:
            errors.extend(f"unknown permission: {p}" for p in perms if p not in PERMISSIONS)
            if len(set(perms)) != len(perms):
                errors.append("permissions must not repeat")
    if "entry" in data and data["entry"] != "source.js":
        errors.append("entry must be 'source.js'")
    if "description" in data and not isinstance(data["description"], str):
        errors.append("description must be a string")
    return errors


def validate_source_dir(path: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = path / "manifest.json"
    js_path = path / "source.js"
    extra = sorted(p.name for p in path.iterdir() if p.name not in {"manifest.json", "source.js", "README.md"})
    if extra:
        errors.append(f"unexpected files (only manifest.json, source.js, README.md allowed): {', '.join(extra)}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"cannot read manifest.json: {exc}"]
    errors.extend(validate_manifest(manifest))
    if isinstance(manifest, dict) and manifest.get("id") != path.name:
        errors.append(f"folder name '{path.name}' must equal manifest id {manifest.get('id')!r}")
    try:
        js = js_path.read_text(encoding="utf-8")
    except OSError as exc:
        return errors + [f"cannot read source.js: {exc}"]
    if len(js.encode("utf-8")) > MAX_JS_BYTES:
        errors.append(f"source.js larger than {MAX_JS_BYTES} bytes")
    for pattern, message in FORBIDDEN_JS:
        if pattern.search(js):
            errors.append(message)
    total = sum(p.stat().st_size for p in path.iterdir() if p.is_file())
    if total > MAX_SOURCE_BYTES:
        errors.append(f"source folder larger than {MAX_SOURCE_BYTES} bytes")
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "sources"
    if not root.is_dir():
        print(f"sources directory not found: {root}", file=sys.stderr)
        return 2
    failed = False
    seen: dict[str, Path] = {}
    dirs = sorted(p for p in root.iterdir() if p.is_dir())
    for path in dirs:
        errors = validate_source_dir(path)
        if (path / "manifest.json").is_file():
            try:
                sid = json.loads((path / "manifest.json").read_text(encoding="utf-8")).get("id")
                if sid in seen:
                    errors.append(f"duplicate id also in {seen[sid]}")
                seen[sid] = path
            except (OSError, json.JSONDecodeError, AttributeError):
                pass
        if errors:
            failed = True
            for err in errors:
                print(f"{path.name}: {err}", file=sys.stderr)
        else:
            print(f"{path.name}: OK")
    if not dirs:
        print("no sources yet (nothing to validate)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
