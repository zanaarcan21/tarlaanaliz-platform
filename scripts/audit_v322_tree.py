# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Audit files declared in v3.2.2 platform tree snapshot."""

from __future__ import annotations

import ast
import json
from pathlib import Path

TREE_FILE = Path("docs/archive/2026-02/tarlaanaliz_platform_tree_v3.2.2_FINAL_2026-02-08_OLD.txt")
REPORT_FILE = Path("docs/v3_2_2_tree_audit_report.md")


def parse_tree_paths(tree_text: str) -> list[Path]:
    files: list[Path] = []
    stack: dict[int, str] = {}

    for line in tree_text.splitlines():
        if "├──" not in line and "└──" not in line:
            continue

        if "├──" in line:
            prefix, rest = line.split("├──", 1)
        else:
            prefix, rest = line.split("└──", 1)

        depth = len(prefix) // 4
        entry = rest.strip()
        if " — " in entry:
            entry = entry.split(" — ", 1)[0].strip()

        is_dir = entry.endswith("/")
        name = entry.rstrip("/")

        parent_parts = [stack[d] for d in sorted(stack) if d < depth]
        path = Path(*parent_parts, name)

        stack[depth] = name
        for key in [k for k in stack if k > depth]:
            del stack[key]

        if not is_dir:
            files.append(path)

    return files


def check_python_parse(path: Path) -> str | None:
    try:
        source = path.read_text(encoding="utf-8")
        ast.parse(source)
    except Exception as exc:  # noqa: BLE001
        return str(exc)
    return None


def check_json_parse(path: Path) -> str | None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return str(exc)
    return None


def main() -> int:
    tree_text = TREE_FILE.read_text(encoding="utf-8")
    declared_files = parse_tree_paths(tree_text)

    missing: list[Path] = []
    empty: list[Path] = []
    parse_errors: list[tuple[Path, str]] = []

    for rel_path in declared_files:
        path = Path(rel_path)
        if not path.exists():
            missing.append(rel_path)
            continue

        if path.is_file() and path.stat().st_size == 0:
            empty.append(rel_path)

        suffix = path.suffix.lower()
        err: str | None = None
        if suffix == ".py":
            err = check_python_parse(path)
        elif suffix == ".json":
            err = check_json_parse(path)

        if err:
            parse_errors.append((rel_path, err))

    lines = [
        "BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.",
        "",
        "# v3.2.2 Tree Audit Report",
        "",
        f"- Declared files in tree: **{len(declared_files)}**",
        f"- Missing files: **{len(missing)}**",
        f"- Empty files: **{len(empty)}**",
        f"- Parse errors (.py/.json): **{len(parse_errors)}**",
        "",
    ]

    if missing:
        lines.append("## Missing Files")
        lines.extend([f"- `{p}`" for p in missing])
        lines.append("")

    if empty:
        lines.append("## Empty Files")
        lines.extend([f"- `{p}`" for p in empty])
        lines.append("")

    if parse_errors:
        lines.append("## Parse Errors")
        for path, err in parse_errors:
            lines.append(f"- `{path}`: `{err}`")
        lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print(f"Declared files: {len(declared_files)}")
    print(f"Missing files: {len(missing)}")
    print(f"Empty files: {len(empty)}")
    print(f"Parse errors: {len(parse_errors)}")
    print(f"Report: {REPORT_FILE}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
