# Recursion in C

A recursive function **calls itself** on a smaller version of the same problem. It works
because every big problem is reduced, step by step, to a tiny one you can answer directly.

## The two parts every recursive function needs

1. **Base case**: the smallest input, answered without another call.
2. **Recursive case**: solve a smaller input by calling yourself, then build the answer.

```c
long long factorial(int n) {
    if (n == 0) {
        return 1;                    /* base case */
    }
    return n * factorial(n - 1);     /* recursive case */
}
```

## What actually happens

Each call gets its **own copy** of `n`, kept in a frame on the **call stack**.
`factorial(3)` waits for `factorial(2)`, which waits for `factorial(1)`, which waits for
`factorial(0)`. Then the answers come back up:

```
factorial(0) = 1
factorial(1) = 1 * 1 = 1
factorial(2) = 2 * 1 = 2
factorial(3) = 3 * 2 = 6
```

If the base case is missing, or the input never gets smaller, the calls never stop. The
stack fills up and the program crashes with a **stack overflow** (often shown as a
segmentation fault).

## Thinking recursively

Trust that the call on the smaller input returns the right answer, and ask: "how do I
finish the job using it?" For the sum of digits of `n`: the last digit is `n % 10`, the
rest is `n / 10`, so `digits(n) = n % 10 + digits(n / 10)`, with `digits(0) = 0`.

## Worked example

Read `n` and print the `n`-th Fibonacci number, where F(0) = 0, F(1) = 1 and each next
number is the sum of the two before it.

```c
#include <stdio.h>

long long fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    int n;
    scanf("%d", &n);
    printf("%lld\n", fib(n));
    return 0;
}
```

Input `10` prints `55`. This version is correct but slow for large `n`: it computes the
same values again and again (`fib(3)` is worked out many times). The dynamic programming
topic shows how to remember them.

## Recursion or a loop?

Anything recursive can be written with a loop, and a loop uses no extra stack. Recursion
shines when the problem is naturally made of smaller copies of itself: trees, splitting
an array in halves, trying every choice.

## Common mistakes

- **No base case, or one that is never reached** (for example `n == 0` when `n` can go
  negative).
- **Not making the input smaller** on every call.
- **Forgetting to `return`** the recursive result: writing `fib(n - 1) + fib(n - 2);`
  without `return` throws it away.
- **Too deep.** A million nested calls can overflow the stack; use a loop instead.

## Remember

Base case first, then a call on a strictly smaller input. Each call has its own variables
on the call stack, and the answers are built on the way back up.
