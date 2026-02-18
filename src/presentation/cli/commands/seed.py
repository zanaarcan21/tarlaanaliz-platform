# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Seed data CLI commands."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_VALIDATION = 2


def _load_service() -> object:
    try:
        from src.application.services import seed_service
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
        raise RuntimeError("TODO: src.application.services.seed_service is not available") from exc
    return seed_service


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("seed", help="Seed commands")
    seed_sub = parser.add_subparsers(dest="seed_command", required=True)

    seed_sub.add_parser("seed-all", help="Seed all baseline data")
    seed_sub.add_parser("seed-minimal", help="Seed minimal baseline data")

    admin = seed_sub.add_parser("seed-admin", help="Seed admin user/data")
    admin.add_argument("--confirm", default="")
    admin.add_argument("--force", action="store_true")

    parser.set_defaults(handler=handle)
    return parser


def _invoke(service: object, name: str, **kwargs: object) -> int:
    fn: Callable[..., object] | None = getattr(service, name, None)
    if fn is None:
        print(f"Error: missing seed service method '{name}'.", file=sys.stderr)
        return EXIT_ERROR
    try:
        result = fn(**kwargs)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return EXIT_VALIDATION
    except Exception:
        print("Seed command failed.", file=sys.stderr)
        return EXIT_ERROR

    print(result if result is not None else "ok")
    return EXIT_SUCCESS


def handle(args: argparse.Namespace) -> int:
    try:
        service = _load_service()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    if args.seed_command == "seed-all":
        return _invoke(service, "seed_all")

    if args.seed_command == "seed-minimal":
        return _invoke(service, "seed_minimal")

    if args.seed_command == "seed-admin":
        if not args.force and args.confirm != "I_UNDERSTAND":
            print("Validation error: seed-admin requires --confirm I_UNDERSTAND or --force.", file=sys.stderr)
            return EXIT_VALIDATION
        return _invoke(service, "seed_admin", force=bool(args.force))

    print("Unknown seed command.", file=sys.stderr)
    return EXIT_VALIDATION


__all__ = ["register", "handle"]
