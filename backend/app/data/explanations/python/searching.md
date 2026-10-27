# Searching in Python

Searching means finding **where** a value is, or learning that it is not there. Two
methods cover most problems: linear search and binary search.

## Linear search

Check every element in order.

```python
def linear_search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

It works on any list, sorted or not, and checks up to `n` elements. `target in nums` and
`nums.index(target)` are linear searches too, so they are slow inside a big loop.

## Binary search

On **sorted** data, look at the middle element. If the target is smaller, it can only be in
the left half; if larger, only in the right half. Each step halves what is left, so a
million elements need about 20 steps.

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

- `while lo <= hi`: a range of one element still has to be checked.
- `mid + 1` and `mid - 1` skip the element already checked; without them the loop can run
  forever.
- Python integers never overflow, so `(lo + hi) // 2` is safe here.

## The bisect module

On a sorted list, `bisect` does the search for you:

| Call | Gives |
|---|---|
| `bisect_left(nums, x)` | first index with value `>= x` |
| `bisect_right(nums, x)` | first index with value `> x` |

`x` is present when `i = bisect_left(nums, x)` gives `i < len(nums) and nums[i] == x`, and
`bisect_right - bisect_left` counts how many times it appears.

## Why binary search needs sorted data

"Smaller means go left" is only true when the list is sorted. On unsorted data the search
can throw away the half holding the target and wrongly report "not found".

## Worked example

Read `n` sorted numbers, then `q` queries; for each, print `YES` if it is present.

```python
import sys
from bisect import bisect_left

data = sys.stdin.read().split()
n = int(data[0])
nums = list(map(int, data[1:1 + n]))
q = int(data[1 + n])
out = []
for x in map(int, data[2 + n:2 + n + q]):
    i = bisect_left(nums, x)
    out.append("YES" if i < n and nums[i] == x else "NO")
print("\n".join(out))
```

For many queries, a `set` (see hashing) also answers "is it present?" in about one step.

## Common mistakes

- **Binary search on unsorted data.** Sort first.
- **`lo < hi` instead of `lo <= hi`**, missing the last element.
- **`lo = mid` / `hi = mid`**, which can loop forever.
- **`x in nums` inside a loop** over a big list: that is `n × q` steps.
- **Using `bisect_left`'s index without checking** that it is in range and equals `x`.

## Remember

Linear search works on anything and checks up to `n` items. Binary search needs sorted
data and halves the range each step; `bisect` does it for you.
