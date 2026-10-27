# Searching in C

Searching means finding **where** a value is in a collection, or learning that it is not
there. Two methods cover most problems: linear search and binary search.

## Linear search

Look at every element in order until you find the value.

```c
int linear_search(int a[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (a[i] == target) {
            return i;      /* found: its index */
        }
    }
    return -1;             /* not found */
}
```

It works on **any** array, sorted or not. In the worst case it checks all `n` elements, so
it takes time proportional to `n`.

## Binary search

If the array is **sorted**, you can do much better. Look at the middle element:

- if it is the target, you are done;
- if the target is smaller, it can only be in the left half;
- if larger, only in the right half.

Each step throws away half of what is left, so even a million elements need only about
20 steps.

```c
int binary_search(int a[], int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

- `lo + (hi - lo) / 2` finds the middle without the overflow that `(lo + hi) / 2` can
  cause for huge indexes.
- The loop runs while `lo <= hi`: a range with one element still has to be checked.
- `lo = mid + 1` and `hi = mid - 1` skip `mid`, which was already checked; without the
  `+ 1` / `- 1` the loop can get stuck forever.

## Why binary search needs sorted data

The rule "smaller means left" is only true when the array is sorted. On unsorted data,
binary search throws away the half that may contain the target and wrongly answers "not
found".

## Worked example

Read `n` sorted numbers, then `q` queries; for each query print `YES` if it is present.

```c
#include <stdio.h>

int a[100000];

int main(void) {
    int n, q;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    scanf("%d", &q);
    while (q--) {
        int x, lo = 0, hi = n - 1, found = 0;
        scanf("%d", &x);
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == x) { found = 1; break; }
            if (a[mid] < x) lo = mid + 1; else hi = mid - 1;
        }
        printf(found ? "YES\n" : "NO\n");
    }
    return 0;
}
```

The large array is declared outside `main`, because big local arrays can overflow the stack.

## Common mistakes

- **Binary search on unsorted input.**
- **`lo < hi` instead of `lo <= hi`**, which misses the last remaining element.
- **`lo = mid` or `hi = mid`**, which can loop forever.
- **Returning too early** from a linear search: `return -1` inside the loop's `else`
  gives up after checking only the first element.

## Remember

Linear search works everywhere and checks up to `n` items. Binary search needs sorted
data and halves the range each step.
