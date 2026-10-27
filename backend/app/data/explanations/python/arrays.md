# Lists (arrays) in Python

Python's array is the **list**: an ordered row of values, reached by position (the
**index**). A list knows its length and can grow and shrink.

## Making and using a list

```python
marks = [70, 82, 91, 64, 88]
print(marks[0])     # 70: indexes start at 0
print(marks[-1])    # 88: negative indexes count from the end
print(len(marks))   # 5
marks.append(77)    # add at the end
marks[2] = 95       # change one element
```

- Indexes run from **0 to len − 1**, or from −1 (last) to −len (first).
- An index outside that range raises **IndexError** instead of reading random memory.
- `[0] * n` makes a list of `n` zeros.

## Reading numbers into a list

```python
n = int(input())
nums = list(map(int, input().split()))
```

## Slicing

`nums[a:b]` gives a **new list** from index `a` up to, but not including, `b`.

| Code | Gives |
|---|---|
| `nums[1:4]` | elements 1, 2, 3 |
| `nums[:3]` | the first three |
| `nums[-2:]` | the last two |
| `nums[::-1]` | a reversed copy |

## Useful operations

| Code | Does | Cost |
|---|---|---|
| `nums.append(x)` | add at the end | fast |
| `nums.pop()` | remove and return the last | fast |
| `nums.pop(0)`, `nums.insert(0, x)` | at the front | slow: shifts every element |
| `x in nums` | is `x` present? | checks every element |
| `sum(nums)`, `max(nums)`, `min(nums)` | totals and extremes | one pass |

## Copies and shared lists

`b = a` does **not** copy: `a` and `b` are two names for the same list, so changing one
changes the other. Use `b = a[:]` or `b = list(a)` for a copy.

The same trap appears in grids: `[[0] * m] * n` makes `n` references to **one** row. Build
a grid with `[[0] * m for _ in range(n)]`.

## Worked example

Read `n` numbers and print them in reverse order.

```python
n = int(input())
nums = list(map(int, input().split()))
print(*nums[::-1])
```

Input `4` then `1 2 3 4` prints `4 3 2 1`. `*` spreads the list into separate values for
`print`.

## Common mistakes

- **`b = a` and expecting a copy.**
- **`[[0] * m] * n`** for a grid: every row is the same row.
- **`range(len(nums) + 1)`** in a loop over indexes, which reaches one past the end.
- **`pop(0)` in a big loop**: each call is slow. Use `collections.deque` for a queue.

## Remember

Lists start at index 0, negative indexes count from the end, slices make copies, and
`b = a` does not.
