import unittest
from local_cachex.backends.ram import RAMBackend
from local_cachex.backends.gpu import GPUBackend

class TestRAMBackend(unittest.TestCase):
    def setUp(self):
        self.backend = RAMBackend()

    def test_get_set_delete(self):
        self.assertIsNone(self.backend.get("key1"))
        self.backend.set("key1", "value1")
        self.assertEqual(self.backend.get("key1"), "value1")
        self.assertTrue(self.backend.delete("key1"))
        self.assertIsNone(self.backend.get("key1"))

    def test_memory_usage(self):
        self.assertEqual(self.backend.memory_usage(), 0)
        self.backend.set("key1", "value1")
        self.assertGreater(self.backend.memory_usage(), 0)

class TestGPUBackend(unittest.TestCase):
    def setUp(self):
        try:
            self.backend = GPUBackend()
        except RuntimeError:
            self.skipTest("CuPy not available")

    def test_get_set_delete(self):
        self.assertIsNone(self.backend.get("key1"))
        self.backend.set("key1", "value1")
        self.assertEqual(self.backend.get("key1"), "value1")
        self.assertTrue(self.backend.delete("key1"))
        self.assertIsNone(self.backend.get("key1"))

if __name__ == '__main__':
    unittest.main()