import redis
import json
from prime import get_primes
import sys
import datetime
from jsonify import jsonify_worker_results

r = redis.Redis()

def worker(name):
    print(f"{datetime.datetime.now()}: Worker: ({name}) started running")
    known_primes = {}

    pubsub = r.pubsub()
    pubsub.subscribe("init")

    for msg in pubsub.listen():
        if msg["type"] == "message":
            known_primes = json.loads(msg["data"].decode())["known_primes"]
            break

    while True:
        task_data = r.brpop("primes:tasks")[1]
        json_data = json.loads(task_data)
        id = json_data["id"]
        start = json_data["start"]
        end = json_data["end"]

        primes = get_primes(start, end, known_primes)

        print(f"{datetime.datetime.now()}: ({name}) just processed: [{start}, {end}] -> Found {len(primes)} primes")

        r.lpush("primes:results", jsonify_worker_results(id, start, end, primes))

if "__main__" == __name__:
    try:
        worker(sys.argv[1])
    except Exception as e:
        raise Exception(f"panic: {e}")
