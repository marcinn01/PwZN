import time
from statistics import mean, stdev
import rich
import numpy as np

rich.get_console().clear()

def decorator(func):
    timings = []

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        timings.append(execution_time)

        return 0

    def statistics():
        avg_time = mean(timings)
        min_time = min(timings)
        max_time = max(timings)
        std_dev = stdev(timings)

        return avg_time, min_time, max_time, std_dev

    wrapper.statistics = statistics
    return wrapper

@decorator
def function():
    np.random.rand(10**8)

for _ in range(6):
    function()

res = function.statistics()

print(f"Average time: {res[0]}")
print(f"Min time: {res[1]}")
print(f"Max time: {res[2]}")
print(f"Standard deviation: {res[3]}")
