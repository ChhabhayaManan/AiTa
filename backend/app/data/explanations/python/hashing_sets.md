# Hashing, sets and dictionaries in Python

Many problems ask "have I seen this before?" or "how many times does each value appear?"
Checking every earlier element takes about `n × n` steps. Python's `set` and `dict` are
**hash tables**: they answer in about one step by turning each value into a position with
a **hash function**.

## set: have I seen it?

```python
seen = set()
seen.add(42)
print(42 in seen)    # True, in about one step
seen.discard(42)
```

A set keeps each value **once**. `set(nums)` removes duplicates, and `len(set(nums))` counts
distinct values. Sets also support `a | b` (union), `a & b` (intersection) and `a - b`.

Compare: `42 in some_list` checks every element; `42 in some_set` does not.

## dict: a value for each key

```python
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq["apple"])
```

- `d[key]` raises **KeyError** if the key is missing; `d.get(key, default)` does not.
- `collections.Counter(words)` counts everything in one line.
- `collections.defaultdict(int)` starts every missing key at 0.

## What can be a key

Keys and set elements must be **hashable**, which in practice means immutable: numbers,
strings, tuples. A list cannot be a key (its contents could change and its hash with them);
use `tuple(lst)` instead.

## How hashing works

The hash function turns a value into a number that picks a slot in an internal table.
Different values can land in the same slot; this is a **collision**, and the table resolves
it by probing for another slot. As long as values spread out, add and lookup take about one
step on average.

## Order

A `set` has **no** reliable order: printing it can show the elements in any order. A `dict`
does keep **insertion order** (since Python 3.7), but that is the order you added keys, not
sorted order. Use `sorted(d)` when you need the keys sorted.

## Worked example

Read `n` numbers and print the first number that appears twice, or `-1` if none does.

```python
n = int(input())
nums = list(map(int, input().split()))
seen = set()
answer = -1
for x in nums:
    if x in seen:
        answer = x
        break
    seen.add(x)
print(answer)
```

Input `6` then `4 7 2 7 4 9` prints `7`: it is the first value seen a second time.

## Common mistakes

- **Using a list for membership tests** inside a loop.
- **`d[key]` on a missing key.** Use `get`, `Counter` or `defaultdict`.
- **Printing a set and expecting sorted output.** Use `sorted(s)`.
- **Using a list as a key.** Convert it to a tuple.

## Remember

`set` answers "seen it?" and `dict` stores a value per key, both in about one step. Keys
must be immutable, sets have no order, and dicts keep insertion order only.
