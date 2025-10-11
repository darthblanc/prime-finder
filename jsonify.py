import json

def jsonify(id, start, end, known_primes):
    return json.dumps(
        {
            "id": str(id),
            "start": int(start),
            "end": int(end),
            "known_primes": [int(x) for x in known_primes]
        }
    )
