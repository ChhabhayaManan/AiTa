# Stacks and queues in C++

Stacks and queues **hold items until you need them**, with a rule about which item comes
out next.

- A **stack** is a pile of plates: add on top, take from the top.
  **Last in, first out** (LIFO).
- A **queue** is a line at a counter: join at the back, leave from the front.
  **First in, first out** (FIFO).

## std::stack

```cpp
#include <stack>

stack<int> st;
st.push(3);
st.push(7);
cout << st.top() << "\n";   // 7: the last one pushed
st.pop();                   // removes 7 (pop returns nothing)
cout << st.size() << "\n";  // 1
```

## std::queue

```cpp
#include <queue>

queue<int> q;
q.push(3);
q.push(7);
cout << q.front() << "\n";  // 3: the first one pushed
q.pop();                    // removes 3
```

`deque` (double-ended queue) allows adding and removing at **both** ends:
`push_front`, `push_back`, `pop_front`, `pop_back`.

## Check before you take

`top()`, `front()` and `pop()` on an **empty** stack or queue are undefined behaviour:
the program may crash or return garbage. Always check `empty()` first.

## When to use which

- **Stack**: matching things in reverse order or undoing steps. Balanced brackets,
  evaluating expressions, the history of a back button, the function call stack itself.
- **Queue**: handling things in the order they arrived. Customers waiting, tasks to run,
  visiting a grid level by level (breadth-first search).

## Worked example

Read a string of brackets and print `YES` if every bracket is closed in the right order.

```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    stack<char> st;
    bool ok = true;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            char want = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (st.empty() || st.top() != want) { ok = false; break; }
            st.pop();
        }
    }
    cout << (ok && st.empty() ? "YES" : "NO") << "\n";
    return 0;
}
```

`([]{})` prints `YES`. `([)]` prints `NO`: when `)` arrives, the top of the stack is `[`.
The most recently opened bracket must close first, which is the LIFO rule.

## Priority queue

`priority_queue<int>` is a different idea: `top()` always gives the **largest** item,
whatever the order of insertion. Use `priority_queue<int, vector<int>, greater<int>>` for
the smallest. It is not first-in-first-out.

## Common mistakes

- **`top()` or `pop()` on an empty container.**
- **Expecting `pop()` to return the item.** Read `top()` / `front()` first, then `pop()`.
- **Forgetting the final empty check** (for `((`, no step fails, but brackets are left open).
- **Using a stack where order of arrival matters**, or the other way round.

## Remember

`stack`: push, top, pop, last in first out. `queue`: push, front, pop, first in first out.
Check `empty()` before you look or remove.
