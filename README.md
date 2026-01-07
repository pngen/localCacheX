# LocalCacheX

A production-grade, lock-free, deterministic in-memory cache engine inspired by Redis.

## Overview

LocalCacheX is a high-performance, embeddable key-value store designed for local-first applications. It provides deterministic LRU eviction, pluggable backends (RAM and optional GPU), and a RESP-compatible server interface.

## Architecture Diagram

<pre>
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│   CLI       │    │  Server      │    │  Cache Core   │
│             │    │              │    │               │
│  start      │───▶│  RESP        │───▶│  RAM/GPU      │
│  bench      │    │  TCP         │    │  Backend      │
│  snapshot   │    │  Protocol    │    │               │
│  restore    │    │              │    │  LRU Eviction │
│  stats      │    │              │    │               │
└─────────────┘    └──────────────┘    └───────────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │   Metrics    │
                                        │              │
                                        │  Hits/Misses │
                                        │  Evictions   │
                                        └──────────────┘
</pre>

## Core Components

1. **Storage Backends**
   - RAMBackend: Lock-free shared memory storage
   - GPUBackend: GPU tensor storage with CPU key table

2. **Eviction Policy**
   - Deterministic LRU with lexicographical tie-breaking
   - Fully auditable eviction decisions

3. **Server Mode**
   - RESP-compatible TCP server
   - Commands: SET, GET, DEL, INFO, PING

4. **Metrics**
   - Hit/miss rates
   - Eviction counts
   - Memory usage tracking

5. **CLI Interface**
   - `cachex start` - Start server
   - `cachex bench` - Run benchmarks
   - `cachex snapshot` - Take snapshots
   - `cachex restore` - Restore from snapshot
   - `cachex stats` - Show statistics

## Usage

Start the server:

```bash
python -m local_cachex.cli.main start
Connect with redis-cli:

redis-cli -p 6379
```

## Design Principles
- Deterministic: Predictable behavior under all conditions
- Low Latency: Optimized for fast access patterns
- Contention Safe: Lock-free structures where possible
- Minimal Dependencies: Only core Python + optional GPU libraries
- Isolation: Clear separation between modules
- Auditable: All decisions logged and traceable

## Requirements
- Python 3.8+
- Optional: CuPy for GPU support (`pip install cupy-cuda11x`)

## License

MIT License

## Author

Paul Ngen
