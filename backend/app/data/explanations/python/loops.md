# Loops in Python

A loop **repeats** a block of code. You need one whenever the amount of work depends on
the input: add up `n` numbers, print a pattern, keep going until something happens.

## for with range

```python
for i in range(n):
    print(i)
```

`range(n)` gives `0, 1, ..., n - 1`: exactly `n` values. Other forms:

| Code | Gives |
|---|---|
| `range(1, n + 1)` | 1 up to `n` |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(n - 1, -1, -1)` | `n - 1` down to 0 |

The end value is never included.

## for over a collection

A `for` loop can visit the items of a list or the characters of a string directly:

```python
for x in [4, 8, 15]:
    print(x)
for ch in "abc":
    print(ch)
for i, x in enumerate(nums):   # index and value together
    print(i, x)
```

## while

Use `while` when you repeat until a condition fails and do not know the count in advance.

```python
n, digits = 1234, 0
while n > 0:
    n //= 10
    digits += 1
# digits is now 4
```

Python has no `i++`; write `i += 1`.

## break, continue and else

`break` leaves the loop at once; `continue` skips to the next repetition. A loop can have an
`else` block that runs only if the loop finished **without** a `break`, which is handy for
"searched everything and did not find it".

## Worked example

Read `n`, then `n` numbers on one line, and print their sum and the largest one.

```python
n = int(input())
nums = list(map(int, input().split()))
total = 0
largest = nums[0]
for x in nums:
    total += x
    if x > largest:
        largest = x
print(total, largest)
```

Input `4` then `3 -1 9 2` prints `13 9`. Starting `largest` at the first number, not 0,
makes a list of only negative numbers work. (`sum(nums)` and `max(nums)` do the same job
in one call each.)

## Common mistakes

- **Off by one with range.** `range(1, n)` stops at `n - 1`. Check the last value.
- **A `while` that never ends**, because nothing in the body changes the condition.
- **Changing a list while looping over it**: removing items skips some. Loop over a copy,
  or build a new list.
- **Wrong indentation**, which moves a line in or out of the loop.
- **Building a string with `+=` in a big loop.** Collect pieces in a list and use
  `" ".join(pieces)`.

## Remember

`for` with `range` when you know the count, `for x in items` to visit everything, `while`
when you wait for a condition. The end of a `range` is never included.
