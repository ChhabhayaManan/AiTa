# Functions in C

A function is a **named piece of code** you can call whenever you need it. It takes
inputs (parameters), does some work, and can give back one value (the return value).
Functions let you write a step once, test it, and reuse it.

## Defining and calling a function

```c
#include <stdio.h>

int square(int x) {
    return x * x;
}

int main(void) {
    printf("%d\n", square(7));   /* 49 */
    return 0;
}
```

- `int` before the name is the **return type**: the kind of value it gives back.
- `int x` is a **parameter**: a local variable that receives the value you pass in.
- `return` ends the function and hands the value back to the caller.
- A function that gives nothing back has return type `void`.

## Declare before use

C reads your file from top to bottom. If `main` calls `square` and `square` is written
**below** `main`, add a **prototype** above `main` so the compiler knows it exists:

```c
int square(int x);   /* prototype */
```

## Pass by value

C copies the argument into the parameter. Changing the parameter does **not** change the
caller's variable:

```c
void add_one(int x) { x = x + 1; }

int n = 5;
add_one(n);      /* n is still 5 */
```

## Changing the caller's variable with a pointer

To let a function change a variable, pass its **address** and work through a pointer:

```c
void add_one(int *p) { *p = *p + 1; }

int n = 5;
add_one(&n);     /* n is now 6 */
```

`&n` is the address of `n`; `*p` means "the variable `p` points to". This is also how a
function can hand back two results, and it is why `scanf` needs `&`.

## Worked example

Read two numbers and print them swapped.

```c
#include <stdio.h>

void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int main(void) {
    int x, y;
    scanf("%d %d", &x, &y);
    swap(&x, &y);
    printf("%d %d\n", x, y);
    return 0;
}
```

Input `3 8` prints `8 3`. A `swap(int a, int b)` without pointers would only swap the
copies and print `3 8`.

## Common mistakes

- **Expecting a value parameter to change the caller's variable.** Use a pointer.
- **Forgetting to return.** A non-void function that reaches its end without `return`
  gives back garbage.
- **Printing instead of returning.** If the caller needs the value, `return` it; printing
  inside the function also adds output the tests did not ask for.
- **Calling before declaring.** Add a prototype or define the function above `main`.

## Remember

Parameters are copies. Return one value with `return`; change the caller's variables
through pointers.
