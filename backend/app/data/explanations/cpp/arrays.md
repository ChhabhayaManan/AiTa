# Arrays and vectors in C++

An array is **a row of boxes of the same type**, stored next to each other, reached by
position (the **index**). In C++ you will mostly use `vector`, an array that knows its own
size and can grow.

## vector: the array you should reach for

```cpp
#include <vector>

vector<int> marks = {70, 82, 91, 64, 88};
cout << marks[0] << "\n";        // 70: indexes start at 0
cout << marks.size() << "\n";    // 5
marks.push_back(77);             // add at the end; size is now 6
```

- Indexes run from **0 to size − 1**.
- `vector<int> a(n);` makes `n` elements, all set to 0. `vector<int> a(n, -1);` sets
  them to −1.
- `a.size()` gives the length, so you never have to pass it separately.
- `a.back()` is the last element, `a.pop_back()` removes it.

## Reading n numbers

```cpp
int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; i++) {
    cin >> a[i];
}
```

## Plain arrays

C++ still has C-style arrays: `int a[5] = {1, 2, 3};` (the rest become 0). Their size is
fixed, they do not know their length, and when passed to a function they turn into a
pointer to the first element. A vector avoids all three problems.

## No bounds checking with []

`a[i]` does **not** check that `i` is valid. `a[n]` or `a[-1]` reads or writes whatever
memory is there: wrong answers, changed variables, or a crash. `a.at(i)` does check and
throws an error instead, which helps while debugging.

## A 2D grid

```cpp
vector<vector<int>> grid(rows, vector<int>(cols, 0));
grid[r][c] = 1;
```

## Passing to functions

A vector passed **by value** is copied in full. Pass it by reference instead:
`void fill(vector<int> &a)` to change it, `int total(const vector<int> &a)` to only read it.

## Worked example

Read `n` numbers and print them in reverse order.

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    for (int i = n - 1; i >= 0; i--) {
        cout << a[i] << (i > 0 ? " " : "\n");
    }
    return 0;
}
```

Input `4` then `1 2 3 4` prints `4 3 2 1`. `for (int &x : a)` reads straight into each
element because `x` is a reference.

## Common mistakes

- **`i <= n`** touches `a[n]`, one past the end.
- **Indexing an empty vector**: `vector<int> a; a[0] = 5;` writes outside it. Use
  `push_back`, or create it with a size first.
- **Comparing `int` with `a.size()`** when `a` is empty: `a.size() - 1` is a huge unsigned
  number, not −1.
- **Copying big vectors** into functions by value.

## Remember

Prefer `vector`: it knows its size and can grow. Indexes go from 0 to size − 1, and `[]`
never checks them for you.
