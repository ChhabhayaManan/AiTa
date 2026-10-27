# Stacks and queues in C

Stacks and queues are ways of **holding items until you need them**, with a rule about
which item comes out next.

- A **stack** is like a pile of plates: you add on top and take from the top.
  **Last in, first out** (LIFO).
- A **queue** is like a line at a counter: you join at the back and leave from the front.
  **First in, first out** (FIFO).

C has no built-in stack or queue, but an array and one or two index variables are all you
need.

## A stack with an array

```c
int stack[100000];
int top = 0;                 /* number of items; next free slot */

void push(int x) { stack[top++] = x; }
int  pop(void)   { return stack[--top]; }
int  peek(void)  { return stack[top - 1]; }
int  empty(void) { return top == 0; }
```

Always check `empty()` before `pop` or `peek`. Popping an empty stack reads `stack[-1]`,
which is outside the array.

## A queue with an array

```c
int queue[100000];
int head = 0, tail = 0;      /* items live in queue[head .. tail-1] */

void enqueue(int x) { queue[tail++] = x; }
int  dequeue(void)  { return queue[head++]; }
int  size(void)     { return tail - head; }
```

`head` moves forward as items leave, so the front of the array is never reused. That is
fine when the total number of items is known. For an endless stream, use a **circular
queue**: wrap the indexes around with `% capacity`.

## When to use which

- **Stack**: anything that must be undone or matched in reverse order. Balanced brackets,
  undo history, evaluating expressions, the call stack itself.
- **Queue**: anything handled in arrival order. Tasks waiting to be served, visiting a grid
  level by level (breadth-first search).

## Worked example

Read a string of brackets and print `YES` if every bracket is closed in the right order.

```c
#include <stdio.h>

char st[100001];

int main(void) {
    char s[100001];
    scanf("%100000s", s);
    int top = 0, ok = 1;
    for (int i = 0; s[i] != '\0' && ok; i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            st[top++] = c;
        } else {
            char want = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (top == 0 || st[top - 1] != want) ok = 0;
            else top--;
        }
    }
    printf(ok && top == 0 ? "YES\n" : "NO\n");
    return 0;
}
```

`([]{})` prints `YES`. `([)]` prints `NO`: when `)` arrives, the top of the stack is `[`.
The most recent opening bracket must close first, which is exactly the LIFO rule.

## Common mistakes

- **Popping an empty stack** or dequeuing an empty queue.
- **Forgetting the final check** that the stack is empty (for `((` every step looks fine).
- **Mixing up `top++` and `++top`**: decide whether `top` is the count or the last index,
  and stick to it.
- **Queue indexes running past the array** when items keep arriving; use a circular queue.

## Remember

Stack: last in, first out, one index. Queue: first in, first out, two indexes. Check for
empty before taking an item out.
