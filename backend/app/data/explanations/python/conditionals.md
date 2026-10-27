# Conditionals in Python

A conditional lets your program **choose**: do one thing when something is true, and
something else when it is not.

## if, elif, else

```python
if marks >= 90:
    print("A")
elif marks >= 75:
    print("B")
else:
    print("C")
```

- The condition ends with a colon `:`.
- The block below it is **indented** (4 spaces). The indentation is what tells Python which
  lines belong to the `if`; there are no braces.
- Python checks from top to bottom and runs **only the first block whose condition is
  true**. So `marks >= 75` here really means "at least 75 and below 90".

## Conditions

| Operator | Meaning |
|---|---|
| `==` `!=` | equal, not equal |
| `<` `<=` `>` `>=` | comparisons |
| `and` | both must be true |
| `or` | at least one must be true |
| `not` | the opposite |
| `in` | is it inside? `"a" in word`, `x in nums` |

Comparisons can be chained: `0 <= x < 10` means `0 <= x and x < 10`.

`and` and `or` stop as soon as the answer is known (short-circuit evaluation), so in
`b != 0 and a / b > 2` the division is skipped when `b` is 0.

## Truthy and falsy

In a condition, `0`, `0.0`, `""` (empty string), `[]` (empty list) and `None` count as
false; almost everything else counts as true. `if nums:` means "if the list is not empty".

## The conditional expression

```python
print("even" if x % 2 == 0 else "odd")
```

## Worked example

Read a year and print `leap` or `not leap`. A year is a leap year if it divides by 4,
except century years, which must also divide by 400.

```python
y = int(input())
if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
    print("leap")
else:
    print("not leap")
```

`2024` prints `leap`, `1900` prints `not leap`, `2000` prints `leap`.

## Common mistakes

- **`=` instead of `==`.** In an `if`, `=` is a syntax error; compare with `==`.
- **Wrong indentation**, which puts a line inside or outside the block by accident.
- **Strictest check last.** If `marks >= 50` comes first, nobody reaches the A branch.
- **Separate `if`s for exclusive cases.** Both can run; use `elif`.
- **Comparing a string with a number.** `input()` gives text, so `"5" == 5` is `False`.

## Remember

Colon, then an indented block. Conditions are checked in order and the first true one
wins. Use `and`, `or`, `not`, and always cover the "none of these" case with `else`.
