# Stacks and queues in Python

Stacks and queues **hold items until you need them**, with a rule about which item comes
out next.

- A **stack** is a pile of plates: add on top, take from the top.
  **Last in, first out** (LIFO).
- A **queue** is a line at a counter: join at the back, leave from the front.
  **First in, first out** (FIFO).

## A stack is a list

```python
stack = []
stack.append(3)     # push
stack.append(7)
print(stack[-1])    # 7: peek at the top
stack.pop()         # removes and returns 7
print(len(stack))   # 1
```

`append` and `pop()` at the end of a list are fast. `pop()` on an empty list raises
**IndexError**, so check `if stack:` first.

## A queue is a deque

Removing from the **front** of a list (`pop(0)`) shifts every other element, so it is slow
for long queues. Use `collections.deque`, which is fast at both ends:

```python
from collections import deque

q = deque()
q.append(3)          # join at the back
q.append(7)
print(q[0])          # 3: the front
q.popleft()          # removes and returns 3
```

`appendleft` and `pop` also exist, so a deque can work as a stack, a queue, or both.

## When to use which

- **Stack**: matching things in reverse order or undoing steps. Balanced brackets,
  evaluating expressions, a back button, the function call stack itself.
- **Queue**: handling things in arrival order. Customers waiting, tasks to run, visiting a
  grid level by level (breadth-first search).

## Worked example

Read a string of brackets and print `YES` if every bracket is closed in the right order.

```python
s = input().strip()
pairs = {")": "(", "]": "[", "}": "{"}
stack = []
ok = True
for ch in s:
    if ch in "([{":
        stack.append(ch)
    elif not stack or stack.pop() != pairs[ch]:
        ok = False
        break
print("YES" if ok and not stack else "NO")
```

`([]{})` prints `YES`. `([)]` prints `NO`: when `)` arrives, the top of the stack is `[`.
The most recently opened bracket must close first, which is the LIFO rule.

## Priority queue

`heapq` gives a different idea: `heapq.heappop(h)` always removes the **smallest** item,
whatever the order of insertion. For the largest, push negated values. It is not
first-in-first-out.

## Common mistakes

- **`pop()` on an empty stack** or `popleft()` on an empty deque.
- **`list.pop(0)` as a queue** on large inputs: slow.
- **Forgetting the final empty check** (for `((`, no step fails, but brackets are left
  open).
- **Peeking with `stack[0]`**, which is the bottom, not the top.

## Remember

Stack: a list with `append`, `pop()` and `[-1]`. Queue: a `deque` with `append` and
`popleft()`. Check for empty before you take an item.
