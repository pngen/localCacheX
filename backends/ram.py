import threading
from typing import Optional, Dict
from .base import Backend

class RAMBackend(Backend):
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._memory_usage = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            old_value = self._data.get(key)
            if old_value is not None:
                self._memory_usage -= old_value.size
            self._data[key] = value
            self._memory_usage += value.size

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                entry = self._data.pop(key)
                self._memory_usage -= entry.size
                return True
            return False

    def memory_usage(self) -> int:
        with self._lock:
            return self._memory_usage