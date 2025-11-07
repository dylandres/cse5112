#!/usr/bin/env python3
"""Benchmark insert performance for LinkedList (p3_a) vs SkipList (p3_b).

Produces:
 - hw2/problem_3/p3_times.json
 - hw2/problem_3/p3_times.png (linear)
 - hw2/problem_3/p3_times_log.png (log y-axis)

Usage: run from workspace root:
    python3 hw2/problem_3/benchmark.py
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
    # generate n unique integers
    return rng.sample(range(10**8), n)


def measure_insert_linkedlist(keys):
    times = []
    for _ in range(REPEATS):
        ll = LinkedList()
        t0 = time.perf_counter()
        for k in keys:
            ll.insert(k)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def measure_insert_skiplist(keys, rng):
    times = []
    for _ in range(REPEATS):
        sl = SkipList(MAX_LEVEL, P)
        t0 = time.perf_counter()
        for k in keys:
            sl.insert(k)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def main():
    rng = random.Random(42)
    ns = []
    results = {'linkedlist': [], 'skiplist': []}

    for n in NS:
        print('n=', n)
        keys = gen_keys(n, rng)
        med_ll = measure_insert_linkedlist(keys)
        med_sl = measure_insert_skiplist(keys, rng)
        results['linkedlist'].append(med_ll)
        results['skiplist'].append(med_sl)
        ns.append(n)
        print('medians', med_ll, med_sl)

    # save json
    # with open('hw2/problem_3/p3_times.json', 'w') as fh:
    #     json.dump({'ns': ns, 'linkedlist': results['linkedlist'], 'skiplist': results['skiplist']}, fh)

    # plot
    plt.plot(ns, results['linkedlist'], label='LinkedList (p3_a)')
    plt.plot(ns, results['skiplist'], label='SkipList (p3_b)')
    plt.scatter(ns, results['linkedlist'], marker='o', s=30, color=plt.gca().lines[0].get_color())
    plt.scatter(ns, results['skiplist'], marker='o', s=30, color=plt.gca().lines[1].get_color())
    plt.xlabel('n')
    plt.ylabel('insert() median runtime (s)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('hw2/problem_3/p3_times.png')




    plt.yscale('log')
    plt.tight_layout()
    # plt.savefig('hw2/problem_3/p3_times_log.png')

    # print('Saved hw2/problem_3/p3_times.{png,json}')


if __name__ == '__main__':
    main()
