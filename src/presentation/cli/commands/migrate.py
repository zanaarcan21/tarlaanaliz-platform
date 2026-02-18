# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Database migration CLI commands."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Callable

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_VALIDATION = 2


def _db_url_from_env() -> str | None:
    return os.getenv("DATABASE_URL") or os.getenv("DB_URL")


def _load_runner() -> object:
    try:
        from src.infrastructure.db import migration_runner
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
        raise RuntimeError("TODO: migration runner adapter is not available") from exc
    return migration_runner


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("migrate", help="Database migration commands")
    migrate_sub = parser.add_subparsers(dest="migrate_command", required=True)

    upgrade = migrate_sub.add_parser("upgrade", help="Upgrade to target revision")
    upgrade.add_argument("revision", nargs="?", default="head")

    downgrade = migrate_sub.add_parser("downgrade", help="Downgrade to target revision")
    downgrade.add_argument("revision")

    migrate_sub.add_parser("current", help="Show current revision")
    migrate_sub.add_parser("history", help="Show revision history")

    parser.set_defaults(handler=handle)
    return parser


def _invoke(runner: object, method_name: str, **kwargs: object) -> int:
    fn: Callable[..., object] | None = getattr(runner, method_name, None)
    if fn is None:
        print(f"Error: missing runner method '{method_name}'.", file=sys.stderr)
        return EXIT_ERROR
    try:
        result = fn(**kwargs)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return EXIT_VALIDATION
    except Exception:
        print("Migration command failed.", file=sys.stderr)
        return EXIT_ERROR
    if result is not None:
        print(result)
    return EXIT_SUCCESS


def handle(args: argparse.Namespace) -> int:
    db_url = _db_url_from_env()
    if not db_url:
        print("Validation error: DATABASE_URL/DB_URL is required.", file=sys.stderr)
        return EXIT_VALIDATION

    try:
        runner = _load_runner()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    if args.migrate_command == "upgrade":
        return _invoke(runner, "upgrade", db_url=db_url, revision=args.revision)
    if args.migrate_command == "downgrade":
        return _invoke(runner, "downgrade", db_url=db_url, revision=args.revision)
    if args.migrate_command == "current":
        return _invoke(runner, "current", db_url=db_url)
    if args.migrate_command == "history":
        return _invoke(runner, "history", db_url=db_url)

    print("Unknown migrate command.", file=sys.stderr)
    return EXIT_VALIDATION


__all__ = ["register", "handle"]
