#!/usr/bin/env python3
"""Dependency-free package checks for the corpify skill.

Verifies the things that silently drift:
  1. Root SKILL.md and .github/skills/corpify/SKILL.md are byte-identical.
  2. SKILL.md frontmatter `name` is "corpify".
  3. SKILL.md `metadata.version` matches .claude-plugin/plugin.json "version".
  4. That version appears in README.md's Version History.

Exit code 0 = all good, 1 = one or more checks failed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict:
    """Parse the leading --- YAML block just enough for name and metadata.version."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    block = text[3:end]
    data, in_metadata = {}, False
    for line in block.splitlines():
        if not line.strip():
            continue
        if re.match(r"^metadata:\s*$", line):
            in_metadata = True
            continue
        m = re.match(r"^(\s*)([\w-]+):\s*(.*)$", line)
        if not m:
            continue
        indent, key, val = m.group(1), m.group(2), m.group(3).strip().strip("'\"")
        if in_metadata and indent:
            data[f"metadata.{key}"] = val
        else:
            in_metadata = False
            data[key] = val
    return data


def main() -> int:
    errors = []

    root_skill = ROOT / "SKILL.md"
    copy_skill = ROOT / ".github" / "skills" / "corpify" / "SKILL.md"
    plugin = ROOT / ".claude-plugin" / "plugin.json"
    readme = ROOT / "README.md"

    for p in (root_skill, copy_skill, plugin, readme):
        if not p.exists():
            errors.append(f"missing file: {p.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1

    if read(root_skill) != read(copy_skill):
        errors.append("SKILL.md and .github/skills/corpify/SKILL.md are out of sync")

    fm = frontmatter(read(root_skill))
    if fm.get("name") != "corpify":
        errors.append(f"SKILL.md name is {fm.get('name')!r}, expected 'corpify'")

    skill_version = fm.get("metadata.version")
    plugin_version = json.loads(read(plugin)).get("version")
    if skill_version != plugin_version:
        errors.append(
            f"version mismatch: SKILL.md {skill_version!r} vs plugin.json {plugin_version!r}"
        )

    if skill_version and skill_version not in read(readme):
        errors.append(f"README.md has no Version History entry for {skill_version}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1

    print(f"OK: corpify v{skill_version} - all package checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
