# PATH: src/core/domain/value_objects/payment_status.py
# DESC: PaymentStatus VO; odeme durumu enum ve KR-033 gate.
# SSOT: KR-033 (odeme ve manuel onay)
"""
PaymentStatus value object.

Odeme durumunu temsil eden enum ve gecis kurallari.
KR-033: PaymentIntent olmadan paid state olmaz; dekont + manuel onay + audit.
Entity'deki PaymentStatus enum'u ile SSOT uyumludur; bu VO
domain genelinde kullanilabilir referans noktasidir.
"""
from __future__ import annotations

from enum import Enum


class PaymentStatus(str, Enum):
    """KR-033 kanonik odeme durumlari.

    * PAYMENT_PENDING -- Odeme bekleniyor (varsayilan baslangic durumu).
    * PAID           -- Odeme onaylandi (provider webhook veya admin onayi).
    * REJECTED       -- Odeme reddedildi (dekont uyumsuzlugu vb.).
    * EXPIRED        -- Sure asimi (7 gun icinde odeme gelmezse).
    * CANCELLED      -- Kullanici tarafindan iptal (yalnizca PAYMENT_PENDING iken).
    * REFUNDED       -- Iade yapildi (yalnizca PAID sonrasi admin aksiyonu).
    """

    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAID = "PAID"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# KR-033: Gecerli durum gecisleri
VALID_PAYMENT_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    PaymentStatus.PAYMENT_PENDING: {
        PaymentStatus.PAID,
        PaymentStatus.REJECTED,
        PaymentStatus.EXPIRED,
        PaymentStatus.CANCELLED,
    },
    PaymentStatus.PAID: {
        PaymentStatus.REFUNDED,
    },
    PaymentStatus.REJECTED: set(),
    PaymentStatus.EXPIRED: set(),
    PaymentStatus.CANCELLED: set(),
    PaymentStatus.REFUNDED: set(),
}

# Terminal durumlar: bu durumlardan cikis yoktur
TERMINAL_PAYMENT_STATUSES: frozenset[PaymentStatus] = frozenset({
    PaymentStatus.REJECTED,
    PaymentStatus.EXPIRED,
    PaymentStatus.CANCELLED,
    PaymentStatus.REFUNDED,
})


def is_valid_payment_transition(
    current: PaymentStatus,
    target: PaymentStatus,
) -> bool:
    """Verilen gecis KR-033 kurallarina uygun mu?"""
    allowed = VALID_PAYMENT_TRANSITIONS.get(current, set())
    return target in allowed


def requires_payment_intent(status: PaymentStatus) -> bool:
    """KR-033: PAID durumu icin PaymentIntent zorunlu mu?

    PAID state'e gecis yalnizca PaymentIntent uzerinden olabilir.
    """
    return status == PaymentStatus.PAID
