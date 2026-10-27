# Sorting in C++

Sorting puts elements **in order**, usually smallest first. Once data is sorted, the
smallest and largest sit at the ends, equal values sit together, and binary search works.

## std::sort

`<algorithm>` has `sort`, which takes about `n log n` steps, fast enough for millions of
elements.

```cpp
#include <algorithm>

vector<int> a = {4, 1, 5, 2, 3};
sort(a.begin(), a.end());                    // 1 2 3 4 5
sort(a.begin(), a.end(), greater<int>());    // 5 4 3 2 1
```

`begin()` and `end()` mark the range to sort. `sort` works **in place**: the original
order is lost, so copy the vector first if you still need it.

## Your own order: a comparator

Pass a function (often a lambda) that answers "should `x` come **before** `y`?":

```cpp
// by length, shorter words first
sort(words.begin(), words.end(), [](const string &x, const string &y) {
    return x.size() < y.size();
});
```

The comparator must be a **strict** order: it returns `false` when the two are equal.
Writing `<=` breaks that rule and can crash or give a wrong order.

To break ties, compare a second field:

```cpp
// by score high to low, then by name A to Z
sort(people.begin(), people.end(), [](const Person &x, const Person &y) {
    if (x.score != y.score) return x.score > y.score;
    return x.name < y.name;
});
```

Pairs and tuples already compare field by field, so `sort` on `vector<pair<int,int>>` orders
by `first`, then by `second`.

## Stable sorting

`stable_sort` keeps equal elements in their original order; `sort` does not promise to.
Use `stable_sort` when the order of ties must follow the input.

## How sorting works underneath

Simple sorts like **insertion sort** (slide each element left until it fits) or **bubble
sort** (swap neighbours that are out of order) take about `n × n` steps. That is fine for a
few hundred elements and far too slow for 100 000. `std::sort` uses a smarter method, so
use it unless the problem asks you to write a sort yourself.

## Worked example

Read `n` numbers and print them in increasing order.

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    sort(a.begin(), a.end());
    for (int i = 0; i < n; i++) {
        cout << a[i] << (i + 1 < n ? " " : "\n");
    }
    return 0;
}
```

Input `5` then `4 1 5 2 3` prints `1 2 3 4 5`.

## Common mistakes

- **`<=` in a comparator** instead of `<`.
- **Sorting when the original order is still needed**: copy first.
- **Writing an `n × n` sort** for large inputs.
- **Sorting only part of the range** by passing the wrong end, such as
  `a.begin() + n - 1`.

## Remember

`sort(a.begin(), a.end())` sorts in place in `n log n`. A comparator returns whether the
first argument comes first and must return `false` for equal elements.
