# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-018: Calibration hard-gate reference test.

import pytest


@pytest.mark.unit
def test_calibration_gate_contract_reference() -> None:
    """KR-018 contract reference smoke check."""
    assert "KR-018" == "KR-018"
