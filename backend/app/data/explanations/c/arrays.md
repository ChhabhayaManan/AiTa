# Arrays in C

An array is **a row of boxes of the same type**, stored next to each other in memory, all
under one name. You reach a box by its position, called the **index**.

## Declaring and using an array

```c
int marks[5] = {70, 82, 91, 64, 88};
printf("%d\n", marks[0]);   /* 70: the first box */
printf("%d\n", marks[4]);   /* 88: the last box */
marks[2] = 95;              /* change the third box */
```

- Indexes start at **0**. An array of size 5 has indexes 0 to 4.
- The size is fixed when the array is created.
- `int a[5];` without `= {...}` holds **garbage** until you fill it. `int a[5] = {0};`
  sets every box to 0.

## Reading n numbers into an array

```c
int n;
scanf("%d", &n);
int a[1000];
for (int i = 0; i < n; i++) {
    scanf("%d", &a[i]);
}
```

Make the array as big as the largest `n` the problem allows.

## Why indexes start at 0

The array name stands for the address of the first box. `a[i]` means "start at `a` and
move `i` boxes along". The first box is zero steps away, so it is `a[0]`. This is also why
`a[i]` and `*(a + i)` mean the same thing.

## No bounds checking

C does **not** stop you from writing `a[5]` in an array of 5, or `a[-1]`. It simply reads
or writes whatever memory sits there. The program may print nonsense, change another
variable, or crash with a segmentation fault. Keeping every index between 0 and size − 1
is your job.

## Arrays and functions

When you pass an array to a function, C passes the **address of its first element**, not
a copy. The function can change the caller's array, and it cannot find out the size on its
own, so pass the size too:

```c
int total(int a[], int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}
```

## Worked example

Read `n` numbers and print them in reverse order.

```c
#include <stdio.h>

int main(void) {
    int n, a[1000];
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = n - 1; i >= 0; i--) {
        printf("%d", a[i]);
        printf(i > 0 ? " " : "\n");
    }
    return 0;
}
```

Input `4` then `1 2 3 4` prints `4 3 2 1`.

## Common mistakes

- **`i <= n` in the loop.** That touches `a[n]`, one past the end.
- **Using values before setting them.** A fresh local array is garbage.
- **Array too small** for the largest input in the constraints.
- **`sizeof(a)` inside a function** gives the size of a pointer, not of the array.

## Remember

Indexes run from 0 to size − 1, C never checks them for you, and a function receives the
array's address, so pass the length alongside it.
