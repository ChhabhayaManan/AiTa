# Sorting in Python

Sorting puts elements **in order**, usually smallest first. Once data is sorted, the
smallest and largest sit at the ends, equal values sit together, and binary search works.

## sorted and list.sort

```python
nums = [4, 1, 5, 2, 3]
print(sorted(nums))   # [1, 2, 3, 4, 5]: a NEW list; nums is unchanged
nums.sort()           # sorts nums itself, in place; returns None
nums.sort(reverse=True)
```

Both take about `n log n` steps, fast enough for millions of elements.

- `sorted(x)` works on any sequence (lists, strings, tuples) and returns a new list.
- `x.sort()` only exists on lists, changes the list, and returns **None**. Writing
  `nums = nums.sort()` loses your list.

## Sorting by a key

Pass `key=`, a function that turns each element into the value to compare:

```python
words.sort(key=len)                         # shortest word first
people.sort(key=lambda p: p[1])             # by the second field
people.sort(key=lambda p: (-p[1], p[0]))    # score high to low, then name A to Z
```

Tuples compare field by field, so a key that returns a tuple sorts by the first field and
breaks ties with the next. A minus sign reverses one numeric field without reversing the
others.

## Sorting is stable

Python's sort is **stable**: elements with equal keys keep their original order. That lets
you sort in steps: sort by the less important field first, then by the more important one.

## How sorting works underneath

Simple sorts like **insertion sort** (slide each element left until it fits) or **bubble
sort** (swap neighbours that are out of order) take about `n × n` steps: fine for a few
hundred elements, far too slow for 100 000. Python's built-in sort (Timsort) is much
faster, so use it unless the problem asks you to write a sort yourself.

```python
def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
```

## Worked example

Read `n` numbers and print them in increasing order.

```python
n = int(input())
nums = list(map(int, input().split()))
print(*sorted(nums))
```

Input `5` then `4 1 5 2 3` prints `1 2 3 4 5`.

## Sorting numbers read as text

`sorted(["10", "9", "100"])` gives `['10', '100', '9']`: strings compare character by
character. Convert to `int` first, or use `key=int`.

## Common mistakes

- **`nums = nums.sort()`**, which sets `nums` to `None`.
- **Sorting strings of digits** instead of numbers.
- **Using `sort()` when the original order is still needed.** Use `sorted()`.
- **Writing an `n × n` sort** for large inputs.

## Remember

`sorted()` returns a new list, `.sort()` changes the list and returns `None`. Use `key=` to
choose what to compare, and rely on the sort being stable for ties.
