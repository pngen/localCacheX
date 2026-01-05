from dataclasses import dataclass
from typing import Dict

@dataclass
class Metrics:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    errors: int = 0

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1

    def eviction(self):
        self.evictions += 1

    def error(self):
        self.errors += 1

    def to_dict(self) -> Dict[str, int]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "errors": self.errors
        }