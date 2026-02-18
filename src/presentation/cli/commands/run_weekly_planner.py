# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Weekly planner runner command."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import uuid
from typing import Callable

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_VALIDATION = 2

_WEEK_PATTERN = re.compile(r"^\d{4}-(0[1-9]|[1-4][0-9]|5[0-3])$")


def _load_service() -> object:
    try:
        from src.application.services import weekly_planner_service
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
        raise RuntimeError("TODO: src.application.services.weekly_planner_service is not available") from exc
    return weekly_planner_service


def _default_week() -> str:
    year, week, _ = dt.date.today().isocalendar()
    return f"{year}-{week:02d}"


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("weekly-planner", help="Run weekly planner job")
    parser.add_argument("--week", default=_default_week(), help="ISO week format YYYY-WW")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--corr-id")
    parser.add_argument("--max-work-days", type=int, default=6)
    parser.add_argument("--daily-capacity", type=int, default=2500)
    parser.set_defaults(handler=handle)
    return parser


def _validate(args: argparse.Namespace) -> str | None:
    # KR-015
    if not _WEEK_PATTERN.match(args.week):
        return "--week must match YYYY-WW"
    if args.max_work_days < 1 or args.max_work_days > 6:
        return "--max-work-days must be in range 1..6"
    if args.daily_capacity < 2500 or args.daily_capacity > 3000:
        return "--daily-capacity must be in range 2500..3000"
    return None


def handle(args: argparse.Namespace) -> int:
    error = _validate(args)
    if error:
        print(f"Validation error: {error}", file=sys.stderr)
        return EXIT_VALIDATION

    corr_id = args.corr_id or str(uuid.uuid4())

    try:
        service = _load_service()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    runner: Callable[..., object] | None = getattr(service, "run", None)
    if runner is None:
        print("Error: weekly_planner_service.run is missing.", file=sys.stderr)
        return EXIT_ERROR

    try:
        result = runner(
            week=args.week,
            dry_run=args.dry_run,
            corr_id=corr_id,
            max_work_days=args.max_work_days,
            daily_capacity_donum=args.daily_capacity,
        )
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return EXIT_VALIDATION
    except Exception:
        print("Weekly planner execution failed.", file=sys.stderr)
        return EXIT_ERROR

    if result is not None:
        print(result)
    else:
        print(f"weekly planner executed (corr_id={corr_id})")
    return EXIT_SUCCESS


__all__ = ["register", "handle"]
