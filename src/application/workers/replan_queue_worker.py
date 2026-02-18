# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Queue worker retries replan tasks with ack/nack semantics.

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ReplanTask:
    task_id: str
    mission_id: str
    reason: str
    correlation_id: str


class QueueClient(Protocol):
    def pop(self, queue_name: str) -> ReplanTask | None: ...

    def ack(self, queue_name: str, task_id: str) -> None: ...

    def nack(self, queue_name: str, task_id: str, *, requeue: bool) -> None: ...


class MissionReplanner(Protocol):
    def replan(self, *, mission_id: str, reason: str, correlation_id: str) -> None: ...


class ReplanQueueWorker:
    def __init__(self, *, queue: QueueClient, replanner: MissionReplanner, queue_name: str = "replan") -> None:
        self._queue = queue
        self._replanner = replanner
        self._queue_name = queue_name

    def run_once(self) -> bool:
        task = self._queue.pop(self._queue_name)
        if task is None:
            return False
        try:
            self._replanner.replan(mission_id=task.mission_id, reason=task.reason, correlation_id=task.correlation_id)
            self._queue.ack(self._queue_name, task.task_id)
            return True
        except Exception:
            self._queue.nack(self._queue_name, task.task_id, requeue=True)
            return True

    def run_forever(self, *, poll_interval_s: float = 1.0) -> None:
        while True:
            if not self.run_once():
                time.sleep(float(poll_interval_s))
