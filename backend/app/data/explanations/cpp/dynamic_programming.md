# Dynamic programming in C++

Dynamic programming (DP) solves a problem by **solving smaller versions first, storing
their answers, and building the big answer from them**, so nothing is computed twice.

## Why it helps

Plain recursive Fibonacci recomputes the same values over and over: `fib(40)` makes
hundreds of millions of calls, yet only 41 different values exist. Store each one once and
the work drops to 41 steps.

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

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    const long long MOD = 1000000007;
    vector<long long> dp(n + 2, 0);
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD;
    }
    cout << dp[n] << "\n";
    return 0;
}
```

Input `5` prints `8`. The counts grow fast, so problems ask for the answer modulo
1 000 000 007; take the remainder at every step, not only at the end. The vector has size
`n + 2` so that `dp[1]` exists even when `n` is 0.

## Top-down: memoisation

Keep the recursion, but remember each answer:

```cpp
vector<long long> memo(100001, -1);

long long ways(int i) {
    if (i <= 1) return 1;
    if (memo[i] != -1) return memo[i];
    return memo[i] = (ways(i - 1) + ways(i - 2)) % 1000000007;
}
```

Bottom-up avoids deep recursion; top-down is handy when the order of states is awkward.

## Bigger states

Some states need two numbers: in the 0/1 knapsack, `dp[i][w]` is the best value using the
first `i` items with capacity `w`; on a grid, `dp[r][c]` counts paths to cell `(r, c)`. Use
`vector<vector<long long>> dp(rows, vector<long long>(cols, 0));`. The recipe is the same.

## Common mistakes

- **A vague state**, so the transition does not match it.
- **Wrong base cases**, or a table too small for index `n`.
- **Filling in the wrong order**, reading states not yet computed.
- **Overflow**: use `long long` and take the modulo at every step.
- **Copying the dp vector** into a recursive helper by value.

## Remember

State, transition, base cases, order. Each subproblem is solved once, stored, and reused.
