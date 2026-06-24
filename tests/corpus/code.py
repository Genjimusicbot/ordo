"""A small in-memory task queue with retry and priority. Generic sample for token-saving verification."""
from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field


@dataclass(order=True)
class Task:
    priority: int
    created_at: float = field(compare=False)
    name: str = field(compare=False)
    payload: dict = field(default_factory=dict, compare=False)
    attempts: int = field(default=0, compare=False)


class TaskQueue:
    def __init__(self, max_attempts: int = 3):
        self._heap: list[Task] = []
        self.max_attempts = max_attempts
        self.failed: list[Task] = []

    def push(self, name: str, payload: dict | None = None, priority: int = 0) -> None:
        if not name:
            raise ValueError("task name must not be empty")
        task = Task(priority=priority, created_at=time.time(), name=name, payload=payload or {})
        heapq.heappush(self._heap, task)

    def pop(self) -> Task | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def run(self, handler) -> dict:
        results = {"ok": 0, "failed": 0}
        while self._heap:
            task = self.pop()
            if task is None:
                break
            try:
                handler(task)
                results["ok"] += 1
            except Exception as exc:  # noqa: BLE001
                task.attempts += 1
                if task.attempts < self.max_attempts:
                    heapq.heappush(self._heap, task)
                else:
                    self.failed.append(task)
                    results["failed"] += 1
                    print(f"task {task.name} failed after {task.attempts} attempts: {exc}")
        return results

    def __len__(self) -> int:
        return len(self._heap)


def _demo():
    q = TaskQueue(max_attempts=2)
    for i in range(5):
        q.push(name=f"job-{i}", payload={"i": i}, priority=i % 2)

    seen = []

    def handler(task: Task) -> None:
        if task.name == "job-3" and task.attempts == 0:
            raise RuntimeError("transient error")
        seen.append(task.name)

    result = q.run(handler)
    assert result["ok"] == 5, result
    assert len(q) == 0
    print("demo ok:", result, "order:", seen)


if __name__ == "__main__":
    _demo()
