import time
import json
import glob
import statistics
import matplotlib.pyplot as plt
from p1_b import stable_matching_1b
from p1_c import stable_matching_1c

INPUT_GLOB = 'test/input/benchmarks/test_p1_*.txt'
REPEATS = 10

# collect files and sort them by the integer n on their first line so we process
# inputs in increasing n order (instead of filename order)
raw_files = [f for f in glob.glob(INPUT_GLOB) if 'public' not in f and 'p3' not in f]
files_with_n = []
for f in raw_files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            first = fh.readline().strip()
            n = int(first) if first else float('inf')
    except Exception:
        n = float('inf')
    files_with_n.append((n, f))
files_with_n.sort(key=lambda x: x[0])
files = [f for (_, f) in files_with_n]

results = {'b': [], 'c': [], 'files': files}

for f in files:
    times_b = []
    times_c = []
    for i in range(REPEATS):
        print(f"Running stable_matching_1b on {f} for the {i}th time")
        t0 = time.perf_counter()
        stable_matching_1b(f)
        delta = time.perf_counter() - t0
        times_b.append(delta)
        print(f"delta: {delta}")
        print(f"Running stable_matching_1c on {f} for the {i}th time")
        t0 = time.perf_counter()
        stable_matching_1c(f)
        delta = time.perf_counter() - t0
        times_c.append(delta)
        print(f"delta: {delta}")
    bmed = statistics.median(times_b)
    cmed = statistics.median(times_c)
    results['b'].append(bmed)
    results['c'].append(cmed)
    print(f, 'b median', results['b'][-1], 'c median', results['c'][-1])

# plot
ns = []
for f in files:
    with open(f) as fh:
        n = int(fh.readline())
        ns.append(n)

plt.plot(ns, results['b'], label='stable_matching_1b')
plt.plot(ns, results['c'], label='stable_matching_1c')
# draw markers at the actual n values
plt.scatter(ns, results['b'], marker='o', s=30, color=plt.gca().lines[0].get_color())
plt.scatter(ns, results['c'], marker='o', s=30, color=plt.gca().lines[1].get_color())
plt.xlabel('n')
plt.ylabel('median runtime (s)')
plt.legend()
plt.tight_layout()
plt.savefig('bench/p1_times.png')

# also save a log-scaled version (log y-axis)
plt.yscale('log')
plt.tight_layout()
plt.savefig('bench/p1_times_log.png')

# loglog
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig('bench/p1_times_log.png')

with open('bench/p1_times.json', 'w') as fh:
    json.dump({'ns': ns, 'b': results['b'], 'c': results['c'], 'files': files}, fh)

print('Done. Saved bench/p1_times.png and bench/p1_times.json')
