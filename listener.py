import redis
import json
import sys
import datetime

r = redis.Redis()

def listener(name):
    print(f"{datetime.datetime.now()}: Listener: ({name}) started running")
    primes_metadata = {} # {id: [count, start, end]}

    while True:
        task_data = r.brpop("primes:results")[1]
        json_data = json.loads(task_data)
        id = json_data["id"]
        start = json_data["start"]
        end = json_data["end"]
        primes = json_data["known_primes"]

        if id in primes_metadata:
            primes_metadata[id][0] += len(primes)
            if start < primes_metadata[id][1]:
                primes_metadata[id][1] = start
            if end > primes_metadata[id][2]:
                primes_metadata[id][2] = end
        else:
            primes_metadata[id] = [len(primes), start, end]

        if start == end == 0:
            print(f"Task with {id}: has {primes_metadata[id][0]} primes")

if "__main__" == __name__:
    try:
        if len(sys.argv) == 2:
            listener(sys.argv[1])
        else:
            listener("Listener")
    except Exception as e:
        raise Exception(f"panic: {e}")
