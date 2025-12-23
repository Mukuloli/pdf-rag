import time
from typing import Any, Dict, Optional, Tuple


class SimpleCache:
    """Tiny in-memory cache with TTL, no external dependency."""

    def __init__(self, max_size: int = 128, ttl_seconds: int = 600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.store: Dict[str, Tuple[float, Any]] = {}

    def _evict_expired(self):
        now = time.time()
        keys = [k for k, (ts, _) in self.store.items() if now - ts > self.ttl]
        for k in keys:
            self.store.pop(k, None)

    def _evict_if_needed(self):
        if len(self.store) > self.max_size:
            # drop oldest entry
            oldest_key = min(self.store.items(), key=lambda kv: kv[1][0])[0]
            self.store.pop(oldest_key, None)

    def get(self, key: str) -> Optional[Any]:
        self._evict_expired()
        item = self.store.get(key)
        if not item:
            return None
        ts, value = item
        if time.time() - ts > self.ttl:
            self.store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any):
        self._evict_expired()
        self.store[key] = (time.time(), value)
        self._evict_if_needed()

