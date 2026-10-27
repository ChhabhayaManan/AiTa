# Recursion in Python

A recursive function **calls itself** on a smaller version of the same problem. Each big
problem is reduced, step by step, to a tiny one you can answer directly.

## The two parts every recursive function needs

1. **Base case**: the smallest input, answered without another call.
2. **Recursive case**: call yourself on a smaller input and build the answer from it.

```python
def factorial(n):
    if n == 0:
        return 1                  # base case
    return n * factorial(n - 1)   # recursive case
```

## What actually happens

Each call gets its **own** local variables, kept in a frame on the **call stack**.
`factorial(3)` waits for `factorial(2)`, which waits for `factorial(1)`, which waits for
`factorial(0)`. Then the results come back up: 1, 1, 2, 6.

## The recursion limit

Python stops runaway recursion at about **1000** nested calls and raises
**RecursionError: maximum recursion depth exceeded**. You hit it when the base case is
missing, when the input never gets smaller, or when the problem is simply too deep (a
chain of 100 000 calls). `sys.setrecursionlimit` can raise the limit, but for very deep
problems a loop is the safer choice.

## Thinking recursively

Assume the call on the smaller input already returns the right answer, and ask how to
finish the job with it. Sum of digits: `digit_sum(n) = n % 10 + digit_sum(n // 10)`, with
`digit_sum(0) = 0`.

## Worked example

Read `n` and print the `n`-th Fibonacci number: F(0) = 0, F(1) = 1, and each next number
is the sum of the two before it.

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

n = int(input())
print(fib(n))
```

Input `10` prints `55`. It is correct but slow for large `n`, because the same values are
computed again and again. Adding `@functools.lru_cache(maxsize=None)` above the `def`
makes Python remember each answer, which is the idea behind dynamic programming.

## Recursion that tries choices

Recursion is natural for "try every option": choose, recurse, undo (**backtracking**).
Listing every subset: for each element, recurse once with it and once without it.

## Common mistakes

- **No base case, or one that is never reached**, ending in RecursionError.
- **Input that does not shrink** on every call.
- **Forgetting `return`**: `fib(n - 1) + fib(n - 2)` without `return` gives `None`.
- **Sharing one list across calls** and forgetting to undo changes when backtracking.
- **Very deep recursion** on large inputs; use a loop.

## Remember

Base case first, then a call on a strictly smaller input. Each call has its own variables,
and Python stops you at about 1000 levels deep.
