# Dynamic programming in Python

Dynamic programming (DP) solves a problem by **solving smaller versions first, storing
their answers, and building the big answer from them**, so nothing is computed twice.

## Why it helps

Plain recursive Fibonacci recomputes the same values over and over: `fib(35)` makes about
30 million calls, yet only 36 different values exist. Store each one once and the work
drops to 36 steps.

A problem suits DP when it has:

1. **Overlapping subproblems**: the same smaller question comes up many times.
2. **Optimal substructure**: the best answer is built from best answers to smaller
   questions.

## The recipe

1. **State**: say in one sentence what `dp[i]` means. Most DP bugs start here.
2. **Transition**: how `dp[i]` comes from smaller states.
3. **Base cases**: the smallest states, known directly.
4. **Order**: fill the table so each state is ready before it is used.
5. **Answer**: which entry holds the result.

## Example: climbing stairs

You climb 1 or 2 steps at a time. In how many ways can you reach step `n`?

- **State**: `dp[i]` = number of ways to reach step `i`.
- **Transition**: the last move came from `i - 1` or `i - 2`, so
  `dp[i] = dp[i - 1] + dp[i - 2]`.
- **Base cases**: `dp[0] = 1`, `dp[1] = 1`.
- **Answer**: `dp[n]`.

```python
MOD = 1_000_000_007
n = int(input())
dp = [0] * (n + 2)
dp[0] = dp[1] = 1
for i in range(2, n + 1):
    dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
print(dp[n])
```

Input `5` prints `8`. Python integers never overflow, but huge numbers make every addition
slower, so still take the modulo at each step when the problem asks for it.

## Top-down: memoisation

Keep the recursion and let Python remember the answers:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways(i):
    if i <= 1:
        return 1
    return (ways(i - 1) + ways(i - 2)) % 1_000_000_007
```

Top-down is short to write, but it recurses, and Python stops at about 1000 levels. For
`n = 100 000` use the bottom-up loop.

## Bigger states

Some states need two numbers: in the 0/1 knapsack, `dp[i][w]` is the best value using the
first `i` items with capacity `w`; on a grid, `dp[r][c]` counts paths to cell `(r, c)`.
Build a 2D table with `[[0] * cols for _ in range(rows)]`, never with `[[0] * cols] * rows`,
which shares one row. The recipe is the same.

## Common mistakes

- **A vague state**, so the transition does not match it.
- **Wrong base cases**, or a table too short for index `n`.
- **Filling in the wrong order**, reading states not yet computed.
- **Deep memoised recursion** hitting RecursionError on large inputs.
- **`[[0] * c] * r`** for a 2D table.

## Remember

State, transition, base cases, order. Each subproblem is solved once, stored, and reused.
