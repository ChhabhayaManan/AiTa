# Loops in C++

A loop **repeats** a block of code. You need one whenever the amount of work depends on
the input: add up `n` numbers, print a pattern, keep going until something happens.

## The for loop

Use `for` when you know how many times to repeat.

```cpp
for (int i = 0; i < n; i++) {
    cout << i << "\n";
}
```

The three parts are **start** (`int i = 0`), **keep going while** (`i < n`) and **step**
(`i++`). This prints `0` up to `n - 1`: exactly `n` lines.

## The range-based for loop

To visit every element of a container, C++ has a shorter form:

```cpp
vector<int> v = {4, 8, 15};
for (int x : v) {
    cout << x << "\n";
}
```

`x` is a **copy** of each element. Write `for (int &x : v)` to change the elements
themselves.

## The while loop

Use `while` when you repeat until a condition fails and the count is not known.

```cpp
int n = 1234, digits = 0;
while (n > 0) {
    n /= 10;
    digits++;
}
// digits is now 4
```

The condition is checked **before** every repetition, so the body may run zero times.
`do { ... } while (cond);` checks after, so it runs at least once.

## Reading until the input ends

`while (cin >> x)` keeps reading while there is input and stops at the end of it. This is
useful when the problem does not tell you how many numbers follow.

## break and continue

`break` leaves the loop at once; `continue` skips to the next repetition.

## Worked example

Read `n`, then `n` numbers, and print their sum and the largest one.

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long sum = 0;
    int largest = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
        if (i == 0 || x > largest) {
            largest = x;
        }
    }
    cout << sum << " " << largest << "\n";
    return 0;
}
```

Input `4` then `3 -1 9 2` prints `13 9`. The largest starts from the first number, so a
list of only negative numbers still works.

## Common mistakes

- **Off by one.** `i <= n` starting from 0 runs `n + 1` times.
- **A loop that never ends**, because nothing in the body moves the condition.
- **Not resetting** a counter at the start of each outer repetition.
- **A semicolon after the header**: `for (...);` repeats nothing.
- **Changing a vector's size while looping over it** with a range-based for.

## Remember

`for` when you know the count, `while` when you wait for a condition, range-based `for`
to visit every element. Check the first and last repetition on a tiny input.
