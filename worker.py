import redis
import json
from prime import get_primes
import sys
import datetime
from jsonify import jsonify

r = redis.Redis()

def worker(name):
    print(f"{datetime.datetime.now()}: Worker: ({name}) started running")
    memory = {}

    while True:
        task_data = r.brpop("primes:tasks")[1]
        json_data = json.loads(task_data)
        id = json_data["id"]
        start = json_data["start"]
        end = json_data["end"]
        known_primes = json_data["known_primes"]

        primes = get_primes(start, end, known_primes)

        print(f"{datetime.datetime.now()}: ({name}) just processed: [{start}, {end}] -> Found {len(primes)} primes")

        r.lpush("primes:results", jsonify(id, start, end, primes))

if "__main__" == __name__:
    try:
        worker(sys.argv[1])
    except Exception as e:
        raise Exception(f"panic: {e}")
