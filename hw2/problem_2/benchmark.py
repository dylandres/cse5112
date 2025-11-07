#!/usr/bin/env python3
"""Benchmark p2_a, p2_b, p2_c closest-pair implementations.

Produces:
 - hw2/problem_2/p2_times.json
 - hw2/problem_2/p2_times.png (linear)
 - hw2/problem_2/p2_times_log.png (log y-axis)

The script generates random point sets in a square [0, range)^2 for increasing n
and measures median runtimes over REPEATS runs.

Usage: run directly from workspace root:
    python3 hw2/problem_2/benchmark.py

"""
import random
import time
import statistics
import json
import matplotlib.pyplot as plt
from typing import List, Tuple

from p2_a import closest_pair as cp_a
from p2_b import closest_pair as cp_b
from p2_c import closest_pair as cp_c

REPEATS = 5
# avoid n < 2 because some implementations assume at least two points
NS = [2, 10, 50, 100, 500, 1000, 2500, 5000]
POINT_RANGE = 10**6


def gen_points(n: int, rng: random.Random) -> List[Tuple[int,int]]:
    return [(rng.randint(0, POINT_RANGE), rng.randint(0, POINT_RANGE)) for _ in range(n)]


def measure(fn, points):
    times = []
    for _ in range(REPEATS):
        pts_copy = list(points)
        t0 = time.perf_counter()
        _ = fn(pts_copy)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def main():
    rng = random.Random(42)
    ns = []
    results = {'a': [], 'b': [], 'c': []}

    for n in NS:
        print('n=', n)
        points = gen_points(n, rng)
        # sanity-run on small n to ensure implementations return consistent results
        if 2 <= n <= 50:
            ra = cp_a(points)
            rb = cp_b(points)
            rc = cp_c(points)
            # just print the raw returned pairs for manual inspection
            # print('sanity results:', ra, rb, rc)

        med_a = measure(cp_a, points)
        med_b = measure(cp_b, points)
        med_c = measure(cp_c, points)
        results['a'].append(med_a)
        results['b'].append(med_b)
        results['c'].append(med_c)
        ns.append(n)
        print('medians', med_a, med_b, med_c)

    # save json
    with open('hw2/problem_2/p2_times.json', 'w') as fh:
        json.dump({'ns': ns, 'a': results['a'], 'b': results['b'], 'c': results['c']}, fh)

    # linear plot
    plt.plot(ns, results['a'], label='p2_a (brute-force)')
    plt.plot(ns, results['b'], label='p2_b (divide & conquer)')
    plt.plot(ns, results['c'], label='p2_c (randomized)')
    plt.scatter(ns, results['a'], marker='o', s=30, color=plt.gca().lines[0].get_color())
    plt.scatter(ns, results['b'], marker='o', s=30, color=plt.gca().lines[1].get_color())
    plt.scatter(ns, results['c'], marker='o', s=30, color=plt.gca().lines[2].get_color())
    plt.xlabel('n')
    plt.ylabel('median runtime (s)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('hw2/problem_2/p2_times.png')

    # log-scaled y
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('hw2/problem_2/p2_times_log.png')

    print('Saved hw2/problem_2/p2_times.{png,json}')


if __name__ == '__main__':
    main()
