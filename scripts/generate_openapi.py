# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Generate OpenAPI spec from src.presentation.api.main:create_app."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from typing import Any

EXIT_OK = 0
EXIT_GENERIC = 1
EXIT_VALIDATION = 2
EXIT_DEP_MISSING = 5


def log(level: str, corr_id: str, message: str, **fields: Any) -> None:
    payload = {"ts": datetime.utcnow().isoformat() + "Z", "level": level, "corr_id": corr_id, "message": message}
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def to_yaml(obj: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.append(f"{pad}{k}:")
                out.append(to_yaml(v, indent + 1))
            else:
                out.append(f"{pad}{k}: {scalar(v)}")
        return "\n".join(out)
    if isinstance(obj, list):
        out = []
        for item in obj:
            if isinstance(item, (dict, list)):
                out.append(f"{pad}-")
                out.append(to_yaml(item, indent + 1))
            else:
                out.append(f"{pad}- {scalar(item)}")
        return "\n".join(out)
    return f"{pad}{scalar(obj)}"


def scalar(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    text = str(v).replace('"', '\\"')
    return f'"{text}"'


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate OpenAPI spec")
    p.add_argument("--out", default="docs/api/openapi.yaml")
    p.add_argument("--format", choices=["yaml", "json"], default="yaml")
    p.add_argument("--validate", action="store_true")
    p.add_argument("--yes", action="store_true", help="Apply write (default dry-run)")
    return p.parse_args(argv)


def basic_validate(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "openapi" not in spec:
        errors.append("missing openapi version")
    if "paths" not in spec or not isinstance(spec["paths"], dict):
        errors.append("missing paths")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corr_id = str(uuid.uuid4())

    try:
        mod = importlib.import_module("src.presentation.api.main")
        app = mod.create_app()
        spec = app.openapi()
    except Exception as exc:
        log("ERROR", corr_id, "failed to import/create app", error=str(exc))
        return EXIT_DEP_MISSING

    paths = spec.get("paths", {})
    invalid_paths = [
        p
        for p in paths
        if p != "/health" and not p.startswith("/v1/") and not p.startswith("/api/v1/")
    ]
    if invalid_paths:
        log("WARNING", corr_id, "non-v1 business paths detected", paths=invalid_paths)

    if args.validate:
        errors = basic_validate(spec)
        if errors:
            log("ERROR", corr_id, "openapi validation failed", errors=errors)
            return EXIT_VALIDATION

    out = Path(args.out)
    if args.format == "json":
        rendered = json.dumps(spec, ensure_ascii=False, indent=2)
    else:
        try:
            import yaml  # type: ignore

            rendered = yaml.safe_dump(spec, sort_keys=False, allow_unicode=True)
        except Exception:
            rendered = to_yaml(spec) + "\n"

    if not args.yes:
        log("INFO", corr_id, "dry-run: spec generated, not written", out=str(out), format=args.format)
        print(rendered)
        return EXIT_OK

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    log("INFO", corr_id, "openapi written", out=str(out), format=args.format)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
