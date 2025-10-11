import sys
from filter import filter
import redis
from jsonify import jsonify
import datetime

if "__main__" == __name__:
    r = redis.Redis()

    if len(sys.argv) < 2:
        raise RuntimeError("not enough arguments")
    elif len(sys.argv) > 3:
        raise RuntimeError("too many arguments")
    else:
        ranges = []
        if len(sys.argv) == 2:
                essential_primes, ranges = filter(sys.argv[1])
        elif len(sys.argv) == 3:
                essential_primes, ranges = filter(sys.argv[1], sys.argv[2])

        task_id = datetime.datetime.now()

        for a, b in ranges:
            r.lpush("primes:tasks", jsonify(task_id, a, b, essential_primes))
            print(f"sending {(a, b)}")

    r.close()
