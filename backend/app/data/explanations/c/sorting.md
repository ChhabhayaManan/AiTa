# Sorting in C

Sorting puts elements **in order**, usually smallest first. Many problems become easy once
the data is sorted: the smallest and largest are at the ends, duplicates sit next to each
other, and binary search becomes possible.

## A simple sort you can write yourself: insertion sort

Think of sorting playing cards in your hand. Take each new card and slide it left until
the card before it is not bigger.

```c
void insertion_sort(int a[], int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];   /* shift the bigger one right */
            j--;
        }
        a[j + 1] = key;
    }
}
```

After step `i`, the first `i + 1` elements are sorted. It is easy to get right, but for
`n` elements it can take about `n × n` steps. For 100 000 numbers that is far too slow.

## Bubble sort and selection sort

- **Bubble sort** swaps neighbours that are out of order, pass after pass.
- **Selection sort** finds the smallest remaining element and puts it next.

Both also take about `n × n` steps. They are worth knowing, not worth using on big inputs.

## The fast way: qsort

`<stdlib.h>` has `qsort`, which sorts in about `n log n` steps. You give it a
**comparison function** that says which of two elements comes first:

```c
#include <stdlib.h>

int cmp_int(const void *x, const void *y) {
    int a = *(const int *)x;
    int b = *(const int *)y;
    return (a > b) - (a < b);   /* negative, 0 or positive */
}

qsort(a, n, sizeof a[0], cmp_int);
```

- The function receives **pointers** to two elements, as `const void *`, so it casts them
  back to `int *` first.
- It returns a negative number if the first should come first, positive if the second
  should, and 0 if they are equal.
- `return a - b;` looks shorter but can overflow for values near ±2 billion and give the
  wrong order. `(a > b) - (a < b)` is always safe.
- To sort largest first, swap the roles: `(a < b) - (a > b)`.

`qsort` sorts the array **in place**: the original order is gone. Copy the array first if
you still need it.

## Worked example

Read `n` numbers and print them in increasing order.

```c
#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

int a[100000];

int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    qsort(a, n, sizeof a[0], cmp_int);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 < n ? ' ' : '\n');
    return 0;
}
```

Input `5` then `4 1 5 2 3` prints `1 2 3 4 5`.

## Stable sorting

A sort is **stable** if equal elements keep their original order. Insertion sort is
stable; `qsort` is not guaranteed to be. When you sort records by one field and the order
of ties matters, compare a second field too.

## Common mistakes

- **`n × n` sorts on large inputs** cause a time limit failure.
- **`return a - b;` in the comparator** overflows on extreme values.
- **Comparing the pointers** instead of the values they point to.
- **Wrong size** in `qsort`: use `sizeof a[0]`, the size of one element.

## Remember

Write insertion sort to understand sorting, use `qsort` with a safe comparator for real
input sizes, and remember it changes the array in place.
