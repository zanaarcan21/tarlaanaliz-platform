# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Platform CLI entrypoint."""

from __future__ import annotations

import argparse
import sys

from src.presentation.cli.commands import expert_management, migrate, run_weekly_planner, seed, subscription_management


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tarlaanaliz")
    subparsers = parser.add_subparsers(dest="command")

    expert_management.register(subparsers)
    migrate.register(subparsers)
    run_weekly_planner.register(subparsers)
    seed.register(subparsers)
    subscription_management.register(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help(sys.stderr)
        return 2
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
