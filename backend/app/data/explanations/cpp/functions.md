# Functions in C++

A function is a **named piece of code** you can call whenever you need it. It takes
parameters, does some work, and can return one value. Write a step once, test it, reuse it.

## Defining and calling a function

```cpp
#include <iostream>
using namespace std;

int square(int x) {
    return x * x;
}

int main() {
    cout << square(7) << "\n";   // 49
    return 0;
}
```

- `int` before the name is the **return type**; `void` means nothing is returned.
- `int x` is a **parameter**, a local variable that receives the argument.
- `return` hands the value back and ends the function.
- A function must be **declared before it is used**: define it above `main`, or put a
  prototype like `int square(int x);` there.

## Three ways to pass a parameter

```cpp
void by_value(int x)        { x++; }   // gets a copy
void by_reference(int &x)   { x++; }   // works on the caller's variable
void by_const_ref(const string &s) { cout << s.size(); }  // no copy, cannot change it
```

```cpp
int n = 5;
by_value(n);       // n is still 5
by_reference(n);   // n is now 6
```

- **By value** copies the argument. Safe, but copying a big `vector` or `string` is slow.
- **By reference** (`&`) gives the function another name for the caller's variable, so
  changes are visible outside. Use it when the function must change the argument.
- **By const reference** (`const T &`) avoids the copy and promises not to change it.
  Use it for large inputs you only read.

A pointer (`int *p` with `*p` and `&n`) can also change the caller's variable, as in C, but
in C++ a reference is simpler and cannot be null.

## Overloading and default arguments

Two functions may share a name if their parameter types differ:
`int area(int s)` and `int area(int w, int h)`. A parameter can also have a default:
`void greet(string name = "friend")`.

## Worked example

Read two numbers and print them swapped.

```cpp
#include <iostream>
using namespace std;

void swap_values(int &a, int &b) {
    int t = a;
    a = b;
    b = t;
}

int main() {
    int x, y;
    cin >> x >> y;
    swap_values(x, y);
    cout << x << " " << y << "\n";
    return 0;
}
```

Input `3 8` prints `8 3`. Without the `&`, only the copies would be swapped and it would
print `3 8`. (The standard library already has `std::swap`, which does the same.)

## Common mistakes

- **Expecting a by-value parameter to change the caller's variable.** Add `&`.
- **Passing big containers by value** in a function called many times. Use `const &`.
- **Forgetting `return`** in a non-void function.
- **Printing instead of returning** a value the caller needs.
- **Returning a reference to a local variable**, which no longer exists after the
  function ends.

## Remember

By value copies, by reference shares, by const reference shares read-only. Return one
value with `return`; change arguments through references.
