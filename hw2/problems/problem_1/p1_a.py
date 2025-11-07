# Problem 1a

def maxsum_list(xs) -> int:
    if len(xs) == 0:
        return 0
    elif len(xs) == 1:
        return xs[0]
    
    dp = [0] * (len(xs) + 1)
    dp[0] = 0
    dp[1] = xs[0]
    for i in range(2, len(dp)):
        take_current = dp[i-2] + xs[i-1]
        skip_current = dp[i-1]
        dp[i] = max(take_current, skip_current)
    return dp[-1]
