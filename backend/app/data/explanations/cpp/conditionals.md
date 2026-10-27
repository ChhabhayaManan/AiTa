# Conditionals in C++

A conditional lets your program **choose**: do one thing when something is true, and
something else when it is not.

## if, else if, else

```cpp
if (marks >= 90) {
    cout << "A\n";
} else if (marks >= 75) {
    cout << "B\n";
} else {
    cout << "C\n";
}
```

C++ checks the conditions from top to bottom and runs **only the first block whose
condition is true**. If none is true, the `else` runs. Because of the order,
`marks >= 75` here really means "at least 75 and below 90".

## Conditions and bool

A condition has type `bool`: `true` or `false`. Numbers also work in a condition:
0 is false and anything else is true.

| Operator | Meaning |
|---|---|
| `==` `!=` | equal, not equal |
| `<` `<=` `>` `>=` | comparisons |
| `&&` | and: both must be true |
| `\|\|` | or: at least one must be true |
| `!` | not |

`&&` and `||` stop as soon as the answer is known (short-circuit evaluation). In
`i < n && a[i] > 0`, `a[i]` is never read when `i` is out of range.

## The conditional operator

`condition ? value_if_true : value_if_false` picks one of two values in a single
expression:

```cpp
cout << (x % 2 == 0 ? "even" : "odd") << "\n";
```

## switch

For one value compared against many fixed cases:

```cpp
switch (op) {
    case '+': cout << a + b << "\n"; break;
    case '-': cout << a - b << "\n"; break;
    default:  cout << "unknown\n";
}
```

Without `break`, execution **falls through** into the next case.

## Worked example

Read a year and print `leap` or `not leap`. A year is a leap year if it divides by 4,
except century years, which must also divide by 400.

```cpp
#include <iostream>
using namespace std;

int main() {
    int y;
    cin >> y;
    bool leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
    cout << (leap ? "leap" : "not leap") << "\n";
    return 0;
}
```

`2024` prints `leap`, `1900` prints `not leap`, `2000` prints `leap`.

## Common mistakes

- **`=` instead of `==`.** `if (x = 5)` assigns and is always true.
- **Strictest check last.** Testing `marks >= 50` first means nobody reaches the A branch.
- **Separate `if`s for exclusive cases.** Both can run; use `else if`.
- **Comparing doubles with `==`.** `0.1 + 0.2 == 0.3` is false; compare with a small
  tolerance instead.
- **Forgetting `break`** in a `switch`.

## Remember

Conditions run in order and the first true one wins. Use `==` to compare, `&&` and `||`
to combine, and always handle the "none of these" case.
