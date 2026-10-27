# Recursion in C++

A recursive function **calls itself** on a smaller version of the same problem. Each big
problem is reduced, step by step, to a tiny one you can answer directly.

## The two parts every recursive function needs

1. **Base case**: the smallest input, answered without another call.
2. **Recursive case**: call yourself on a smaller input and build the answer from it.

```cpp
long long factorial(int n) {
    if (n == 0) {
        return 1;                    // base case
    }
    return n * factorial(n - 1);     // recursive case
}
```

## What actually happens

Every call gets its **own copy** of its parameters and local variables, stored in a frame
on the **call stack**. `factorial(3)` waits for `factorial(2)`, which waits for
`factorial(1)`, which waits for `factorial(0)`. Then the results return upwards:
1, 1, 2, 6.

If the base case is missing, or the input never shrinks, the calls never stop. The stack
runs out and the program crashes (a **stack overflow**, often reported as a segmentation
fault).

## Thinking recursively

Assume the call on the smaller input already returns the right answer, and ask how to
finish the job with it. Sum of a vector from index `i`: `sum(v, i) = v[i] + sum(v, i + 1)`,
with `sum(v, v.size()) = 0`. Pass the vector as `const vector<int> &` so it is not copied
on every call.

## Worked example

Read `n` and print the `n`-th Fibonacci number: F(0) = 0, F(1) = 1, and each next number
is the sum of the two before it.

```cpp
#include <iostream>
using namespace std;

long long fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    int n;
    cin >> n;
    cout << fib(n) << "\n";
    return 0;
}
```

Input `10` prints `55`. It is correct but slow for large `n`, because the same values are
computed many times. Dynamic programming fixes that by remembering them.

## Recursion that tries choices

Recursion is natural when you must try every option: at each step choose one, recurse,
then undo the choice (**backtracking**). For example, printing every subset of a set:
include the next element and recurse, then exclude it and recurse.

## Recursion or a loop?

A loop uses no extra stack and is usually faster. Choose recursion when the problem is
made of smaller copies of itself: splitting in halves, trees, trying choices.

## Common mistakes

- **No base case, or one that is never reached** (testing `n == 0` when `n` can skip it
  or go negative).
- **Input that does not get smaller** on each call.
- **Dropping the result**: calling `fib(n - 1)` without using or returning it.
- **Copying a big vector** on every call by passing it by value.
- **Recursing a million levels deep**, which overflows the stack; use a loop.

## Remember

Base case first, then a call on a strictly smaller input. Each call has its own variables
on the call stack, and the answer is built on the way back up.
