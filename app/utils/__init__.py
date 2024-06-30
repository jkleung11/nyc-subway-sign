import time
from typing import List


def time_to_train(arrival_time: str, in_mins: bool = True) -> int:
    """return expected arrival time in seconds given a POSIX timestamp"""
    arrival_time = int(arrival_time)
    time_to_train = arrival_time - time.time()
    if in_mins:
        return int(time_to_train / 60)
    return time_to_train
