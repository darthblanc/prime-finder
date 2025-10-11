import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty

def divide_range(start: int, end: int, depth: int, q: Queue, ranges: Queue):
    if start > end:
        return
    if depth == 0:
        ranges.put((start, end))
        return
    
    mid = (start + end) //2

    q.put((start, mid, depth - 1))
    q.put((mid + 1, end, depth - 1))

def get_ranges(start: int, end: int):
    q = Queue()
    ranges = Queue()

    q.put( (start, end, int( np.floor( np.log10( end - start ) ) ) ) )

    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        while not q.empty():
            start, end, depth = q.get()
            future = executor.submit(divide_range, start, end, depth, q, ranges)
            futures.append(future)
        
        while True:
            try:
                result = ranges.get(timeout=1)
                yield result
            except Empty:
                if q.empty():
                    break
