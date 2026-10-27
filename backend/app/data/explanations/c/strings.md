# Strings in C

C has no separate string type. A string is a **`char` array that ends with a special
character `'\0'`** (the null character, value 0). Every string function finds the end of
the text by looking for that `'\0'`.

## Storing a string

```c
char name[20] = "Asha";
```

In memory this is `'A' 's' 'h' 'a' '\0'` followed by unused boxes. The text has 4
characters but needs **5** boxes. Always leave room for the `'\0'`.

## Reading and printing

```c
char word[101];
scanf("%100s", word);        /* one word, no spaces; no & for arrays */
printf("%s\n", word);
```

`%s` stops at the first space. To read a whole line, including spaces, use `fgets`:

```c
char line[201];
fgets(line, sizeof line, stdin);   /* keeps the '\n' at the end */
```

## Walking through the characters

```c
int len = 0;
while (word[len] != '\0') {
    len++;
}
```

This is what `strlen` from `<string.h>` does. Characters are small numbers, so you can
compare and do arithmetic: `c >= 'a' && c <= 'z'` checks for a lowercase letter, and
`c - 'a'` gives its position in the alphabet (0 to 25).

## Useful functions from string.h

| Function | Does |
|---|---|
| `strlen(s)` | length, not counting `'\0'` |
| `strcpy(dst, src)` | copy `src` into `dst` |
| `strcmp(a, b)` | 0 if equal, negative or positive otherwise |
| `strcat(dst, src)` | add `src` to the end of `dst` |

You **cannot** compare strings with `==` (that compares addresses) or copy with `=`.

## Literals are read-only

`char *p = "hello";` points to text the compiler may store in read-only memory. Writing
`p[0] = 'H';` is undefined and often crashes. If you need to change the text, copy it into
an array: `char s[] = "hello"; s[0] = 'H';` is fine.

## Worked example

Read a word and print how many vowels it has.

```c
#include <stdio.h>

int main(void) {
    char w[1001];
    scanf("%1000s", w);
    int count = 0;
    for (int i = 0; w[i] != '\0'; i++) {
        char c = w[i];
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
    }
    printf("%d\n", count);
    return 0;
}
```

Input `programming` prints `3`.

## Common mistakes

- **No room for `'\0'`.** A 5-letter word needs `char w[6]`.
- **`==` or `=` on strings.** Use `strcmp` and `strcpy`.
- **Calling `strlen` in the loop condition** of a long string recomputes the length every
  time. Store it once.
- **Forgetting the `'\n'` that `fgets` keeps.**

## Remember

A C string is characters plus a `'\0'` terminator. Size the array for it, walk until you
reach it, and use the `string.h` functions to compare and copy.
