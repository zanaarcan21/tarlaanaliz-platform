# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Analyze JSONL API logs for rate-limit behavior and trends."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

EXIT_OK = 0
EXIT_GENERIC = 1
EXIT_VALIDATION = 2
EXIT_NOT_FOUND = 3


@dataclass
class Report:
    corr_id: str
    processed: int
    skipped: int
    top_rate_limited_routes: list[dict[str, Any]]
    top_talkers: list[dict[str, Any]]
    status_distribution: dict[str, int]
    trend_429_by_minute: list[dict[str, Any]]


def _log(level: str, corr_id: str, message: str, **fields: Any) -> None:
    payload = {"ts": datetime.utcnow().isoformat() + "Z", "level": level, "corr_id": corr_id, "message": message}
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def _mask_ip(ip: str | None) -> str | None:
    if not ip:
        return ip
    if "." in ip:
        parts = ip.split(".")
        if len(parts) == 4 and all(p.isdigit() for p in parts):
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    return ip


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    return datetime.fromisoformat(text)


def _iter_lines(paths: list[str]) -> Iterable[str]:
    if not paths:
        for line in sys.stdin:
            yield line
        return
    for p in paths:
        if p == "-":
            for line in sys.stdin:
                yield line
            continue
        file_path = Path(p)
        if not file_path.exists():
            raise FileNotFoundError(str(file_path))
        with file_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                yield line


def _status_bucket(status: int) -> str:
    if status == 429:
        return "429"
    if 500 <= status <= 599:
        return "5xx"
    if 400 <= status <= 499:
        return "4xx"
    if 200 <= status <= 299:
        return "200"
    return str(status)


def build_report(args: argparse.Namespace, corr_id: str) -> Report:
    since_dt = _parse_dt(args.since)
    until_dt = _parse_dt(args.until)

    routes = Counter()
    talkers = Counter()
    statuses = Counter()
    trend_429: dict[str, int] = defaultdict(int)

    processed = 0
    skipped = 0

    for raw in _iter_lines(args.paths):
        line = raw.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue

        ts_value = rec.get("ts")
        ts_dt = None
        if isinstance(ts_value, str):
            try:
                ts_dt = _parse_dt(ts_value)
            except ValueError:
                skipped += 1
                continue
        if since_dt and ts_dt and ts_dt < since_dt:
            continue
        if until_dt and ts_dt and ts_dt > until_dt:
            continue

        route = str(rec.get("route", "unknown"))
        if args.route_prefix and not route.startswith(args.route_prefix):
            continue

        status = rec.get("status")
        try:
            status_int = int(status)
        except (TypeError, ValueError):
            status_int = 0

        ip = rec.get("client_ip_masked")
        if not ip and rec.get("client_ip"):
            ip = _mask_ip(str(rec.get("client_ip")))
        elif isinstance(ip, str):
            ip = _mask_ip(ip)
        if not ip:
            ip = "unknown"

        rate_limited = bool(rec.get("rate_limited")) or status_int == 429

        processed += 1
        statuses[_status_bucket(status_int)] += 1
        talkers[ip] += 1
        if rate_limited:
            routes[route] += 1
            if ts_dt:
                minute = ts_dt.replace(second=0, microsecond=0).isoformat()
                trend_429[minute] += 1

    top_routes = [{"route": r, "count": c} for r, c in routes.most_common(args.top)]
    top_talkers = [{"ip_block": ip, "count": c} for ip, c in talkers.most_common(args.top)]
    trend_sorted = [{"minute": k, "count": trend_429[k]} for k in sorted(trend_429.keys())]

    return Report(
        corr_id=corr_id,
        processed=processed,
        skipped=skipped,
        top_rate_limited_routes=top_routes,
        top_talkers=top_talkers,
        status_distribution=dict(statuses),
        trend_429_by_minute=trend_sorted,
    )


def _print_text(report: Report) -> None:
    print(f"corr_id={report.corr_id}")
    print(f"processed={report.processed} skipped={report.skipped}")

    print("\nTop rate-limited routes:")
    for row in report.top_rate_limited_routes:
        print(f"- {row['route']}: {row['count']}")

    print("\nTop talkers (/24 masked):")
    for row in report.top_talkers:
        print(f"- {row['ip_block']}: {row['count']}")

    print("\nStatus distribution:")
    for key in ["200", "4xx", "5xx", "429"]:
        print(f"- {key}: {report.status_distribution.get(key, 0)}")

    print("\n429 trend (minute):")
    max_count = max((x["count"] for x in report.trend_429_by_minute), default=0)
    for row in report.trend_429_by_minute:
        count = row["count"]
        bar_len = int((count / max_count) * 40) if max_count else 0
        print(f"- {row['minute']} | {'#' * bar_len} ({count})")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Rate-limit log analysis")
    p.add_argument("paths", nargs="*", help="JSONL log files. Omit for stdin.")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--since", help="ISO-8601 inclusive start")
    p.add_argument("--until", help="ISO-8601 inclusive end")
    p.add_argument("--route-prefix", help="Only include routes with this prefix")
    p.add_argument("--json-out", help="Write report JSON to file path or '-' for stdout")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corr_id = str(uuid.uuid4())

    if args.top <= 0:
        _log("ERROR", corr_id, "invalid --top", top=args.top)
        return EXIT_VALIDATION

    try:
        report = build_report(args, corr_id)
    except FileNotFoundError as exc:
        _log("ERROR", corr_id, "log file not found", path=str(exc))
        return EXIT_NOT_FOUND
    except Exception as exc:  # pragma: no cover
        _log("ERROR", corr_id, "analysis failed", error=str(exc))
        return EXIT_GENERIC

    _print_text(report)

    if args.json_out:
        payload = report.__dict__
        if args.json_out == "-":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            Path(args.json_out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            _log("INFO", corr_id, "json report written", out=args.json_out)

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
