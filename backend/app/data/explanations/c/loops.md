# Loops in C

A loop **repeats** a block of code. You need one whenever the work depends on how much
input there is: add up `n` numbers, print a pattern, keep going until a condition fails.

## The for loop

Use `for` when you know how many times to repeat.

```c
for (int i = 0; i < n; i++) {
    printf("%d\n", i);
}
```

The three parts are: **start** (`int i = 0`), **keep going while** (`i < n`), and **step**
(`i++`, add 1). This prints `0` up to `n - 1`, which is exactly `n` lines.

## The while loop

Use `while` when you repeat until something happens and you do not know in advance how
many times.

```c
int n = 1234, digits = 0;
while (n > 0) {
    n = n / 10;
    digits++;
}
/* digits is now 4 */
```

The condition is checked **before** each repetition, so the body may run zero times.

## do-while

`do { ... } while (condition);` checks **after** the body, so it always runs at least once.
It is handy for "ask again until the input is valid".

## break and continue

- `break` leaves the loop immediately.
- `continue` skips the rest of this repetition and goes to the next one.

## Worked example

Read `n`, then `n` numbers, and print their sum and the largest one.

```c
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    long long sum = 0;
    int largest = 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        sum += x;
        if (i == 0 || x > largest) {
            largest = x;
        }
    }
    printf("%lld %d\n", sum, largest);
    return 0;
}
```

Input `4` then `3 -1 9 2` prints `13 9`. The largest starts from the first number, not
from 0, so a list of all negative numbers still works.

## Common mistakes

- **Off by one.** `i <= n` with `i` starting at 0 runs `n + 1` times. Count the
  repetitions on a tiny example.
- **A loop that never ends.** If nothing inside a `while` changes the condition, it runs
  forever. Make sure every repetition moves towards the end.
- **Not resetting a variable.** A sum used in an outer loop must be set back to 0 at the
  start of each outer repetition.
- **Semicolon after the header.** `for (i = 0; i < n; i++);` repeats an empty statement;
  the block below then runs once.

## Remember

`for` when you know the count, `while` when you wait for a condition. Check the first and
the last repetition on a small input before you trust a loop.
