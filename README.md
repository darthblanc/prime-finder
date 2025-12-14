# Prime Finder

A mathematics tool that counts the number of primes within a range. The tool uses multi-threading, multi-processing, and Redis streams to distribute workloads across several worker processes leading to faster compute times.

## Features

- **Multi-threading**: Concurrent execution for improved performance
- **Multi-processing**: Distributes workload across multiple processes
- **Redis Streams**: Uses Redis for inter-process communication and task distribution
- **Distributed Computing**: Spawn multiple worker processes for parallel computation

## Prerequisites

- Python 3
- Redis server
- Redis Python library

## Installation

### Install Redis Server

```bash
sudo apt update
sudo apt install redis-server -y
sudo systemctl enable --now redis-server
```

### Test Redis Connection

You should get "PONG" as output:

```bash
redis-cli ping
```

### Install Python Dependencies

```bash
pip install redis
```

## How to Use

### 1. Spawn the Listener/Counter Process

The listener process prints the number of primes from the range specified by the initiator process:

```bash
python3 listener.py <n>
```

### 2. Spawn Worker Processes

Enter this command in as many terminals as you need for parallel processing:

```bash
python3 worker.py <n>
```

### 3. Spawn the Initiator Process

```bash
python3 main.py <start> <end>
```

Where `<start>` and `<end>` define the range to search for prime numbers.

## Repository Structure

```
prime-finder/
├── main.py          # Initiator process - defines the range
├── listener.py      # Listener/counter process - aggregates results
├── worker.py        # Worker process - performs prime calculations
├── prime.py         # Prime number calculation logic
├── cast.py          # Type casting utilities
├── filter.py        # Filtering operations
├── jsonify.py       # JSON serialization utilities
├── .gitignore       # Git ignore file
└── README.md        # This file
```

## Redis CLI

To open the Redis terminal:

```bash
redis-cli
```

## Topics

- Python
- Redis
- JSON
- Multiprocessing
- NumPy
- Mathematics
- Multithreading
- Primes

## How It Works

1. **Initiator** (`main.py`): Defines the range and distributes tasks
2. **Workers** (`worker.py`): Multiple worker processes compute prime numbers in parallel
3. **Listener** (`listener.py`): Aggregates results from workers and outputs the final count
4. **Redis**: Manages communication between processes using streams

This distributed architecture allows for efficient computation of prime numbers across large ranges by leveraging multiple CPU cores and processes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Efficiently finding primes through distributed computing! 🔢⚡**
