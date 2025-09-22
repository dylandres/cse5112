'''
Problem 4b

input: 
    values -- list of integers. 
    d_mode -- most frequent delta.
output: integer containing the frequency of d_mode.

TODO: implement your solution in Θ(n log n).
'''
def most_frequent_difference_b(values, d_mode) -> int:
    count = 0
    values.sort()
    if d_mode != 0:
        for i in range(len(values)):
            # Subtracting the mode will give us the "other" value that would produce this pairwise difference
            diff = values[i] - d_mode
            # Binary search for the first index of this other value
            first_occurence_of_diff = binary_search_for_value(values, diff, "FIRST")
            # Binary search for the last index of this other value
            last_occurence_of_diff = binary_search_for_value(values, diff, "LAST")
            # Get the number of total occurence of this value. If it doesn't exist, we will get 0
            count += (last_occurence_of_diff - first_occurence_of_diff)
    
    # if d_mode is 0
    else:
        i = 0
        while i < len(values):
            j = i + 1
            # Find consecutive dups that contributed to mode=0
            while j < len(values):
                if values[j] != values[i]:
                    break
                j += 1
            # The number of pairs across these dups gives us
            # number of the times diff=0 occurred
            num_dups = j - i
            # Can't include i == j, so we do (num_dups) * (num_dups minus this one)
            count += num_dups * (num_dups - 1)
            i = j
    return count

def binary_search_for_value(arr, target, which_occurence):
    lower = 0
    upper = len(arr)
    while lower < upper:
        mid = (lower + upper) // 2
        # Target is on the right
        if arr[mid] < target:
            lower = mid + 1
        # Target is on the left
        elif arr[mid] > target:
            upper = mid
        # This is the target
        else:
            # Keep looking left for first occurrence
            if "FIRST" == which_occurence:
                upper = mid
            # Keep looking right for last occurrence
            if "LAST" == which_occurence:
                lower = mid + 1
    return lower
