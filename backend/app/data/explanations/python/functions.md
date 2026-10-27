# Functions in Python

A function is a **named piece of code** you can call whenever you need it. It takes
parameters, does some work, and can return a value. Write a step once, test it, reuse it.

## Defining and calling

```python
def square(x):
    return x * x

print(square(7))   # 49
```

- `def`, the name, the parameters in brackets, a colon, then an indented body.
- `return` hands a value back and ends the function.
- A function with no `return` gives back `None`.
- You can return several values at once: `return lo, hi`, then `a, b = f()`.

## Default and keyword arguments

```python
def greet(name="friend"):
    print("Hello", name)

greet()            # Hello friend
greet(name="Asha") # Hello Asha
```

## How arguments are passed

Python passes a **reference to the object**, not a copy. What happens next depends on the
object:

- Numbers, strings and tuples are **immutable**: they cannot be changed. Assigning a new
  value to the parameter only changes the function's local name.

  ```python
  def add_one(x):
      x = x + 1      # a new int, local to the function

  n = 5
  add_one(n)         # n is still 5
  ```

- Lists, dicts and sets are **mutable**. Changing them **through** the parameter changes
  the caller's object, because both names refer to the same list.

  ```python
  def add_item(items):
      items.append(99)

  nums = [1, 2]
  add_item(nums)     # nums is now [1, 2, 99]
  ```

To get a changed number back, **return** it: `n = add_one(n)`.

## Local and global names

Names created inside a function are **local**: they disappear when it returns. A function
can read a global variable, but assigning to it inside the function creates a new local
name instead, unless you write `global name`. Passing values in and returning them out is
clearer than using globals.

## Worked example

Read two numbers and print them swapped.

```python
def swapped(a, b):
    return b, a

x, y = map(int, input().split())
x, y = swapped(x, y)
print(x, y)
```

Input `3 8` prints `8 3`. Python can also swap directly with `x, y = y, x`.

## A trap: mutable default arguments

`def add(item, bucket=[]):` creates the list **once**, when the function is defined, so
every call shares it. Use `bucket=None` and create the list inside.

## Common mistakes

- **Expecting a number parameter to change the caller's variable.** Return the new value.
- **Changing a list the caller still needs** without meaning to. Copy it with `items[:]`.
- **Printing instead of returning**: the caller gets `None`.
- **Calling a function before its `def` line has run.**

## Remember

`def` and an indented body, `return` to give values back. Immutable values cannot be
changed by a function; mutable ones like lists can, because the function sees the same
object.
