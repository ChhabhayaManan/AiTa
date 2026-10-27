# Hashing and sets in C++

Many problems ask "have I seen this before?" or "how many times does each value appear?"
Checking every earlier element takes about `n × n` steps. A **hash table** answers in about
one step by turning each value into a position with a **hash function**.

## unordered_set: have I seen it?

```cpp
#include <unordered_set>

unordered_set<int> seen;
seen.insert(42);
if (seen.count(42)) { /* present */ }
seen.erase(42);
```

A set keeps each value **once**: inserting 42 twice still leaves one 42.

## unordered_map: how many times?

```cpp
#include <unordered_map>

unordered_map<string, int> freq;
freq["apple"]++;          // a missing key starts at 0
freq["apple"]++;
cout << freq["apple"];    // 2
```

Careful: `freq[key]` **creates** the key if it is missing. To only check, use
`freq.count(key)` or `freq.find(key) != freq.end()`.

## How hashing works

The hash function turns a value into a number, which picks a **bucket** in an internal
array. Different values can land in the same bucket; this is a **collision**, and the table
handles it by keeping a small list per bucket. As long as values spread out, insert and
lookup take about one step on average.

## Order is not kept

`unordered_set` and `unordered_map` store values by their hash, so looping over them gives
an order that looks random and can change between compilers. If you must print in input
order, loop over the **input** again and look each value up. If you need sorted order, use
`set` and `map` instead: they keep keys sorted, at a cost of about `log n` steps per
operation.

## A plain array is often enough

When values are small whole numbers, a counting array is the fastest hash of all:
`vector<int> count(1001, 0); count[x]++;`. For lowercase letters use `count[c - 'a']`.

## Worked example

Read `n` numbers and print the first number that appears twice, or `-1` if none does.

```cpp
#include <iostream>
#include <unordered_set>
using namespace std;

int main() {
    int n;
    cin >> n;
    unordered_set<long long> seen;
    long long answer = -1;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if (answer == -1 && seen.count(x)) answer = x;
        seen.insert(x);
    }
    cout << answer << "\n";
    return 0;
}
```

Input `6` then `4 7 2 7 4 9` prints `7`: it is the first value seen a second time.

## Common mistakes

- **`map[key]` to test membership**, which silently inserts the key.
- **Relying on the iteration order** of an unordered container.
- **Forgetting to clear** the set between test cases.
- **Using `set`/`map` when order is not needed**, which is slower than the unordered ones.

## Remember

`unordered_set` answers "seen it?", `unordered_map` counts and stores values per key, both
in about one step. Neither keeps any order; use `set`/`map` when you need sorted keys.
