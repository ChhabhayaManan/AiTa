# Basics and input/output in C++

Every C++ program you write here does three things: **read** input from the keyboard
(standard input), **work** on it, and **print** an answer (standard output). The tests type
the input for you and compare what you print, character by character.

## The smallest complete program

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello" << "\n";
    return 0;
}
```

- `#include <iostream>` brings in `cin` and `cout`.
- `using namespace std;` lets you write `cout` instead of `std::cout`.
- `main` is where the program starts; `return 0;` means it finished normally.
- `"\n"` ends the line. Most answers must end with one.

## Variables and types

| Type | Holds | Example |
|---|---|---|
| `int` | whole numbers, about ±2 billion | `int count = 5;` |
| `long long` | bigger whole numbers | `long long total = 0;` |
| `double` | numbers with a fraction | `double avg = 2.5;` |
| `char` | one character | `char grade = 'A';` |
| `string` | text (needs `<string>`) | `string name = "Asha";` |
| `bool` | `true` or `false` | `bool done = false;` |

## Reading with cin

`cin >> x` skips spaces and newlines, then reads one value into `x`. The type of `x`
decides how the text is read, so there are no format codes to get wrong.

```cpp
int a, b;
cin >> a >> b;        // two whole numbers, on one line or two
string word;
cin >> word;          // one word, stops at a space
```

To read a whole line with spaces, use `getline(cin, line);`.

## Printing with cout

```cpp
cout << a + b << "\n";
cout << fixed << setprecision(2) << 7.0 / 2 << "\n";   // 3.50, needs <iomanip>
```

## Worked example

Read two numbers and print their sum, their quotient and the remainder.

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << "\n";
    cout << a / b << " " << a % b << "\n";
    return 0;
}
```

Input `17 5` prints `22`, then `3 2`. Dividing two `int`s drops the fraction (`17 / 5` is
`3`); `%` gives the remainder (`17 % 5` is `2`).

## Fast input for big inputs

With 100 000 numbers or more, add these two lines at the start of `main`:

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

They stop `cin` from synchronising with C's `scanf`, which makes reading several times
faster. After this, do not mix `cin` with `scanf` in the same program.

## Common mistakes

- **Integer division by surprise.** `7 / 2` is `3`. Write `7.0 / 2` or
  `(double)a / b` for `3.5`.
- **Overflow.** `int` cannot hold 10 000 000 000; use `long long`.
- **Mixing `cin >>` and `getline`.** `cin >> n` leaves the newline behind, so the next
  `getline` reads an empty line. Call `cin.ignore();` in between.
- **Extra text in the output.** Print exactly what the problem asks.
- **`endl` in a big loop.** It flushes every time and is slow; use `"\n"`.

## Remember

Read with `cin >>`, compute, print with `cout <<` and `"\n"`. Pick the type that fits the
size of the values.
