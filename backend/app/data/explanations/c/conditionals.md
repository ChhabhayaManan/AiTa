# Conditionals in C

A conditional lets your program **choose**: do one thing when something is true, and
something else when it is not.

## if, else if, else

```c
if (marks >= 90) {
    printf("A\n");
} else if (marks >= 75) {
    printf("B\n");
} else {
    printf("C\n");
}
```

C checks the conditions from top to bottom and runs **only the first block whose
condition is true**. If none is true, the `else` block runs. Because the checks happen in
order, `marks >= 75` here really means "at least 75 **and** below 90".

## What counts as true

C has no separate true/false type in older code: a condition is an expression whose
value is **0 for false and anything else for true**.

| Operator | Meaning |
|---|---|
| `==` `!=` | equal, not equal |
| `<` `<=` `>` `>=` | comparisons |
| `&&` | and: both must be true |
| `\|\|` | or: at least one must be true |
| `!` | not |

`&&` and `||` stop early: in `b != 0 && a / b > 2`, the division never happens when `b`
is 0. This is called short-circuit evaluation and it often protects you from crashes.

## switch

When you compare one value against many fixed cases, `switch` is cleaner:

```c
switch (day) {
    case 1: printf("Mon\n"); break;
    case 2: printf("Tue\n"); break;
    default: printf("Other\n");
}
```

Without `break`, execution **falls through** into the next case.

## Worked example

Read a year and print `leap` or `not leap`. A year is a leap year if it divides by 4,
except century years, which must also divide by 400.

```c
#include <stdio.h>

int main(void) {
    int y;
    scanf("%d", &y);
    if ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) {
        printf("leap\n");
    } else {
        printf("not leap\n");
    }
    return 0;
}
```

`2024` prints `leap`, `1900` prints `not leap`, `2000` prints `leap`.

## Common mistakes

- **`=` instead of `==`.** `if (x = 5)` sets `x` to 5 and is always true. Compare with `==`.
- **Wrong order of checks.** Testing `marks >= 50` before `marks >= 90` means nobody ever
  gets an A. Put the strictest condition first.
- **Separate `if`s for exclusive cases.** Two plain `if`s can both run; use `else if` when
  only one answer is allowed.
- **Missing braces.** Without `{ }`, only the next single statement belongs to the `if`.
- **Forgetting `break` in a switch.**

## Remember

Conditions are checked in order and the first true one wins. Compare with `==`, combine
with `&&` and `||`, and always cover the "none of these" case.
