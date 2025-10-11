import json

def jsonify(id, start, end):
    return json.dumps(
        {
            "id": str(id),
            "start": int(start),
            "end": int(end),
        }
    )

def jsonify_essential_primes(essential_primes):
    return json.dumps(
        {
            "known_primes": list(map(int, essential_primes))
        }
    )

def jsonify_worker_results(id, start, end, primes):
    return json.dumps(
        {
            "id": str(id),
            "start": int(start),
            "end": int(end),
            "known_primes": list(map(int, primes))
        }
    )