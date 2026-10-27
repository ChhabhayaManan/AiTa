# Basics and input/output in Python

Every Python program you write here does three things: **read** input from the keyboard
(standard input), **work** on it, and **print** an answer (standard output). The tests type
the input for you and compare what you print, character by character.

## The smallest complete program

```python
print("Hello")
```

There is no `main` to write and nothing to include. Python runs the file from top to
bottom. `print` adds a newline at the end for you.

## Values and types

Python works out the type from the value. You do not declare it.

| Type | Holds | Example |
|---|---|---|
| `int` | whole numbers of **any** size | `count = 5` |
| `float` | numbers with a fraction | `avg = 2.5` |
| `str` | text | `name = "Asha"` |
| `bool` | `True` or `False` | `done = False` |

`int` never overflows: `2 ** 100` is exact.

## Reading input

`input()` reads **one line** and always gives back a **string**. Convert it yourself:

```python
n = int(input())                       # one number on a line
a, b = map(int, input().split())       # two numbers on one line
nums = list(map(int, input().split())) # all numbers on a line, as a list
word = input().strip()                 # a line of text, spaces at the ends removed
```

`split()` cuts the line at spaces; `map(int, ...)` turns each piece into a number.

## Printing

```python
print(a + b)
print(a, b)                 # 3 8: print puts a space between values
print(a, b, sep=",")        # 3,8
print(f"{7 / 2:.2f}")       # 3.50: an f-string with two decimals
print(*nums)                # every element of a list, separated by spaces
```

## Two kinds of division

- `/` always gives a `float`: `7 / 2` is `3.5`, and even `6 / 2` is `3.0`.
- `//` gives the whole-number part: `7 // 2` is `3`. `%` gives the remainder: `7 % 2` is `1`.

## Worked example

Read two numbers and print their sum, then the quotient and remainder.

```python
a, b = map(int, input().split())
print(a + b)
print(a // b, a % b)
```

Input `17 5` prints `22`, then `3 2`.

## Fast input for big inputs

`input()` is slow for 100 000 lines. Read everything at once instead:

```python
import sys
data = sys.stdin.read().split()
```

`data` is then a list of every word in the input, in order.

## Common mistakes

- **Forgetting to convert.** `input() + input()` joins two strings: `"3" + "8"` is `"38"`.
- **`/` when the answer must be whole.** `print(7 / 1)` prints `7.0`, not `7`. Use `//`.
- **Reading numbers on one line with `int(input())`**, which fails on `"3 8"`. Split first.
- **Extra text in the output.** Print exactly what the problem asks.

## Remember

`input()` gives a string: convert with `int()` and `split()`. Use `//` for whole-number
division and `print` for output.
