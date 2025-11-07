import random, time, statistics, math
import matplotlib.pyplot as plt
from p3_a import LinkedList
from p3_b import SkipList

REPEATS = 7
BATCH = 1000          # number of timed inserts at size n
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

def time_per_insert_ll(n, rng):
    base = rng.sample(range(10**9), n + BATCH)
    init, batch = base[:n], base[n:]
    times = []
    for _ in range(REPEATS):
        ll = build_ll(init)
        t0 = time.perf_counter()
        for k in batch:
            ll.insert(k)
        dt = time.perf_counter() - t0
        times.append(dt / BATCH)
    return statistics.median(times)

def time_per_insert_sl(n, rng):
    base = rng.sample(range(10**9), n + BATCH)
    init, batch = base[:n], base[n:]
    times = []
    for _ in range(REPEATS):
        sl = build_sl(init)
        t0 = time.perf_counter()
        for k in batch:
            sl.insert(k)
        dt = time.perf_counter() - t0
        times.append(dt / BATCH)
    return statistics.median(times)

def main():
    rng = random.Random(42)
    ll_y, sl_y = [], []
    for n in NS:
        print("n =", n)
        ll_t = time_per_insert_ll(n, rng)
        sl_t = time_per_insert_sl(n, rng)
        ll_y.append(ll_t)
        sl_y.append(sl_t)
        print(" per-insert:", ll_t, sl_t)

    # Raw per-insert vs n
    plt.figure()
    # plt.plot(NS, ll_y, marker='o', label='LinkedList')
    plt.plot(NS, sl_y, marker='o', label='SkipList')
    plt.xlabel('n')
    plt.ylabel('insert median time')
    plt.legend(); plt.tight_layout()
    plt.savefig('hw2/problem_3/insert_per_op_skip.png')

    # # Transform checks
    # # LL: (time per op) / n should be ~constant
    # plt.figure()
    # plt.plot(NS, [t/n for t,n in zip(ll_y, NS)], marker='o')
    # plt.xlabel('n'); plt.ylabel('(sec / insert) / n  [LinkedList]')
    # plt.tight_layout(); plt.savefig('hw2/problem_3/insert.png')

    # # SL: (time per op) / log2(n) should be ~constant
    # plt.figure()
    # logs = [math.log2(n) for n in NS]
    # plt.plot(NS, [t/L for t,L in zip(sl_y, logs)], marker='o')
    # plt.xlabel('n'); plt.ylabel('(sec / insert) / log2(n)  [SkipList]')
    # plt.tight_layout(); plt.savefig('hw2/problem_3/insert.png')

    # Optional: regression sanity check (slope on log-log)
    # If you want: fit slope of LL ≈ 1, SL ≈ 0 on (n vs per-op) after transforms

if __name__ == '__main__':
    main()
