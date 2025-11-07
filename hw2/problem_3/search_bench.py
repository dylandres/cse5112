#!/usr/bin/env python3
"""Benchmark search (per-op) performance for LinkedList (p3_a) vs SkipList (p3_b).

Produces:
 - hw2/problem_3/search_per_op.png
"""
import random, time, statistics, math
import matplotlib.pyplot as plt
from p3_a import LinkedList
from p3_b import SkipList

REPEATS = 7
BATCH = 1000                    # number of timed searches at size n
NS = [200, 500, 1000, 2000, 4000, 5000]
MAX_LEVEL = 16
P = 0.5

def build_ll(keys):
    ll = LinkedList()
    for k in keys:
        ll.insert(k)
    return ll

def build_sl(keys):
    sl = SkipList(MAX_LEVEL, P)
    for k in keys:
        sl.insert(k)
    return sl

def time_per_search_ll(n, rng):
    # Build with n unique keys, then search a random batch of PRESENT keys
    keys = rng.sample(range(10**9), n)
    batch = rng.sample(keys, min(BATCH, n))
    times = []
    for _ in range(REPEATS):
        ll = build_ll(keys)
        t0 = time.perf_counter()
        for k in batch:
            _ = ll.search(k)
        dt = time.perf_counter() - t0
        times.append(dt / len(batch))
    return statistics.median(times)

def time_per_search_sl(n, rng):
    keys = rng.sample(range(10**9), n)
    batch = rng.sample(keys, min(BATCH, n))
    times = []
    for _ in range(REPEATS):
        sl = build_sl(keys)
        t0 = time.perf_counter()
        for k in batch:
            _ = sl.search(k)
        dt = time.perf_counter() - t0
        times.append(dt / len(batch))
    return statistics.median(times)

# Optional: mixed hit/miss searches (50/50) to test behavior on absent keys too
def time_per_search_mixed_sl(n, rng):
    keys = rng.sample(range(10**9), n)
    present = rng.sample(keys, min(BATCH // 2, n))
    # Generate absents disjoint from 'keys'
    absents = set()
    while len(absents) < len(present):
        cand = rng.randrange(10**9, 2 * 10**9)
        if cand not in keys:
            absents.add(cand)
    batch = present + list(absents)
    rng.shuffle(batch)

    times = []
    for _ in range(REPEATS):
        sl = build_sl(keys)
        t0 = time.perf_counter()
        for k in batch:
            _ = sl.search(k)
        dt = time.perf_counter() - t0
        times.append(dt / len(batch))
    return statistics.median(times)

def main():
    rng = random.Random(42)
    ll_y, sl_y = [], []
    for n in NS:
        print("n =", n)
        ll_t = time_per_search_ll(n, rng)
        sl_t = time_per_search_sl(n, rng)
        ll_y.append(ll_t)
        sl_y.append(sl_t)
        print(" per-search:", ll_t, sl_t)

    # Raw per-search vs n
    plt.figure()
    # plt.plot(NS, ll_y, marker='o', label='LinkedList')
    plt.plot(NS, sl_y, marker='o', label='SkipList')
    plt.xlabel('n')
    plt.ylabel('search median time')
    plt.legend(); plt.tight_layout()
    plt.savefig('hw2/problem_3/search_per_op_skip.png')

    # # Transform checks (uncomment if you want the "flatness" confirmations):
    # # LinkedList: (time per op)/n ~ constant
    # plt.figure()
    # plt.plot(NS, [t/n for t, n in zip(ll_y, NS)], marker='o')
    # plt.xlabel('n'); plt.ylabel('(sec / search) / n  [LinkedList]')
    # plt.tight_layout(); plt.savefig('hw2/problem_3/search_ll_div_n.png')
    #
    # # SkipList: (time per op)/log2(n) ~ constant
    # logs = [math.log2(n) for n in NS]
    # plt.figure()
    # plt.plot(NS, [t/L for t, L in zip(sl_y, logs)], marker='o')
    # plt.xlabel('n'); plt.ylabel('(sec / search) / log2(n)  [SkipList]')
    # plt.tight_layout(); plt.savefig('hw2/problem_3/search_sl_div_log.png')

if __name__ == '__main__':
    main()
