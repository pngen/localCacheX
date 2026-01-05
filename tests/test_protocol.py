import unittest
from local_cachex.server.protocol import RESPProtocol
from local_cachex.core.cache import LocalCacheX
from local_cachex.backends.ram import RAMBackend

class TestRESPProtocol(unittest.TestCase):
    def setUp(self):
        backend = RAMBackend()
        cache = LocalCacheX(backend)
        self.protocol = RESPProtocol(cache)

    def test_parse_command(self):
        data = b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"
        result = self.protocol.parse_command(data)
        self.assertEqual(result, ("GET", ["key"]))

    def test_handle_get_command(self):
        response = self.protocol.handle_command(("GET", ["nonexistent"]))
        self.assertEqual(response, b"$-1\r\n")

    def test_handle_set_command(self):
        response = self.protocol.handle_command(("SET", ["key", "value"]))
        self.assertEqual(response, b"+OK\r\n")

    def test_process_request(self):
        data = b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"
        response = self.protocol.process_request(data)
        self.assertEqual(response, b"$-1\r\n")

if __name__ == '__main__':
    unittest.main()