# PATH: src/core/domain/value_objects/weather_block_status.py
# DESC: WeatherBlockStatus VO; rapor durumu enum.
# SSOT: KR-015-5 (reschedule/force majeure), KR-028 (mission lifecycle)
"""
WeatherBlockStatus value object.

Hava durumu engeli raporunun durumunu temsil eder.
KR-015-5: Weather block force majeure olarak değerlendirilir;
reschedule token tüketmez.
"""
from __future__ import annotations

from enum import Enum


class WeatherBlockStatus(str, Enum):
    """Hava durumu engeli rapor durumları.

    * PENDING     -- Rapor oluşturuldu, doğrulama bekliyor.
    * CONFIRMED   -- Hava engeli doğrulandı (force majeure, token tüketmez).
    * REJECTED    -- Rapor reddedildi (hava engeli geçerli değil).
    * EXPIRED     -- Rapor süresi doldu (zamanında işlenmedi).
    * RESOLVED    -- Hava engeli kalktı; görev yeniden planlanabilir.
    """

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    RESOLVED = "RESOLVED"


# Geçerli durum geçişleri
VALID_WEATHER_BLOCK_TRANSITIONS: dict[WeatherBlockStatus, frozenset[WeatherBlockStatus]] = {
    WeatherBlockStatus.PENDING: frozenset({
        WeatherBlockStatus.CONFIRMED,
        WeatherBlockStatus.REJECTED,
        WeatherBlockStatus.EXPIRED,
    }),
    WeatherBlockStatus.CONFIRMED: frozenset({
        WeatherBlockStatus.RESOLVED,
    }),
    WeatherBlockStatus.REJECTED: frozenset(),
    WeatherBlockStatus.EXPIRED: frozenset(),
    WeatherBlockStatus.RESOLVED: frozenset(),
}

# Terminal durumlar: bu durumlardan çıkış yoktur
TERMINAL_WEATHER_BLOCK_STATUSES: frozenset[WeatherBlockStatus] = frozenset({
    WeatherBlockStatus.REJECTED,
    WeatherBlockStatus.EXPIRED,
    WeatherBlockStatus.RESOLVED,
})


def is_valid_weather_block_transition(
    current: WeatherBlockStatus,
    target: WeatherBlockStatus,
) -> bool:
    """Verilen geçiş kurallara uygun mu?"""
    allowed = VALID_WEATHER_BLOCK_TRANSITIONS.get(current, frozenset())
    return target in allowed


def is_force_majeure(status: WeatherBlockStatus) -> bool:
    """Bu durum force majeure (token tüketmeyen reschedule) tetikler mi?

    KR-015-5: CONFIRMED weather block, reschedule token tüketmez.
    """
    return status == WeatherBlockStatus.CONFIRMED


def is_blocking_mission(status: WeatherBlockStatus) -> bool:
    """Bu durum görevi engelliyor mu?

    PENDING veya CONFIRMED durumda görev uçurulamaz.
    """
    return status in {WeatherBlockStatus.PENDING, WeatherBlockStatus.CONFIRMED}
