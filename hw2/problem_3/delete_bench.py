#!/usr/bin/env python3
"""Benchmark delete (per-op) performance for LinkedList (p3_a) vs SkipList (p3_b).

Produces:
 - hw2/problem_3/delete_per_op.png
"""
import random, time, statistics
import matplotlib.pyplot as plt
from p3_a import LinkedList
from p3_b import SkipList

REPEATS = 7
BATCH = 1000
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

def time_per_delete_ll(n, rng):
    # Build with n unique keys, then delete a random batch of present keys
    keys = rng.sample(range(10**9), n)
    batch = rng.sample(keys, min(BATCH, n))  # ensure BATCH <= n
    times = []
    for _ in range(REPEATS):
        ll = build_ll(keys)
        del_order = list(batch)
        rng.shuffle(del_order)
        t0 = time.perf_counter()
        for k in del_order:
            ll.delete(k)
        dt = time.perf_counter() - t0
        times.append(dt / len(del_order))
    return statistics.median(times)

def time_per_delete_sl(n, rng):
    keys = rng.sample(range(10**9), n)
    batch = rng.sample(keys, min(BATCH, n))
    times = []
    for _ in range(REPEATS):
        sl = build_sl(keys)
        del_order = list(batch)
        rng.shuffle(del_order)
        t0 = time.perf_counter()
        for k in del_order:
            sl.delete(k)
        dt = time.perf_counter() - t0
        times.append(dt / len(del_order))
    return statistics.median(times)

def main():
    rng = random.Random(42)
    ll_y, sl_y = [], []
    for n in NS:
        print("n =", n)
        ll_t = time_per_delete_ll(n, rng)
        sl_t = time_per_delete_sl(n, rng)
        ll_y.append(ll_t)
        sl_y.append(sl_t)
        print(" per-delete:", ll_t, sl_t)

    plt.figure()
    # plt.plot(NS, ll_y, marker='o', label='LinkedList')
    plt.plot(NS, sl_y, marker='o', label='SkipList')
    plt.xlabel('n')
    plt.ylabel('delete median runtime')
    plt.legend(); plt.tight_layout()
    plt.savefig('hw2/problem_3/delete_per_op_skip.png')

if __name__ == '__main__':
    main()
