'''
Problem 2

input: Integer M and a list of intervals [a, b].
output: List of list of integers composing the covering.

TODO: implement a correct greedy algorithm from the homework.
'''
def interval_covering(M: int, intervals: list) -> list:

    # Do some pre-requisite work to sort the sub-intervals by start (chronological)
    # This will put any redundant sub-intervals next to each other so we can evaluate with a linear scan
    intervals.sort(key=lambda sub_interval: (sub_interval[0]))

    # The sub-intervals that we will return
    minimum_covering = []
    # The earliest start time that we will consider at each iteration
    start_time_to_evaluate = 0
    # Current internal index
    i = 0

    # Stop condition, when we've fully considered all intervals up to M
    while start_time_to_evaluate < M:
        latest_finish_time = start_time_to_evaluate
        latest_finish_time_j = -1
        # In this iteration, consider all the sub-intervals that cover [`start_time_to_evaluate`, B]
        # Where we want to delete the sub-interval that is the earliest, i.e. the minimum B value
        while i < len(intervals):
            sub_interval = intervals[i]
            start_time = sub_interval[0]
            finish_time = sub_interval[1]
            # Encountered a sub-interval with a start-time > `start_time_to_evaluate``
            # Case 1: This sub-interval has the same finish time as the last one, so this is
            # redundant and definitely doesn't cover as much "range" as the last one
            # Case 2: This sub-interval has a later finish time as the last one, so it will
            # be considered in the next iteration
            if start_time > start_time_to_evaluate:
                break
            # Case 1: This is the first sub-interval we are evaluating in this range
            # Case 2: We've found a redundant sub-interval, this one has a later start time so we
            # should pick it instead of the last one (equivalent to deleting the one with 
            # an earlier finish time)
            if finish_time > latest_finish_time:
                latest_finish_time = finish_time
                latest_finish_time_j = i
            # Look at next interval
            i += 1

        # Of all the redundant sub-intervals we've considered that cover [`current_covered_interaval`, B],
        # pick the latest/delete the earliest
        minimum_covering.append(intervals[latest_finish_time_j])
        start_time_to_evaluate = latest_finish_time

    return minimum_covering
