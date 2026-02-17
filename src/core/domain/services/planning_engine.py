# PATH: src/core/domain/services/planning_engine.py
# DESC: Mission takvimi optimizasyonu (KR-015).

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, timedelta


class PlanningEngineError(Exception):
    """Planlama motoru domain invariant ihlali."""


@dataclass(frozen=True)
class PilotSlot:
    """Pilot müsaitlik slotu."""

    pilot_id: uuid.UUID
    date: date
    province_code: str
    remaining_capacity: int
    daily_capacity: int


@dataclass(frozen=True)
class MissionDemand:
    """Planlanması gereken mission talebi."""

    demand_id: uuid.UUID
    field_id: uuid.UUID
    province_code: str
    crop_type: str
    area_m2: float
    priority: int  # Düşük = yüksek öncelik (0 en yüksek)
    earliest_date: date
    latest_date: date
    estimated_duration_minutes: int


@dataclass(frozen=True)
class ScheduledSlot:
    """Planlanmış mission slotu."""

    demand_id: uuid.UUID
    field_id: uuid.UUID
    pilot_id: uuid.UUID
    scheduled_date: date
    estimated_duration_minutes: int


@dataclass(frozen=True)
class ScheduleResult:
    """Optimizasyon sonucu."""

    scheduled: tuple[ScheduledSlot, ...]
    unscheduled: tuple[uuid.UUID, ...]  # Planlanamayan demand_id'ler
    pilot_utilization: dict[uuid.UUID, float]  # pilot_id -> kullanım oranı
    warnings: tuple[str, ...]


class PlanningEngine:
    """Mission takvimi optimizasyonu servisi (KR-015).

    Tek entity'ye sığmayan saf iş mantığı; policy ve hesaplamalar.

    Domain invariants:
    - Her pilot günlük kapasitesini aşamaz.
    - Mission tarihi talep edilen pencere içinde olmalıdır.
    - Pilot bölge yetkisi tarla bölgesi ile eşleşmelidir.
    - Yüksek öncelikli talepler önce planlanır.
    """

    def optimize_schedule(
        self,
        demands: list[MissionDemand],
        pilot_slots: list[PilotSlot],
    ) -> ScheduleResult:
        """Mission taleplerini pilot slotlarına optimize ederek yerleştirir.

        Greedy yaklaşım: önceliğe göre sıralı talepleri, bölge eşleşen
        ve en az yüklü pilotlara atar.

        Args:
            demands: Planlanması gereken mission talepleri.
            pilot_slots: Pilot müsaitlik slotları.

        Returns:
            ScheduleResult: Optimizasyon sonucu.
        """
        if not demands:
            return ScheduleResult(
                scheduled=(),
                unscheduled=(),
                pilot_utilization={},
                warnings=(),
            )

        # Önceliğe göre sırala
        sorted_demands = sorted(demands, key=lambda d: d.priority)

        # Pilot slot'ları index: (pilot_id, date) -> kalan kapasite
        slot_capacity: dict[tuple[uuid.UUID, date], int] = {}
        slot_province: dict[tuple[uuid.UUID, date], str] = {}
        pilot_daily_cap: dict[uuid.UUID, int] = {}

        for slot in pilot_slots:
            key = (slot.pilot_id, slot.date)
            slot_capacity[key] = slot.remaining_capacity
            slot_province[key] = slot.province_code
            pilot_daily_cap[slot.pilot_id] = slot.daily_capacity

        scheduled: list[ScheduledSlot] = []
        unscheduled: list[uuid.UUID] = []
        warnings: list[str] = []

        # Pilot bazında atama sayısı (kullanım hesabı için)
        pilot_assigned: dict[uuid.UUID, int] = {}
        pilot_total_slots: dict[uuid.UUID, int] = {}

        # Pilot toplam slot sayısını hesapla
        for slot in pilot_slots:
            pid = slot.pilot_id
            pilot_total_slots[pid] = pilot_total_slots.get(pid, 0) + slot.daily_capacity

        for demand in sorted_demands:
            assigned = False

            # Tarih penceresi içindeki slotları bul
            candidate_slots = [
                (pid, d)
                for (pid, d), cap in slot_capacity.items()
                if cap > 0
                and demand.earliest_date <= d <= demand.latest_date
                and slot_province.get((pid, d)) == demand.province_code
            ]

            # En az yüklü pilotu tercih et (tarihe göre de erken olanı)
            candidate_slots.sort(
                key=lambda s: (
                    pilot_assigned.get(s[0], 0),
                    s[1],
                )
            )

            for pilot_id, sched_date in candidate_slots:
                key = (pilot_id, sched_date)
                if slot_capacity.get(key, 0) > 0:
                    scheduled.append(
                        ScheduledSlot(
                            demand_id=demand.demand_id,
                            field_id=demand.field_id,
                            pilot_id=pilot_id,
                            scheduled_date=sched_date,
                            estimated_duration_minutes=demand.estimated_duration_minutes,
                        )
                    )
                    slot_capacity[key] -= 1
                    pilot_assigned[pilot_id] = pilot_assigned.get(pilot_id, 0) + 1
                    assigned = True
                    break

            if not assigned:
                unscheduled.append(demand.demand_id)
                warnings.append(
                    f"Talep {demand.demand_id}: uygun pilot/tarih bulunamadı "
                    f"(bölge: {demand.province_code}, "
                    f"pencere: {demand.earliest_date} - {demand.latest_date})."
                )

        # Kullanım oranı hesapla
        utilization: dict[uuid.UUID, float] = {}
        for pid, total in pilot_total_slots.items():
            if total > 0:
                utilization[pid] = pilot_assigned.get(pid, 0) / total

        return ScheduleResult(
            scheduled=tuple(scheduled),
            unscheduled=tuple(unscheduled),
            pilot_utilization=utilization,
            warnings=tuple(warnings),
        )

    @staticmethod
    def generate_date_range(start: date, end: date) -> list[date]:
        """Tarih aralığı üretir (dahil-dahil).

        Args:
            start: Başlangıç tarihi.
            end: Bitiş tarihi.

        Returns:
            Tarih listesi.
        """
        if start > end:
            raise PlanningEngineError("start, end'den sonra olamaz.")

        dates: list[date] = []
        current = start
        while current <= end:
            dates.append(current)
            current += timedelta(days=1)
        return dates
