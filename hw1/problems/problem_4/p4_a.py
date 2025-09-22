'''
Problem 4a

input: 
    values -- list of integers. 
    d_mode -- most frequent delta.
output: integer containing the frequency of d_mode.

TODO: implement your solution in Θ(n^2).
'''
def most_frequent_difference_a(values, d_mode) -> int:
    count = 0
    for i in range(len(values)):
        for j in range(len(values)):
            if i == j:
                continue
            diff = values[i] - values[j]
            if diff == d_mode:
                count += 1
    return count
