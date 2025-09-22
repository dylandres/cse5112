'''
Problem 4c

input: 
    values -- list of integers. 
    d_mode -- most frequent delta.
output: integer containing the frequency of d_mode.

TODO: implement your solution in Θ(n).
'''
def most_frequent_difference_c(values, d_mode) -> int:
    count = 0
    # Track frequencies of all elements
    frequencies = {}
    for element in values:
        try:
            frequencies[element] += 1
        except KeyError:
            frequencies[element] = 1

    # For each element
    for element, frequency in frequencies.items():
        # For a pair (a,b) s.t. b - a = d_mode, it is equivalent that b = a + d_mode
        other_element_in_pair = element + d_mode
        freq_of_other_pair_element = frequencies.get(other_element_in_pair)
        # We can multiply by the frequency of b to find out how many pairwise elements of (a,b) could be made
        if freq_of_other_pair_element:
            count += frequency * freq_of_other_pair_element

    # The above count also counts (a,b) where i == j
    if d_mode == 0:
        double_counts = sum(frequencies.values())
        count -= double_counts
    return count
