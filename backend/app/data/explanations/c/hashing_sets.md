# Hashing and sets in C

Many problems ask "have I seen this before?" or "how many times does each value appear?"
Checking every earlier element each time takes about `n × n` steps. **Hashing** answers
in about one step by turning the value itself into an array index.

## The simplest hash: a counting array

When the values are small whole numbers, use them directly as indexes.

```c
int count[1001] = {0};       /* values are between 0 and 1000 */
for (int i = 0; i < n; i++) {
    count[a[i]]++;
}
/* count[v] is how many times v appeared */
```

The same idea works for letters: `count[c - 'a']` for lowercase letters 0 to 25.

A **set** only needs to know yes or no, so use `0` and `1`: `seen[v] = 1;` and later
`if (seen[v])`.

## When values are too big for an array

If values go up to 10⁹, an array of that size does not fit in memory. A **hash table**
squeezes them into a small array:

1. A **hash function** maps the value to a slot, for example
   `slot = (unsigned)x % SIZE`.
2. Two different values can land in the same slot. This is a **collision**, and it is
   normal.
3. One simple fix is **linear probing**: if the slot is taken by a different value, try
   the next slot, and the next, until you find the value or an empty slot.

```c
#define SIZE 262144            /* more than twice the number of values */
long long keys[SIZE];
char used[SIZE];

int insert(long long x) {      /* returns 1 if x is new */
    unsigned h = (unsigned)((x % SIZE + SIZE) % SIZE);
    while (used[h] && keys[h] != x) {
        h = (h + 1) % SIZE;
    }
    if (used[h]) return 0;
    used[h] = 1;
    keys[h] = x;
    return 1;
}
```

`(x % SIZE + SIZE) % SIZE` keeps the slot non-negative even when `x` is negative.

## Why order is lost

A hash table places values by their hash, not by when they arrived or by size. Walking
through the table gives the values in slot order, which looks random. If the output must
be in input order, walk the **input** again and look each value up.

## Worked example

Read `n` numbers between 1 and 1000 and print the first number that appears twice, or
`-1` if none does.

```c
#include <stdio.h>

int main(void) {
    int n, seen[1001] = {0}, answer = -1;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        if (answer == -1 && seen[x]) answer = x;
        seen[x] = 1;
    }
    printf("%d\n", answer);
    return 0;
}
```

Input `6` then `4 7 2 7 4 9` prints `7`.

## Common mistakes

- **Index out of range**: a value of 1000 needs an array of size 1001.
- **Negative values as indexes**: shift them first (`count[x + OFFSET]`).
- **Forgetting to reset** the counting array between test cases.
- **A table that is too full**: linear probing gets slow as the table fills; keep it less
  than half full.

## Remember

Hashing turns a value into an index, so lookups take about one step. Small values: a
counting array. Big values: a hash table that handles collisions. Either way, order is not
kept.
