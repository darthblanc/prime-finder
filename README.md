# Prime Finder

A distributed prime-counting system built on a **producer-worker-aggregator architecture**, using Redis Streams for inter-process communication and Python multiprocessing + multithreading for parallel computation.

Built to explore the performance ceiling of CPU-bound workloads distributed across independent processes — the same architectural pattern underlying large-scale data pipelines.

---

## Architecture

The system is split into three independently-spawned process types that communicate exclusively through Redis Streams:

```
main.py (Initiator)
    │
    │  Pushes range partitions → Redis Stream
    │
    ▼
worker.py × N (Workers)
    │
    │  Consume partitions, compute primes → Redis Stream
    │
    ▼
listener.py (Aggregator)
    │
    └─ Collects results, outputs final prime count
```

**Why this matters:** Each layer is fully decoupled. You can spawn as many worker processes as you have CPU cores — or run workers on separate machines — without changing any code. Redis acts as the message bus, handling backpressure and delivery guarantees between processes.

### How Work Is Distributed

1. **Initiator** (`main.py`) partitions the input range `[start, end]` into chunks and publishes them to a Redis Stream
2. **Workers** (`worker.py`) each consume chunks from the stream independently, computing primes within their partition using multithreaded execution
3. **Aggregator** (`listener.py`) collects results from all workers and outputs the final count

Adding more workers linearly increases throughput — no code changes required.

---

## Performance

The distributed design trades single-process simplicity for horizontal scalability. For large ranges, spawning N workers reduces wall-clock time approximately proportionally to N (up to the limit of available cores and Redis throughput).

```bash
# Example: search primes from 1 to 10,000,000 with 4 workers
python3 listener.py 4 &
python3 worker.py 4 & python3 worker.py 4 & python3 worker.py 4 & python3 worker.py 4 &
python3 main.py 1 10000000
```

---

## Quick Start

### Prerequisites

- Python 3
- Redis server

### Install Redis

```bash
sudo apt update
sudo apt install redis-server -y
sudo systemctl enable --now redis-server
redis-cli ping  # should return PONG
```

### Install Python Dependencies

```bash
pip install redis numpy
```

### Run

Open three terminal windows:

**Terminal 1 — Start the aggregator:**
```bash
python3 listener.py <n>
```

**Terminal 2+ — Start one or more workers:**
```bash
python3 worker.py <n>
```

**Terminal 3 — Start the initiator:**
```bash
python3 main.py <start> <end>
```

Where `<n>` is the number of worker processes and `<start>`/`<end>` define the search range.

---

## Project Structure

```
prime-finder/
├── main.py        # Initiator — partitions range, publishes to Redis Stream
├── worker.py      # Worker — consumes partitions, computes primes (multithreaded)
├── listener.py    # Aggregator — collects results, outputs final count
├── prime.py       # Prime calculation logic
├── filter.py      # Filtering operations
├── jsonify.py     # JSON serialization for Redis messages
└── cast.py        # Type casting utilities
```

---

## Design Decisions

**Why Redis Streams (not queues or pub/sub)?** Streams give consumer groups with at-least-once delivery semantics — if a worker crashes mid-computation, the partition gets redelivered to another worker. A simple queue would lose that work.

**Why separate processes instead of threads?** Python's GIL limits true parallelism for CPU-bound work within a single process. Spawning independent worker processes sidesteps the GIL entirely, giving real multi-core utilization.

**Why multithreading inside each worker?** I/O operations (Redis reads/writes) don't hold the GIL, so threading within each worker improves throughput on the communication layer while multiprocessing handles the CPU-bound prime computation.

---

## Topics

`distributed-systems` · `redis-streams` · `multiprocessing` · `multithreading` · `python` · `mathematics` · `inter-process-communication`
