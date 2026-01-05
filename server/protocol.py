import socket
from typing import Tuple, Optional
from ..core.cache import LocalCacheX

class RESPProtocol:
    def __init__(self, cache: LocalCacheX):
        self.cache = cache

    def parse_command(self, data: bytes) -> Optional[Tuple[str, list]]:
        lines = data.decode().strip().split('\r\n')
        if not lines or lines[0] != '*':
            return None
        
        try:
            count = int(lines[1])
            if count < 1:
                return None
            cmd = lines[2].upper()
            args = [line for line in lines[3:3+count]]
            return (cmd, args)
        except Exception:
            return None

    def handle_command(self, command: Tuple[str, list]) -> bytes:
        cmd, args = command
        try:
            if cmd == 'GET':
                key = args[0] if args else ''
                value = self.cache.get(key)
                if value is not None:
                    return f"+{value}\r\n".encode()
                else:
                    return "$-1\r\n".encode()  # nil reply
            elif cmd == 'SET':
                key = args[0] if args else ''
                value = args[1] if len(args) > 1 else ''
                self.cache.set(key, value)
                return "+OK\r\n".encode()
            elif cmd == 'DEL':
                key = args[0] if args else ''
                deleted = self.cache.delete(key)
                return f":{1 if deleted else 0}\r\n".encode()
            elif cmd == 'INFO':
                info = self.cache.info()
                response = "\r\n".join([f"{k}:{v}" for k, v in info.items()]) + "\r\n"
                return response.encode()
            elif cmd == 'PING':
                return "+PONG\r\n".encode()
            else:
                return f"-ERR unknown command '{cmd}'\r\n".encode()
        except Exception as e:
            return f"-ERR {str(e)}\r\n".encode()

    def process_request(self, data: bytes) -> bytes:
        cmd = self.parse_command(data)
        if cmd is None:
            return b"-ERR invalid RESP command\r\n"
        return self.handle_command(cmd)