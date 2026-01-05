import threading
from typing import Optional, Dict, Any
from .base import Backend

class GPUBackend(Backend):
    def __init__(self):
        try:
            import cupy as cp
            self._cp = cp
        except ImportError:
            raise RuntimeError("CuPy not installed. Install with: pip install cupy-cuda11x")
        
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._memory_usage = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._data.get(key)
            if entry is not None:
                # Transfer from GPU to CPU for access
                return self._cp.asnumpy(entry.value)
            return None

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            old_value = self._data.get(key)
            if old_value is not None:
                self._memory_usage -= old_value.size
            # Move to GPU memory
            gpu_tensor = self._cp.asarray(value.value)
            value.value = gpu_tensor
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