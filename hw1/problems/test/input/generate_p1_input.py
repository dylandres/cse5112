#!/usr/bin/env python3
"""Generate a problem_1 input file for given n.

Format matches existing test files:
First line: n
Then n lines: hospitals' preference lists (space-separated permutations of 0..n-1)
Then n lines: doctors' preference lists (space-separated permutations of 0..n-1)

The script streams output to avoid large memory use.

Usage:
    python3 generate_p1_input.py --n 10000 --out test_p1_n10000_1.txt --seed 42

"""
import sys
import argparse
import random
from typing import List


def write_permutation(n: int, rng: random.Random, fout) -> None:
    # generate a random permutation efficiently
    perm = list(range(n))
    rng.shuffle(perm)
    fout.write(" ".join(map(str, perm)))
    fout.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True, help="size n (e.g. 10000)")
    parser.add_argument("--out", type=str, required=True, help="output filename (relative to this script) or '-' for stdout")
    parser.add_argument("--seed", type=int, default=None, help="optional RNG seed for reproducibility")
    parser.add_argument("--preview", action="store_true", help="only write first 10 lines for quick preview")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    target_path = args.out
    if target_path == "-":
        fout = sys.stdout
    else:
        fout = open(target_path, "w", encoding="utf-8")

    try:
        n = args.n
        fout.write(f"{n}\n")
        lines = n if not args.preview else min(10, n)
        # write hospitals' preferences
        for i in range(lines):
            write_permutation(n, rng, fout)
        if args.preview and lines < n:
            # skip remaining hospitals in preview with placeholder
            for _ in range(n - lines):
                fout.write("0")
                fout.write("\n")
        # write doctors' preferences
        for i in range(lines):
            write_permutation(n, rng, fout)
        if args.preview and lines < n:
            for _ in range(n - lines):
                fout.write("0")
                fout.write("\n")
    finally:
        if fout is not sys.stdout:
            fout.close()


if __name__ == "__main__":
    main()
