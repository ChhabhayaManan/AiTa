# Searching in C++

Searching means finding **where** a value is, or learning that it is not there. Two
methods cover most problems: linear search and binary search.

## Linear search

Check every element in order.

```cpp
int linear_search(const vector<int> &a, int target) {
    for (int i = 0; i < (int)a.size(); i++) {
        if (a[i] == target) return i;
    }
    return -1;
}
```

It works on **any** data, sorted or not, and checks up to `n` elements. The standard
library version is `find(a.begin(), a.end(), target)`, which returns an iterator (equal to
`a.end()` when not found).

## Binary search

On **sorted** data, look at the middle element. If the target is smaller, it can only be in
the left half; if larger, only in the right half. Each step halves what is left, so a
million elements need about 20 steps.

```cpp
int binary_search_index(const vector<int> &a, int target) {
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

- `lo + (hi - lo) / 2` avoids the overflow `(lo + hi) / 2` can cause.
- `while (lo <= hi)`: a range of one element still has to be checked.
- `mid + 1` and `mid - 1` skip the element already checked; without them the loop can
  run forever.

## The standard library does it for you

On a sorted vector (needs `<algorithm>`):

| Call | Gives |
|---|---|
| `binary_search(a.begin(), a.end(), x)` | `true` if `x` is present |
| `lower_bound(a.begin(), a.end(), x)` | first position with value `>= x` |
| `upper_bound(a.begin(), a.end(), x)` | first position with value `> x` |

Subtract `a.begin()` to turn a position into an index. `upper_bound - lower_bound` counts
how many times `x` appears.

## Why binary search needs sorted data

"Smaller means go left" is only true when the data is sorted. On unsorted data the search
can throw away the half that holds the target and wrongly report "not found".

## Worked example

Read `n` sorted numbers, then `q` queries; for each, print `YES` if it is present.

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    cin >> q;
    while (q--) {
        int x;
        cin >> x;
        cout << (binary_search(a.begin(), a.end(), x) ? "YES" : "NO") << "\n";
    }
    return 0;
}
```

## Common mistakes

- **Binary search on unsorted data.** Sort first, or use linear search.
- **`lo < hi` instead of `lo <= hi`**, missing the last element.
- **`lo = mid` / `hi = mid`**, which can loop forever.
- **Forgetting that `lower_bound` may return `end()`** when every value is smaller.

## Remember

Linear search works on anything and checks up to `n` items. Binary search needs sorted
data and halves the range each step; prefer the library's `lower_bound` and friends.
