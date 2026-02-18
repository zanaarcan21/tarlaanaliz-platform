# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Seed baseline data via application service layer only."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

EXIT_OK = 0
EXIT_GENERIC = 1
EXIT_VALIDATION = 2
EXIT_DEP_MISSING = 5


def log(level: str, corr_id: str, message: str, **fields: Any) -> None:
    payload = {"ts": datetime.utcnow().isoformat() + "Z", "level": level, "corr_id": corr_id, "message": message}
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed system data")
    p.add_argument("--apply", action="store_true", help="Apply changes (default dry-run)")
    p.add_argument("--only", choices=["plans", "admin", "fields", "all"], default="all")
    p.add_argument("--corr-id")
    return p.parse_args(argv)


def load_callable(path: str):
    module_name, fn_name = path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    return getattr(mod, fn_name)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corr_id = args.corr_id or str(uuid.uuid4())
    actor = "SYSTEM_SEED"

    target_map = {
        "admin": "src.application.services.seed_service.create_admin_user",
        "plans": "src.application.services.seed_service.create_default_plans",
        "fields": "src.application.services.seed_service.create_sample_fields",
    }
    tasks = list(target_map.keys()) if args.only == "all" else [args.only]

    if not args.apply:
        log("INFO", corr_id, "dry-run seed plan", actor=actor, tasks=tasks)
        return EXIT_OK

    missing: list[str] = []
    for task in tasks:
        ref = target_map[task]
        try:
            fn = load_callable(ref)
        except Exception:
            missing.append(ref)
            continue
        try:
            fn(actor=actor, corr_id=corr_id)
            log("INFO", corr_id, "seed task applied", actor=actor, task=task)
        except TypeError:
            fn()
            log("INFO", corr_id, "seed task applied (fallback signature)", actor=actor, task=task)
        except Exception as exc:
            log("ERROR", corr_id, "seed task failed", task=task, error=str(exc))
            return EXIT_GENERIC

    if missing:
        log("ERROR", corr_id, "seed dependencies missing", missing=missing)
        return EXIT_DEP_MISSING

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
