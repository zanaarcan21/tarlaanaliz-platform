# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-081: Field contract checks.

from __future__ import annotations

from decimal import Decimal

import pytest

from tests.fixtures.domain_fixtures import as_contract_payload


def test_field_contract_contains_geometry_and_parcel_components(field_entity: object) -> None:
    payload = as_contract_payload(field_entity)

    required = {"province", "district", "village", "ada", "parsel", "geometry"}
    assert required.issubset(payload.keys()), "KR-081 contract mismatch in field payload."
    assert payload["geometry"]["type"] == "Polygon"


def test_field_parcel_ref_and_area_donum_are_consistent(field_entity: object) -> None:
    assert field_entity.parcel_ref == "Konya/Selcuklu/Sancak/123/45"
    assert field_entity.area_donum == Decimal("2500"), "Expected deterministic dönüm conversion."


def test_fields_api_unavailable_yet(fastapi_app_factory: object) -> None:
    if fastapi_app_factory is None:
        pytest.skip("FastAPI app factory bulunamadı; /fields integration testi skip edildi.")

    pytest.xfail("/fields endpoint henüz implement değil; domain-level contract testleri aktif.")
