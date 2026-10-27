# Basics and input/output in C

Every C program you write here does three things: **read** some numbers or text from the
keyboard (standard input), **work** on them, and **print** an answer (standard output).
The tests type the input for you and compare what you print, character by character.

## The smallest complete program

```c
#include <stdio.h>

int main(void) {
    printf("Hello\n");
    return 0;
}
```

- `#include <stdio.h>` brings in `printf` and `scanf`. Without it, the compiler does not
  know these functions.
- `main` is where the program starts. `return 0;` tells the system it finished normally.
- `\n` is a newline. Most answers must end with one.

## Variables and types

A variable is a named box in memory. In C you must say what kind of value it holds:

| Type | Holds | Example |
|---|---|---|
| `int` | whole numbers, about ±2 billion | `int count = 5;` |
| `long long` | bigger whole numbers | `long long total = 0;` |
| `double` | numbers with a fraction | `double avg = 2.5;` |
| `char` | one character | `char grade = 'A';` |

## Reading input with scanf

`scanf` reads text and stores it **into** your variables, so it needs their addresses.
That is what the `&` means: "the address of".

```c
int a, b;
scanf("%d %d", &a, &b);   /* reads two whole numbers */
```

| Format | Type |
|---|---|
| `%d` | `int` |
| `%lld` | `long long` |
| `%lf` | `double` (in scanf) |
| `%c` | `char` |
| `%s` | a word into a `char` array (no `&`) |

## Printing with printf

```c
printf("%d\n", a + b);        /* a whole number */
printf("%.2f\n", 7.0 / 2);    /* 3.50: two digits after the point */
```

## Worked example

Read two numbers and print their sum, their quotient and the remainder.

```c
#include <stdio.h>

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d\n", a + b);
    printf("%d %d\n", a / b, a % b);
    return 0;
}
```

Input `17 5` prints `22`, then `3 2`. Dividing two `int`s throws the fraction away
(`17 / 5` is `3`), and `%` gives what is left over (`17 % 5` is `2`).

## Common mistakes

- **Forgetting `&` in scanf.** `scanf("%d", x)` writes to a random address and usually
  crashes. Write `scanf("%d", &x)`.
- **Integer division by surprise.** `7 / 2` is `3`. If you need `3.5`, make one side a
  `double`: `7.0 / 2` or `(double)a / b`.
- **Overflow.** `int` cannot hold 10 000 000 000. Use `long long` and `%lld`.
- **Extra text in the output.** Printing `Sum: 22` when the test expects `22` fails.
  Print exactly what is asked.

## Remember

Read with `scanf` and `&`, compute, print with `printf` and a newline. Match the format
code to the type every time.
