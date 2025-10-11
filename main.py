import sys
from filter import get_ranges
import redis
from jsonify import jsonify, jsonify_essential_primes
import datetime
from prime import get_essential_primes
from cast import as_int
import numpy as np

if "__main__" == __name__:
    r = redis.Redis()

    if len(sys.argv) < 2:
        raise RuntimeError("not enough arguments")
    elif len(sys.argv) > 3:
        raise RuntimeError("too many arguments")
    else:
        if len(sys.argv) == 2:
            start, end = np.append([2], as_int(sys.argv[1]))
        if len(sys.argv) == 3:
            start, end = as_int(sys.argv[1], sys.argv[2])
        
        if start >= end:
            raise RuntimeError("there are no primes within the range selected")

        task_id = datetime.datetime.now()

        essential_primes = get_essential_primes(end)
        essential_primes_json = jsonify_essential_primes(essential_primes)

        r.publish("init", essential_primes_json)

        print(essential_primes_json)
        for a, b in get_ranges(start, end):
            r.lpush("primes:tasks", jsonify(task_id, a, b))
            print(f"sending {(a, b)}")

    r.close()
