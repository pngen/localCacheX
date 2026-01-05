import unittest
from unittest.mock import Mock, patch
from local_cachex.core.cache import LocalCacheX
from local_cachex.backends.ram import RAMBackend

class TestLocalCacheX(unittest.TestCase):
    def setUp(self):
        self.backend = RAMBackend()
        self.cache = LocalCacheX(self.backend, max_memory_mb=1)

    def test_set_and_get(self):
        self.assertTrue(self.cache.set("key1", "value1"))
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_delete(self):
        self.cache.set("key1", "value1")
        self.assertTrue(self.cache.delete("key1"))
        self.assertIsNone(self.cache.get("key1"))

    def test_info(self):
        info = self.cache.info()
        self.assertIn("memory_usage_mb", info)
        self.assertIn("evictions", info)
        self.assertIn("hits", info)
        self.assertIn("misses", info)

    def test_eviction(self):
        # Set a large entry that should trigger eviction
        large_value = "x" * (1024 * 1024)  # 1MB value
        self.cache.set("large", large_value, size=1024*1024)
        
        # This should evict the large entry due to memory limit
        self.assertTrue(self.cache.set("small", "value"))
        self.assertEqual(self.cache.get("small"), "value")

if __name__ == '__main__':
    unittest.main()