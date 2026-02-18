# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Export training dataset from manifest or DB adapter stub with KR-018 filtering."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_GENERIC = 1
EXIT_VALIDATION = 2
EXIT_NOT_FOUND = 3
EXIT_DEP_MISSING = 5


@dataclass
class Record:
    item_id: str
    image_path: str
    label: dict[str, Any]
    calibrated: bool
    qc_status: str


def log(level: str, corr_id: str, message: str, **fields: Any) -> None:
    payload = {"ts": datetime.utcnow().isoformat() + "Z", "level": level, "corr_id": corr_id, "message": message}
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def load_manifest(path: Path) -> list[Record]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("manifest must be list")
    out: list[Record] = []
    for row in data:
        out.append(
            Record(
                item_id=str(row["item_id"]),
                image_path=str(row["image_path"]),
                label=dict(row.get("label", {})),
                calibrated=bool(row.get("calibrated", False)),
                qc_status=str(row.get("qc_status", "FAIL")).upper(),
            )
        )
    return out


def load_db_placeholder() -> list[Record]:
    raise RuntimeError("DB adapter not implemented yet. Use --source manifest.")


def passes_filters(rec: Record, qc: str, calibrated: str) -> bool:
    qc_ok = qc == "ANY" or rec.qc_status == qc
    if calibrated == "any":
        cal_ok = True
    elif calibrated == "true":
        cal_ok = rec.calibrated is True
    else:
        cal_ok = rec.calibrated is False
    return qc_ok and cal_ok


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export training dataset")
    p.add_argument("--source", choices=["manifest", "db"], default="manifest")
    p.add_argument("--manifest-path", default="exports/manifest.json")
    p.add_argument("--out-dir", default="exports")
    p.add_argument("--qc", choices=["PASS", "WARN", "FAIL", "ANY"], default="PASS")
    p.add_argument("--calibrated", choices=["true", "false", "any"], default="true")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corr_id = str(uuid.uuid4())

    if args.limit is not None and args.limit <= 0:
        log("ERROR", corr_id, "invalid limit", limit=args.limit)
        return EXIT_VALIDATION

    try:
        records = load_manifest(Path(args.manifest_path)) if args.source == "manifest" else load_db_placeholder()
    except FileNotFoundError as exc:
        log("ERROR", corr_id, "source not found", path=str(exc))
        return EXIT_NOT_FOUND
    except RuntimeError as exc:
        log("ERROR", corr_id, "dependency missing", detail=str(exc))
        return EXIT_DEP_MISSING
    except Exception as exc:
        log("ERROR", corr_id, "source load failed", error=str(exc))
        return EXIT_GENERIC

    selected = [r for r in records if passes_filters(r, args.qc, args.calibrated)]
    if args.limit is not None:
        selected = selected[: args.limit]

    version = datetime.utcnow().strftime("dataset_%Y%m%dT%H%M%SZ")
    base = Path(args.out_dir) / version
    images_dir = base / "images"
    labels_dir = base / "labels"
    metadata_jsonl = base / "metadata.jsonl"

    if args.dry_run:
        log("INFO", corr_id, "dry-run export plan", out=str(base), count=len(selected), qc=args.qc, calibrated=args.calibrated)
        return EXIT_OK

    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    source_refs: list[str] = []
    with metadata_jsonl.open("w", encoding="utf-8") as mf:
        for rec in selected:
            src = Path(rec.image_path)
            if not src.exists():
                log("ERROR", corr_id, "image not found", image_path=rec.image_path, item_id=rec.item_id)
                return EXIT_NOT_FOUND
            dst_img = images_dir / f"{rec.item_id}{src.suffix or '.dat'}"
            shutil.copy2(src, dst_img)
            label_path = labels_dir / f"{rec.item_id}.json"
            label_path.write_text(json.dumps(rec.label, ensure_ascii=False), encoding="utf-8")
            meta = {
                "corr_id": corr_id,
                "export_ts": datetime.utcnow().isoformat() + "Z",
                "item_id": rec.item_id,
                "calibrated": rec.calibrated,
                "qc_status": rec.qc_status,
                "image": str(dst_img),
                "label": str(label_path),
            }
            source_refs.append(rec.item_id)
            mf.write(json.dumps(meta, ensure_ascii=False) + "\n")

    summary = {
        "corr_id": corr_id,
        "export_ts": datetime.utcnow().isoformat() + "Z",
        "filters": {"qc": args.qc, "calibrated": args.calibrated, "limit": args.limit},
        "counts": {"selected": len(selected), "total": len(records)},
        "source_refs": source_refs,
    }
    (base / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log("INFO", corr_id, "dataset export complete", out=str(base), selected=len(selected))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
