# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Expert management CLI commands."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_VALIDATION = 2
EXIT_NOT_FOUND = 3
EXIT_FORBIDDEN = 4


def _load_service() -> object:
    try:
        from src.application.services import expert_management_service
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
    except Exception as exc:
        raise RuntimeError("TODO: src.application.services.expert_management_service is not available") from exc
    return expert_management_service


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("expert", help="Expert management commands")
    expert_sub = parser.add_subparsers(dest="expert_command", required=True)

    expert_sub.add_parser("list-experts", help="List experts")

    add_cmd = expert_sub.add_parser("add-expert", help="Add expert")
    add_cmd.add_argument("--name", required=True)
    add_cmd.add_argument("--phone", required=True)

    deactivate = expert_sub.add_parser("deactivate-expert", help="Deactivate expert")
    deactivate.add_argument("--expert-id", required=True)

    assign = expert_sub.add_parser("assign-expert-to-job", help="Assign expert to job")
    assign.add_argument("--expert-id", required=True)
    assign.add_argument("--job-id", required=True)

    parser.set_defaults(handler=handle)
    return parser


def _invoke(service: object, name: str, **kwargs: object) -> int:
    fn: Callable[..., object] | None = getattr(service, name, None)
    if fn is None:
        print(f"Error: missing service method '{name}'.", file=sys.stderr)
        return EXIT_ERROR
    try:
        result = fn(**kwargs)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return EXIT_VALIDATION
    except PermissionError:
        print("Forbidden.", file=sys.stderr)
        return EXIT_FORBIDDEN
    except LookupError:
        print("Not found.", file=sys.stderr)
        return EXIT_NOT_FOUND
    except Exception:
        print("Command failed.", file=sys.stderr)
        return EXIT_ERROR
    print(result if result is not None else "ok")
    return EXIT_SUCCESS


def handle(args: argparse.Namespace) -> int:
    try:
        service = _load_service()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    if args.expert_command == "list-experts":
        return _invoke(service, "list_experts")
    if args.expert_command == "add-expert":
        return _invoke(service, "add_expert", name=args.name, phone=args.phone)
    if args.expert_command == "deactivate-expert":
        return _invoke(service, "deactivate_expert", expert_id=args.expert_id)
    if args.expert_command == "assign-expert-to-job":
        return _invoke(service, "assign_expert_to_job", expert_id=args.expert_id, job_id=args.job_id)

    print("Unknown expert command.", file=sys.stderr)
    return EXIT_VALIDATION


__all__ = ["register", "handle"]
