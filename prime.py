import numpy as np

def get_essential_primes(b):
    primes = set()
    non_primes = set()

    for i in range(2, int(np.sqrt(b))+1):
        if i in non_primes:
            continue
        primes.add(i)
        for j in range(i**2, int(np.sqrt(b))+1, i):
            non_primes.add(j)
            
    return primes


def get_primes(a, b, known_primes):
    if a < 2:
        a = 2

    primes = set(np.arange(a, b, 1))
    non_primes = set()

    for prime in known_primes:
        for i in range(prime**2, b, prime):
            if i in non_primes:
                continue
            non_primes.add(i)
            if i in primes:
                primes.remove(i)
            
    return primes
