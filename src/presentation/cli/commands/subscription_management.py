# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Subscription management CLI commands."""

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
        from src.application.services import subscription_management_service
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
        raise RuntimeError("TODO: src.application.services.subscription_management_service is not available") from exc
    return subscription_management_service


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("subscription", help="Subscription management commands")
    subscription_sub = parser.add_subparsers(dest="subscription_command", required=True)

    subscription_sub.add_parser("list", help="List subscriptions")

    create = subscription_sub.add_parser("create", help="Create subscription")
    create.add_argument("--farmer-id", required=True)
    create.add_argument("--package-code", required=True)

    cancel = subscription_sub.add_parser("cancel", help="Cancel subscription")
    cancel.add_argument("--subscription-id", required=True)

    renew = subscription_sub.add_parser("renew", help="Renew subscription")
    renew.add_argument("--subscription-id", required=True)

    attach_field = subscription_sub.add_parser("attach-field", help="Attach field to subscription")
    attach_field.add_argument("--subscription-id", required=True)
    attach_field.add_argument("--field-id", required=True)

    parser.set_defaults(handler=handle)
    return parser


def _invoke(service: object, method_name: str, **kwargs: object) -> int:
    fn: Callable[..., object] | None = getattr(service, method_name, None)
    if fn is None:
        print(f"Error: missing service method '{method_name}'.", file=sys.stderr)
        return EXIT_ERROR

    try:
        # KR-033: payment verification is enforced in application layer.
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
        print("Subscription command failed.", file=sys.stderr)
        return EXIT_ERROR

    print(result if result is not None else "ok")
    return EXIT_SUCCESS


def handle(args: argparse.Namespace) -> int:
    try:
        service = _load_service()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    if args.subscription_command == "list":
        return _invoke(service, "list_subscriptions")
    if args.subscription_command == "create":
        return _invoke(service, "create_subscription", farmer_id=args.farmer_id, package_code=args.package_code)
    if args.subscription_command == "cancel":
        return _invoke(service, "cancel_subscription", subscription_id=args.subscription_id)
    if args.subscription_command == "renew":
        return _invoke(service, "renew_subscription", subscription_id=args.subscription_id)
    if args.subscription_command == "attach-field":
        return _invoke(service, "attach_field", subscription_id=args.subscription_id, field_id=args.field_id)

    print("Unknown subscription command.", file=sys.stderr)
    return EXIT_VALIDATION


__all__ = ["register", "handle"]
