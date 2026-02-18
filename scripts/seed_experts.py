# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Seed experts via ExpertManagementService with dry-run by default."""

from __future__ import annotations

import argparse
import csv
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
EXIT_NOT_FOUND = 3
EXIT_DEP_MISSING = 5


def log(level: str, corr_id: str, message: str, **fields: Any) -> None:
    payload = {"ts": datetime.utcnow().isoformat() + "Z", "level": level, "corr_id": corr_id, "message": message}
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed experts")
    p.add_argument("--input", required=True)
    p.add_argument("--format", choices=["csv", "json"], required=True)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--deactivate-missing", action="store_true")
    p.add_argument("--corr-id")
    return p.parse_args(argv)


def load_rows(path: Path, fmt: str) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    if fmt == "json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON input must be list")
        return [dict(x) for x in data]

    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return [dict(r) for r in reader]


def normalize(row: dict[str, Any]) -> dict[str, Any]:
    out = {
        "expert_id": str(row.get("expert_id", "")).strip(),
        "display_name": str(row.get("display_name", "")).strip()[:64],
        "specialties": row.get("specialties", []),
        "region": str(row.get("region", "")).strip(),
        "capacity": int(row.get("capacity", 0) or 0),
    }
    if isinstance(out["specialties"], str):
        out["specialties"] = [x.strip() for x in out["specialties"].split(",") if x.strip()]
    return out


def get_service():
    mod = importlib.import_module("src.application.services.expert_management_service")
    cls = getattr(mod, "ExpertManagementService")
    return cls()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corr_id = args.corr_id or str(uuid.uuid4())

    try:
        rows = [normalize(r) for r in load_rows(Path(args.input), args.format)]
    except FileNotFoundError as exc:
        log("ERROR", corr_id, "input not found", path=str(exc))
        return EXIT_NOT_FOUND
    except Exception as exc:
        log("ERROR", corr_id, "invalid input", error=str(exc))
        return EXIT_VALIDATION

    for row in rows:
        if not row["expert_id"]:
            log("ERROR", corr_id, "validation failed: expert_id required")
            return EXIT_VALIDATION

    if not args.apply:
        log("INFO", corr_id, "dry-run expert seed", count=len(rows), deactivate_missing=args.deactivate_missing)
        return EXIT_OK

    try:
        svc = get_service()
    except Exception as exc:
        log("ERROR", corr_id, "dependency missing", detail=f"ExpertManagementService import failed: {exc}")
        return EXIT_DEP_MISSING

    seen_ids = set()
    for row in rows:
        seen_ids.add(row["expert_id"])
        try:
            svc.create_or_update_expert(
                expert_id=row["expert_id"],
                display_name=row["display_name"],
                specialties=row["specialties"],
                region=row["region"],
                capacity=row["capacity"],
                corr_id=corr_id,
            )
            log("INFO", corr_id, "expert upserted", expert_id=row["expert_id"])
        except TypeError:
            svc.create_or_update_expert(**{k: row[k] for k in ["expert_id", "display_name", "specialties", "region", "capacity"]})
            log("INFO", corr_id, "expert upserted (fallback signature)", expert_id=row["expert_id"])
        except Exception as exc:
            log("ERROR", corr_id, "expert upsert failed", expert_id=row["expert_id"], error=str(exc))
            return EXIT_GENERIC

    if args.deactivate_missing:
        try:
            if hasattr(svc, "deactivate_missing"):
                svc.deactivate_missing(expert_ids=sorted(seen_ids), corr_id=corr_id)
            elif hasattr(svc, "deactivate_missing_experts"):
                svc.deactivate_missing_experts(expert_ids=sorted(seen_ids), corr_id=corr_id)
            else:
                log("WARNING", corr_id, "deactivate-missing requested but no service method")
        except Exception as exc:
            log("ERROR", corr_id, "deactivate-missing failed", error=str(exc))
            return EXIT_GENERIC

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
