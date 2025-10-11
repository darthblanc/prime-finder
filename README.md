# Prime Finder

## How to use ✍️

#### Spawn the listener/counter process (prints the number of primes from the range specified by the initiator process)

```
python3 listener.py <name>
```

#### Spawn the worker processes (enter this command in as many terminals as you need)

```
python3 worker.py <name>
```

#### Spawn the initiator process

```
python3 main.py <start> <end>
```

#### You also need to ensure that you have redis

```
sudo apt update
sudo apt install redis-server -y
sudo systemctl enable --now redis-server
```

#### Test your redis connection. You should get "PONG" as your output

```
redis-cli ping
```

#### Install the python dependency for redis

```
pip install redis
```

#### To open the redis terminal

```
redis-cli
```
