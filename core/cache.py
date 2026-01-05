import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Dict, Tuple
from dataclasses import dataclass
from .metrics import Metrics

@dataclass
class CacheEntry:
    value: Any
    size: int
    timestamp: float

class LocalCacheX:
    def __init__(self, backend, max_memory_mb: int = 100):
        self.backend = backend
        self.max_memory_mb = max_memory_mb
        self.metrics = Metrics()
        self._lock = threading.RLock()
        self._access_order = OrderedDict()  # For LRU tracking

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            try:
                entry = self.backend.get(key)
                if entry is not None:
                    self.metrics.hit()
                    self._update_access_order(key)
                    return entry.value
                else:
                    self.metrics.miss()
                    return None
            except Exception as e:
                self.metrics.error()
                raise

    def set(self, key: str, value: Any, size: int = 0) -> bool:
        with self._lock:
            try:
                # Evict if needed before setting
                self._evict_if_needed(size)
                
                entry = CacheEntry(value=value, size=size or len(str(value)), timestamp=time.time())
                self.backend.set(key, entry)
                self._update_access_order(key)
                return True
            except Exception as e:
                self.metrics.error()
                raise

    def delete(self, key: str) -> bool:
        with self._lock:
            try:
                result = self.backend.delete(key)
                if result:
                    self._access_order.pop(key, None)
                return result
            except Exception as e:
                self.metrics.error()
                raise

    def info(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "memory_usage_mb": self.backend.memory_usage(),
                "evictions": self.metrics.evictions,
                "hits": self.metrics.hits,
                "misses": self.metrics.misses,
                "errors": self.metrics.errors
            }

    def _update_access_order(self, key: str):
        if key in self._access_order:
            self._access_order.move_to_end(key)
        else:
            self._access_order[key] = None

    def _evict_if_needed(self, new_entry_size: int):
        current_memory = self.backend.memory_usage()
        if current_memory + new_entry_size > self.max_memory_mb * 1024 * 1024:
            # Evict LRU entries until space is available
            while current_memory + new_entry_size > self.max_memory_mb * 1024 * 1024:
                if not self._access_order:
                    break
                lru_key = next(iter(self._access_order))
                entry = self.backend.get(lru_key)
                if entry is not None:
                    self.backend.delete(lru_key)
                    self.metrics.eviction()
                    current_memory -= entry.size
                else:
                    # Entry was deleted by another thread, remove from access order
                    del self._access_order[lru_key]