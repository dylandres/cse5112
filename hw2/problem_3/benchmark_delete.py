#!/usr/bin/env python3
"""Benchmark delete performance for LinkedList (p3_a) vs SkipList (p3_b).

Produces:
 - hw2/problem_3/p3_delete_times.json
 - hw2/problem_3/p3_delete_times.png (linear)
 - hw2/problem_3/p3_delete_times_log.png (log y-axis)
"""
import random
import time
import statistics
import json
import matplotlib.pyplot as plt

from p3_a import LinkedList
from p3_b import SkipList

REPEATS = 5
NS = [10, 50, 100, 500, 1000, 2500, 4000, 5000]
MAX_LEVEL = 16
P = 0.5


def gen_keys(n, rng):
    return rng.sample(range(10**8), n)


def measure_delete_linkedlist(keys, rng):
    times = []
    for _ in range(REPEATS):
        ll = LinkedList()
        for k in keys:
            ll.insert(k)
        t0 = time.perf_counter()
        for k in keys:
            ll.delete(k)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def measure_delete_skiplist(keys, rng):
    times = []
    for _ in range(REPEATS):
        sl = SkipList(MAX_LEVEL, P)
        for k in keys:
            sl.insert(k)
        t0 = time.perf_counter()
        for k in keys:
            sl.delete(k)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def main():
    rng = random.Random(42)
    ns = []
    results = {'linkedlist': [], 'skiplist': []}

    for n in NS:
        print('n=', n)
        keys = gen_keys(n, rng)
        med_ll = measure_delete_linkedlist(keys, rng)
        med_sl = measure_delete_skiplist(keys, rng)
        results['linkedlist'].append(med_ll)
        results['skiplist'].append(med_sl)
        ns.append(n)
        print('medians', med_ll, med_sl)

    # with open('hw2/problem_3/p3_delete_times.json', 'w') as fh:
    #     json.dump({'ns': ns, 'linkedlist': results['linkedlist'], 'skiplist': results['skiplist']}, fh)

    plt.plot(ns, results['linkedlist'], label='LinkedList (p3_a)')
    plt.plot(ns, results['skiplist'], label='SkipList (p3_b)')
    plt.scatter(ns, results['linkedlist'], marker='o', s=30, color=plt.gca().lines[0].get_color())
    plt.scatter(ns, results['skiplist'], marker='o', s=30, color=plt.gca().lines[1].get_color())
    plt.xlabel('n')
    plt.ylabel('delete() median runtime (s)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('hw2/problem_3/p3_delete_times.png')

    plt.yscale('log')
    plt.tight_layout()
    # plt.savefig('hw2/problem_3/p3_delete_times_log.png')

    # print('Saved hw2/problem_3/p3_delete_times.{png,json}')


if __name__ == '__main__':
    main()
