import redis
import json
import sys
import datetime
from collections import defaultdict

r = redis.Redis()

def listener(name):
    print(f"{datetime.datetime.now()}: Listener: ({name}) started running")
    prime_counts = defaultdict(int)

    while True:
        task_data = r.brpop("primes:results")[1]
        json_data = json.loads(task_data)
        id = json_data["id"]
        start = json_data["start"]
        end = json_data["end"]
        primes = json_data["known_primes"]

        prime_counts[id] += len(primes)

        print(f"{datetime.datetime.now()}: ({name}) just processed: [{start}, {end}] with id: {id}: Counted {prime_counts[id]} primes")

if "__main__" == __name__:
    try:
        listener(sys.argv[1])
    except Exception as e:
        raise Exception(f"panic: {e}")
