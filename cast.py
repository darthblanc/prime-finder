import numpy as np

def as_int(*args, dtype="64"):
    try:
        match dtype:
            case "128":
                return as_int128(args)[0]
            case "64":
                return as_int64(args)[0]
            case "32":
                return as_int32(args)[0]
            case "16":
                return as_int16(args)[0]
            case "8":
                return as_int8(args)[0]
    except Exception as e:
        raise e
    
    raise RuntimeError(f"unrecognised dataype: {dtype} used")

def as_int128(*args):
    nums = np.array(args, dtype=np.int128)
    return nums

def as_int64(*args):
    nums = np.array(args, dtype=np.int64)
    return nums

def as_int32(*args):
    nums = np.array(args, dtype=np.int32)
    return nums

def as_int16(*args):
    nums = np.array(args, dtype=np.int16)
    return nums

def as_int8(*args):
    nums = np.array(args, dtype=np.int8)
    return nums
