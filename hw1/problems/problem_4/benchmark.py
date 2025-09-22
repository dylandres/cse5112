import random
import unittest
import time
import statistics
import matplotlib.pyplot as plt
from collections import Counter
import tracemalloc

from p4_b import most_frequent_difference_b
from p4_c import most_frequent_difference_c

def expected_frequency(values, d_mode: int) -> int:
    """
    Compute expected frequency in O(n) using same logic,
    just a direct reference implementation.
    """
    cnt = Counter(values)
    if d_mode == 0:
        return sum(c * (c - 1) for c in cnt.values())
    return sum(c * cnt.get(x + d_mode, 0) for x, c in cnt.items())

def generate_input_and_dmode(n: int, value_range=(1, 1000)):
    """
    Generate an input list and a valid d_mode chosen from actual differences.
    """
    values = [random.randint(*value_range) for _ in range(n)]

    # pick two distinct positions to define a valid delta
    i, j = random.sample(range(n), 2)
    d_mode = values[i] - values[j]

    times_b = []
    times_c = []
    space_b = []
    space_c = []
    # compute frequency for this d_mode
    for _ in range(10):
        t0 = time.perf_counter()
        tracemalloc.start()
        b_freq = most_frequent_difference_b(values, d_mode)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage: {current :.2f} B")
        print(f"Peak memory usage: {peak :.2f} B")
        tracemalloc.stop()
        delta = time.perf_counter() - t0
        times_b.append(delta)
        space_b.append(peak)
        t0 = time.perf_counter()
        tracemalloc.start()
        c_freq = most_frequent_difference_c(values, d_mode)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage: {current :.2f} B")
        print(f"Peak memory usage: {peak :.2f} B")
        tracemalloc.stop()
        delta = time.perf_counter() - t0
        times_c.append(delta)
        space_c.append(peak)
    bmed = statistics.median(times_b)
    cmed = statistics.median(times_c)
    bmeds = statistics.median(space_b)
    cmeds = statistics.median(space_c)
    print(bmed, cmed)
    return values, d_mode, b_freq, c_freq, bmed, cmed, bmeds, cmeds


# Example: direct usage
if __name__ == "__main__":
    ns = []
    results_b = []
    results_c = []

    for n in [10, 50, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]:
        values, d_mode, b_freq, c_freq, bmed, cmed, bmeds, cmeds = generate_input_and_dmode(n, (1, 10))
        results_b.append(bmeds)
        results_c.append(cmeds)
        ns.append(n)

        # print(f"Generated {len(values)} input:", values)
        print("Generated d_mode:", d_mode)
        print("Expected frequency:", expected_frequency(values, d_mode))
        print("Calculated b frequency:", b_freq)
        print("Calculated c frequency:", c_freq)

    plt.plot(ns, results_b, label='most_frequent_difference_b')
    plt.plot(ns, results_c, label='most_frequent_difference_c')
    # draw markers at the actual n values
    plt.scatter(ns, results_b, marker='o', s=30, color=plt.gca().lines[0].get_color())
    plt.scatter(ns, results_c, marker='o', s=30, color=plt.gca().lines[1].get_color())
    plt.xlabel('n')
    plt.ylabel('median peak memory usage (bytes)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('problem_4/p4_space.png')
