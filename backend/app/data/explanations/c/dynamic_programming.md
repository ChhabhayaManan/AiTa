# Dynamic programming in C

Dynamic programming (DP) solves a problem by **solving smaller versions first, storing
their answers, and building the big answer from them**, so nothing is computed twice.

## Why it helps

The recursive Fibonacci function calls `fib(n - 1)` and `fib(n - 2)`, and each of those
calls the same smaller values again. `fib(40)` makes hundreds of millions of calls. But
there are only 41 different values to know. Store each one once and the work drops to 41
steps.

A problem suits DP when:

1. **Overlapping subproblems**: the same smaller question comes up many times.
2. **Optimal substructure**: the best answer can be built from best answers to smaller
   questions.

## The recipe

1. **State**: decide what `dp[i]` means, in one sentence. This is the most important step.
2. **Transition**: how `dp[i]` is computed from smaller states.
3. **Base cases**: the smallest states you know directly.
4. **Order**: fill the table so every state is ready before it is needed.
5. **Answer**: which entry holds the final result.

## Example: climbing stairs

You can climb 1 or 2 steps at a time. In how many ways can you reach step `n`?

- **State**: `dp[i]` = number of ways to reach step `i`.
- **Transition**: the last move was 1 step (from `i - 1`) or 2 steps (from `i - 2`), so
  `dp[i] = dp[i - 1] + dp[i - 2]`.
- **Base cases**: `dp[0] = 1` (one way: do nothing), `dp[1] = 1`.
- **Order**: `i` from 2 up to `n`.
- **Answer**: `dp[n]`.

```c
#include <stdio.h>

long long dp[100001];

int main(void) {
    int n;
    scanf("%d", &n);
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = (dp[i - 1] + dp[i - 2]) % 1000000007;
    }
    printf("%lld\n", dp[n]);
    return 0;
}
```

Input `5` prints `8`. The counts grow very fast, which is why problems ask for the answer
modulo 1 000 000 007; take the remainder at every step, not only at the end.

## Top-down and bottom-up

- **Bottom-up** (above): fill the table with a loop from the smallest state up.
- **Top-down (memoisation)**: keep the recursive function, but store each answer in an
  array the first time and return the stored value on later calls.

Both give the same results. Bottom-up avoids deep recursion; top-down can be easier to
write when the order of states is awkward.

## Bigger states

Some problems need two numbers to describe a state. In the 0/1 knapsack, `dp[i][w]` is
the best value using the first `i` items with capacity `w`. On a grid, `dp[r][c]` is the
number of paths to cell `(r, c)`. The recipe stays the same.

## Common mistakes

- **A vague state.** If you cannot say what `dp[i]` means in one sentence, the
  transition will be wrong.
- **Missing or wrong base cases.**
- **Filling in the wrong order**, so you read a state before it is computed.
- **Overflow**: use `long long` and apply the modulo at each step.
- **Large local tables**: declare big `dp` arrays outside `main`.

## Remember

Define the state, write the transition, set the base cases, fill in order. Every
subproblem is solved once and reused.
