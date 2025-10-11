import numpy as np
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
from prime import get_essential_primes

def cast_arguments(*args):
    try:
        nums = np.array(args, dtype=np.int64)[0]
    except:
        raise RuntimeError("non-integer detected in arguments")

    return nums

def divide_range(start: int, end: int, depth: int, q: Queue, ranges: list):
    if start > end:
        return
    if depth == 0:
        ranges.append((start, end))
        return
    
    mid = (start + end) //2

    q.put((start, mid, depth - 1))
    q.put((mid + 1, end, depth - 1))

def get_ranges(q: Queue, ranges: list):
    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        while not q.empty():
            start, end, depth = q.get()
            future = executor.submit(divide_range, start, end, depth, q, ranges)
            futures.append(future)
        
        wait(future)

def filter(*args):
    nums = cast_arguments(args)

    if len(nums) == 1:
        nums = np.append([0], nums)

    q = Queue()
    q.put((nums[0], nums[1], int(np.floor(np.log10(nums[1] - nums[0])))) )
    ranges = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_essential_primes = executor.submit(get_essential_primes, nums[1])
        executor.submit(get_ranges, q, ranges)

        wait([future_essential_primes])

    print("pre-processing successful")
    return future_essential_primes.result(), ranges
