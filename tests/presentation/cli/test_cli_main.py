# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from __future__ import annotations

from src.presentation.cli.main import main


def test_cli_help_runs() -> None:
    exit_code = main(["--help"])
    assert exit_code == 0


def test_cli_unknown_command_returns_non_zero() -> None:
    exit_code = main(["does-not-exist"])
    assert exit_code != 0


def test_weekly_planner_dry_run_graceful_when_service_missing(capsys) -> None:
    exit_code = main(["weekly-planner", "--dry-run", "--week", "2026-10"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "weekly_planner_service" in captured.err
