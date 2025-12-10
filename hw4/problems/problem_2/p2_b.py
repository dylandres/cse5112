import bisect

def binary_search(packages, boxes):
    # Sort packages once: O(n log n)
    packages = sorted(packages)

    least_waste = float('inf')
    possible = False

    for supplier in boxes:
        supplier_sorted = sorted(supplier)

        cur_waste = 0
        i = 0

        for box in supplier_sorted:
            if i >= len(packages):
                break

            j = bisect.bisect_right(packages, box, lo=i)
            for k in range(i, j):
                cur_waste += box - packages[k]
            i = j

        if i == len(packages):
            possible = True
            if cur_waste < least_waste:
                least_waste = cur_waste

    return least_waste if possible else -1
