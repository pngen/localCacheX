import argparse
import sys
from ..core.cache import LocalCacheX
from ..backends.ram import RAMBackend
from ..server.tcp_server import TCPServer

def start_server(args):
    backend = RAMBackend()
    cache = LocalCacheX(backend)
    server = TCPServer(cache, args.host, args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped.")

def main():
    parser = argparse.ArgumentParser(description='LocalCacheX CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Start command
    start_parser = subparsers.add_parser('start', help='Start the cache server')
    start_parser.add_argument('--host', default='localhost', help='Host to bind to')
    start_parser.add_argument('--port', type=int, default=6379, help='Port to listen on')

    # Benchmark command
    bench_parser = subparsers.add_parser('bench', help='Run benchmarks')
    bench_parser.add_argument('--duration', type=int, default=10, help='Benchmark duration in seconds')

    # Snapshot command
    snap_parser = subparsers.add_parser('snapshot', help='Take a snapshot')
    snap_parser.add_argument('--file', required=True, help='Snapshot file path')

    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from snapshot')
    restore_parser.add_argument('--file', required=True, help='Snapshot file path')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show cache statistics')

    args = parser.parse_args()

    if args.command == 'start':
        start_server(args)
    elif args.command == 'bench':
        print("Benchmarking not implemented yet")
    elif args.command == 'snapshot':
        print("Snapshot not implemented yet")
    elif args.command == 'restore':
        print("Restore not implemented yet")
    elif args.command == 'stats':
        print("Stats not implemented yet")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()