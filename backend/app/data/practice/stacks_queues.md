# Stacks & Queues

=== PROBLEM ===
ID: aita-remove-adjacent
DIFFICULTY: medium
STATEMENT: A single line contains a string of lowercase letters. Repeatedly remove any two neighbouring letters that are equal, until no such pair is left. Print what remains, or EMPTY if nothing remains.
CONSTRAINTS: The string has between 1 and 500 lowercase letters.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    stack = []
    for ch in data[k]:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    print("".join(stack) if stack else "EMPTY")
```
TESTS:
### input
abbaca
### output
ca
### input
aabb
### output
EMPTY
### input
abc
### output
abc
### input
a
### output
a
### input
azxxzy
### output
ay
### input
abccba
### output
EMPTY
=== END ===

=== PROBLEM ===
ID: aita-postfix
DIFFICULTY: medium
STATEMENT: A single line contains an expression in postfix notation: single-digit numbers and the operators +, - and *, separated by single spaces. Each operator applies to the two values before it. Print the value of the expression.
CONSTRAINTS: The line has between 1 and 99 tokens and the expression is valid; every intermediate value fits in a 32-bit integer.
REFERENCE:
```python
import sys

lines = sys.stdin.read().split("\n")
t = int(lines[0])
for k in range(1, t + 1):
    stack = []
    for token in lines[k].split():
        if token in "+-*":
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b if token == "+" else a - b if token == "-" else a * b)
        else:
            stack.append(int(token))
    print(stack[-1])
```
TESTS:
### input
2 3 +
### output
5
### input
5 1 2 + 4 * + 3 -
### output
14
### input
7
### output
7
### input
9 3 -
### output
6
### input
2 3 4 * +
### output
14
### input
1 2 - 3 *
### output
-3
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int stack[5];
    int top = 0;
    stack[top++] = 1;
    stack[top++] = 2;
    stack[top++] = 3;
    top--;
    printf("%d %d\n", stack[top - 1], top);
    return 0;
}
```
OPTIONS:
A) 3 3 || none
B) 2 2 || correct
C) 1 2 || none
D) 3 2 || none
EXPLANATION: Three pushes leave top at 3; popping lowers it to 2, so the top of the stack is now the 2.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int q[5];
    int head = 0, tail = 0;
    q[tail++] = 4;
    q[tail++] = 7;
    q[tail++] = 9;
    head++;
    printf("%d %d\n", q[head], tail - head);
    return 0;
}
```
OPTIONS:
A) 9 2 || none
B) 4 3 || none
C) 7 2 || correct
D) 7 3 || none
EXPLANATION: A queue removes from the front: head moves past the 4, leaving 7 at the front and two values waiting.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "abc";
    char st[4];
    int top = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        st[top++] = s[i];
    }
    while (top > 0) {
        putchar(st[--top]);
    }
    putchar('\n');
    return 0;
}
```
OPTIONS:
A) abc || none
B) cba || correct
C) bca || none
D) cab || none
EXPLANATION: The last character pushed is the first one popped, so a stack reverses the order.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "(()(";
    int depth = 0, deepest = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '(') {
            depth++;
            if (depth > deepest) {
                deepest = depth;
            }
        } else {
            depth--;
        }
    }
    printf("%d %d\n", depth, deepest);
    return 0;
}
```
OPTIONS:
A) 0 2 || none
B) 2 3 || none
C) 1 2 || none
D) 2 2 || correct
EXPLANATION: depth goes 1, 2, 1, 2, so two brackets are still open at the end and the deepest point was 2.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
A circular queue stores its values in an array of size 4. What does this program print?
```c
#include <stdio.h>

int main(void) {
    int capacity = 4;
    int tail = 3;
    tail = (tail + 1) % capacity;
    printf("%d\n", tail);
    return 0;
}
```
OPTIONS:
A) 4 || index_out_of_range
B) 3 || none
C) 0 || correct
D) 1 || none
EXPLANATION: % wraps the index back to the start of the array once it passes the last slot.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int st[10];
    int top = 0;
    st[top++] = 1;
    st[top++] = 2;
    int x = st[--top];
    st[top++] = 3;
    st[top++] = x * 10;
    int y = st[--top];
    printf("%d %d %d\n", x, y, st[top - 1]);
    return 0;
}
```
OPTIONS:
A) 2 20 3 || correct
B) 1 10 3 || none
C) 2 20 1 || none
D) 2 3 20 || none
EXPLANATION: x pops the 2; then 3 and 20 are pushed and y pops the 20, leaving 3 on top of the 1.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> s;
    s.push(1);
    s.push(2);
    s.push(3);
    s.pop();
    cout << s.top() << s.size() << endl;
    return 0;
}
```
OPTIONS:
A) 33 || none
B) 12 || none
C) 22 || correct
D) 32 || none
EXPLANATION: pop removes the last value pushed, 3, so the top is 2 and two values remain.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    q.pop();
    cout << q.front() << q.back() << endl;
    return 0;
}
```
OPTIONS:
A) 23 || correct
B) 12 || none
C) 13 || none
D) 32 || none
EXPLANATION: A queue removes from the front, so after one pop 2 is at the front and 3 is still at the back.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <deque>
#include <iostream>
using namespace std;

int main() {
    deque<int> d = {1, 2, 3};
    d.push_front(0);
    d.pop_back();
    for (int x : d) {
        cout << x;
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 123 || none
B) 0123 || none
C) 123 0 || none
D) 012 || correct
EXPLANATION: A deque can add and remove at both ends: 0 goes on the front and 3 comes off the back.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    stack<char> st;
    for (char c : string("hello")) {
        st.push(c);
    }
    string out;
    while (!st.empty()) {
        out += st.top();
        st.pop();
    }
    cout << out << endl;
    return 0;
}
```
OPTIONS:
A) hello || none
B) olleh || correct
C) h || none
D) o || none
EXPLANATION: Popping a stack until it is empty gives the values back in reverse order.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    for (int i = 1; i <= 5; i++) {
        q.push(i);
    }
    int sum = 0;
    while (q.size() > 2) {
        sum += q.front();
        q.pop();
    }
    cout << sum << " " << q.front() << endl;
    return 0;
}
```
OPTIONS:
A) 9 4 || none
B) 6 3 || off_by_one
C) 6 4 || correct
D) 12 1 || none
EXPLANATION: Values leave from the front: 1, 2 and 3 are removed (sum 6), leaving 4 and 5.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    priority_queue<int> pq;
    pq.push(5);
    pq.push(1);
    pq.push(8);
    pq.push(3);
    pq.pop();
    cout << pq.top() << pq.size() << endl;
    return 0;
}
```
OPTIONS:
A) 33 || none
B) 83 || none
C) 13 || none
D) 53 || correct
EXPLANATION: A priority_queue always gives out its largest value first; pop removes the 8, leaving 5 on top and three values.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
stack = [1, 2]
stack.append(3)
stack.pop()
print(stack)
```
OPTIONS:
A) [2, 3] || none
B) [1, 2] || correct
C) [1, 2, 3] || none
D) [3] || none
EXPLANATION: append pushes on the end and pop() removes from the end, so the 3 that was just pushed comes straight back off.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)
q.popleft()
print(list(q))
```
OPTIONS:
A) [1, 2, 3] || none
B) [2, 3, 4] || correct
C) [1, 2, 3, 4] || none
D) [4, 2, 3] || none
EXPLANATION: A queue adds at the back and removes from the front, so the 1 leaves and the 4 joins at the end.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
stack = []
for ch in "ab)c)":
    if ch == ")":
        stack.pop()
    else:
        stack.append(ch)
print("".join(stack))
```
OPTIONS:
A) a || correct
B) ac || none
C) abc || none
D) b || none
EXPLANATION: The stack goes a, ab, a (the first ")" pops b), ac, and the second ")" pops c, leaving a.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
The values 1, 2 and 3 are pushed onto an empty stack in that order. Which value comes off first?
OPTIONS:
A) 1 || none
B) 2 || none
C) 3 || correct
D) All three come off at once || none
EXPLANATION: A stack is last in, first out: the most recently pushed value is removed first.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
Documents sent to a shared printer must be printed in the order they arrived. Which data structure fits best?
OPTIONS:
A) A stack, because the newest document should print first || none
B) A queue, because the first document in should be the first one out || correct
C) A sorted array, ordered by document size || none
D) A set, so duplicate documents are dropped || none
EXPLANATION: A queue is first in, first out, which is exactly a waiting line.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Why is a stack the natural tool for checking whether brackets like ( [ { } ] ) are balanced?
OPTIONS:
A) The bracket opened most recently is the one that must be closed next || correct
B) A stack keeps the brackets sorted || none
C) A stack can hold only brackets || none
D) A stack removes duplicate brackets automatically || none
EXPLANATION: Each closing bracket must match the latest unmatched opening one, which is exactly what sits on top of the stack.
=== END ===

=== DEBUG ===
PROBLEM: dsa-valid-parentheses
LANGUAGE: python
BUG: empty_input_unhandled
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    ok = True
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack[-1] != pairs[ch]:
                ok = False
                break
            stack.pop()
    if stack:
        ok = False
    print("YES" if ok else "NO")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    ok = True
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if stack[-1] != pairs[ch]:
                ok = False
                break
            stack.pop()
    if stack:
        ok = False
    print("YES" if ok else "NO")
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-valid-parentheses
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[256];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        char stack[256] = {0};
        int top = 0;
        int ok = 1;
        for (int i = 0; line[i] != '\0'; i++) {
            char c = line[i];
            if (c == '(' || c == '[' || c == '{') {
                stack[top++] = c;
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (top == 0 || stack[top - 1] != open) {
                    ok = 0;
                    break;
                }
                top--;
            }
        }
        if (top != 0) {
            ok = 0;
        }
        printf("%s\n", ok ? "YES" : "NO");
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[256];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        char stack[256] = {0};
        int top = 0;
        int ok = 1;
        for (int i = 0; line[i] != '\0'; i++) {
            char c = line[i];
            if (c == '(' || c == '[' || c == '{') {
                stack[top++] = c;
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (top == 0 || stack[top] != open) {
                    ok = 0;
                    break;
                }
                top--;
            }
        }
        if (top != 0) {
            ok = 0;
        }
        printf("%s\n", ok ? "YES" : "NO");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-valid-parentheses
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string s;
        getline(cin, s);
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (st.empty() || st.top() != open) {
                    ok = false;
                    break;
                }
                st.pop();
            }
        }
        if (!st.empty()) {
            ok = false;
        }
        cout << (ok ? "YES" : "NO") << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string s;
        getline(cin, s);
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (st.empty() || st.top() == open) {
                    ok = false;
                    break;
                }
                st.pop();
            }
        }
        if (!st.empty()) {
            ok = false;
        }
        cout << (ok ? "YES" : "NO") << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-remove-adjacent
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    print("".join(stack) if stack else "EMPTY")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    stack = []
    for ch in s:
        if stack and stack[-1] != ch:
            stack.pop()
        else:
            stack.append(ch)
    print("".join(stack) if stack else "EMPTY")
```
=== END ===

=== DEBUG ===
PROBLEM: aita-remove-adjacent
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[600];
        char stack[600];
        int top = 0;
        scanf("%s", s);
        for (int i = 0; s[i] != '\0'; i++) {
            if (top > 0 && stack[top - 1] == s[i]) {
                top--;
            } else {
                stack[top++] = s[i];
            }
        }
        if (top == 0) {
            printf("EMPTY\n");
        } else {
            for (int i = 0; i < top; i++) {
                putchar(stack[i]);
            }
            putchar('\n');
        }
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[600];
        char stack[600];
        int top = 0;
        scanf("%s", s);
        for (int i = 0; s[i] != '\0'; i++) {
            if (top > 0 && stack[top - 1] == s[i]) {
                top--;
            } else {
                stack[top++] = s[i];
            }
        }
        if (top == 0) {
            printf("EMPTY\n");
        } else {
            for (int i = 1; i < top; i++) {
                putchar(stack[i]);
            }
            putchar('\n');
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-remove-adjacent
LANGUAGE: cpp
BUG: empty_input_unhandled
CORRECT:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        string st;
        for (char c : s) {
            if (!st.empty() && st.back() == c) {
                st.pop_back();
            } else {
                st.push_back(c);
            }
        }
        cout << (st.empty() ? "EMPTY" : st) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        string st;
        for (char c : s) {
            if (!st.empty() && st.back() == c) {
                st.pop_back();
            } else {
                st.push_back(c);
            }
        }
        cout << st << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-postfix
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def evaluate(expression):
    stack = []
    for token in expression.split():
        if token in "+-*":
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            else:
                stack.append(a * b)
        else:
            stack.append(int(token))
    return stack[-1]


t = int(input())
for _ in range(t):
    print(evaluate(input()))
```
BUGGY:
```python
def evaluate(expression):
    stack = []
    for token in expression.split():
        if token in "+-*":
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            else:
                stack.append(a * b)
        else:
            stack.append(int(token))
    print(stack[-1])


t = int(input())
for _ in range(t):
    print(evaluate(input()))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-postfix
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[256];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        int stack[128];
        int top = 0;
        for (int i = 0; line[i] != '\0'; i++) {
            char c = line[i];
            if (c >= '0' && c <= '9') {
                stack[top++] = c - '0';
            } else if (c == '+' || c == '-' || c == '*') {
                int b = stack[--top];
                int a = stack[--top];
                if (c == '+') {
                    stack[top++] = a + b;
                } else if (c == '-') {
                    stack[top++] = a - b;
                } else {
                    stack[top++] = a * b;
                }
            }
        }
        printf("%d\n", stack[top - 1]);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[256];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        int stack[128];
        int top = 0;
        for (int i = 0; line[i] != '\0'; i++) {
            char c = line[i];
            if (c >= '0' && c <= '9') {
                stack[top++] = c - '1';
            } else if (c == '+' || c == '-' || c == '*') {
                int b = stack[--top];
                int a = stack[--top];
                if (c == '+') {
                    stack[top++] = a + b;
                } else if (c == '-') {
                    stack[top++] = a - b;
                } else {
                    stack[top++] = a * b;
                }
            }
        }
        printf("%d\n", stack[top - 1]);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-postfix
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string line;
        getline(cin, line);
        stack<int> st;
        for (char c : line) {
            if (c >= '0' && c <= '9') {
                st.push(c - '0');
            } else if (c == '+' || c == '-' || c == '*') {
                int b = st.top();
                st.pop();
                int a = st.top();
                st.pop();
                if (c == '+') {
                    st.push(a + b);
                } else if (c == '-') {
                    st.push(a - b);
                } else {
                    st.push(a * b);
                }
            }
        }
        cout << st.top() << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string line;
        getline(cin, line);
        stack<int> st;
        for (char c : line) {
            if (c >= '0' && c < '9') {
                st.push(c - '0');
            } else if (c == '+' || c == '-' || c == '*') {
                int b = st.top();
                st.pop();
                int a = st.top();
                st.pop();
                if (c == '+') {
                    st.push(a + b);
                } else if (c == '-') {
                    st.push(a - b);
                } else {
                    st.push(a * b);
                }
            }
        }
        cout << st.top() << endl;
    }
    return 0;
}
```
=== END ===

=== PROBLEM ===
ID: aita-stk-final-stack
DIFFICULTY: easy
STATEMENT: The first line contains n, the number of commands. Each of the next n lines is either PUSH x, which puts the integer x on top of a stack, or POP, which removes the value on top. A POP on an empty stack does nothing. The stack starts empty. After all the commands, print the values left on the stack from bottom to top, separated by single spaces, or EMPTY if no values are left.
CONSTRAINTS: 1 <= n <= 10^5; -10^9 <= x <= 10^9.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    pos += 1
    stack = []
    for _ in range(n):
        command = data[pos]
        pos += 1
        if command == "PUSH":
            stack.append(int(data[pos]))
            pos += 1
        elif stack:
            stack.pop()
    print(" ".join(map(str, stack)) if stack else "EMPTY")
```
TESTS:
### input
5
PUSH 3
PUSH 8
POP
PUSH 1
PUSH 4
### output
3 1 4
### input
2
POP
POP
### output
EMPTY
### input
1
PUSH -7
### output
-7
### input
4
PUSH 1
PUSH 2
POP
POP
### output
EMPTY
### input
6
POP
PUSH 10
PUSH 20
PUSH 30
POP
PUSH 5
### output
10 20 5
### input
3
PUSH 0
PUSH 0
PUSH 1000000000
### output
0 0 1000000000
=== END ===

=== PROBLEM ===
ID: aita-stk-ticket-counter
DIFFICULTY: easy
STATEMENT: People wait in one line at a ticket counter. The first line contains n, the number of events. Each of the next n lines is either JOIN x, meaning a person holding token number x joins the back of the line, or SERVE, meaning the person at the front is served and leaves. The line starts empty. For every SERVE, output the token number of the person served, or -1 if nobody is waiting. Print all these outputs on one line, separated by single spaces.
CONSTRAINTS: 1 <= n <= 10^5; 1 <= x <= 10^9; there is at least one SERVE.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    pos += 1
    line = []
    head = 0
    served = []
    for _ in range(n):
        command = data[pos]
        pos += 1
        if command == "JOIN":
            line.append(int(data[pos]))
            pos += 1
        elif head < len(line):
            served.append(line[head])
            head += 1
        else:
            served.append(-1)
    print(" ".join(map(str, served)))
```
TESTS:
### input
6
JOIN 12
JOIN 5
SERVE
JOIN 9
SERVE
SERVE
### output
12 5 9
### input
1
SERVE
### output
-1
### input
4
JOIN 7
SERVE
SERVE
JOIN 3
### output
7 -1
### input
5
JOIN 1
JOIN 2
JOIN 3
SERVE
SERVE
### output
1 2
### input
3
SERVE
JOIN 1000000000
SERVE
### output
-1 1000000000
### input
7
JOIN 4
JOIN 4
SERVE
JOIN 8
SERVE
SERVE
SERVE
### output
4 4 8 -1
=== END ===

=== PROBLEM ===
ID: aita-stk-browser-history
DIFFICULTY: medium
STATEMENT: A web browser starts on page 1 with no history. The first line contains n, the number of commands. Each of the next n lines is one of: VISIT x, which opens page x (the current page is saved in the back history and the forward history is wiped); BACK, which returns to the most recently saved page in the back history and saves the current page in the forward history; FORWARD, which does the opposite of BACK. A BACK with an empty back history, or a FORWARD with an empty forward history, does nothing. After every command, output the page now on screen. Print all these outputs on one line, separated by single spaces.
CONSTRAINTS: 1 <= n <= 10^5; 1 <= x <= 10^9.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    pos += 1
    back, forward = [], []
    current = 1
    shown = []
    for _ in range(n):
        command = data[pos]
        pos += 1
        if command == "VISIT":
            back.append(current)
            current = int(data[pos])
            pos += 1
            forward = []
        elif command == "BACK":
            if back:
                forward.append(current)
                current = back.pop()
        elif forward:
            back.append(current)
            current = forward.pop()
        shown.append(current)
    print(" ".join(map(str, shown)))
```
TESTS:
### input
5
VISIT 4
VISIT 9
BACK
BACK
FORWARD
### output
4 9 4 1 4
### input
2
BACK
FORWARD
### output
1 1
### input
1
VISIT 7
### output
7
### input
7
VISIT 2
VISIT 3
VISIT 5
BACK
BACK
VISIT 8
FORWARD
### output
2 3 5 3 2 8 8
### input
8
VISIT 6
BACK
BACK
FORWARD
FORWARD
VISIT 2
BACK
FORWARD
### output
6 1 1 6 6 2 6 2
### input
4
VISIT 1000000000
VISIT 3
BACK
VISIT 5
### output
1000000000 3 1000000000 5
=== END ===

=== PROBLEM ===
ID: aita-stk-next-greater
DIFFICULTY: medium
STATEMENT: The first line contains n. The second line contains n positive integers. For each value, find the first value to its right that is strictly greater than it, or -1 if there is no such value. Print the n answers on one line, separated by single spaces.
CONSTRAINTS: 1 <= n <= 10^5; 1 <= each value <= 10^9.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = [int(v) for v in data[pos + 1:pos + 1 + n]]
    pos += 1 + n
    answer = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= values[i]:
            stack.pop()
        if stack:
            answer[i] = stack[-1]
        stack.append(values[i])
    print(" ".join(map(str, answer)))
```
TESTS:
### input
5
2 7 3 5 1
### output
7 -1 5 -1 -1
### input
1
42
### output
-1
### input
4
1 2 3 4
### output
2 3 4 -1
### input
4
9 6 4 1
### output
-1 -1 -1 -1
### input
6
3 3 1 3 4 4
### output
4 4 3 4 -1 -1
### input
7
5 1 1 2 1 6 2
### output
6 2 2 6 6 -1 -1
=== END ===

=== PROBLEM ===
ID: aita-stk-bracket-error
DIFFICULTY: hard
STATEMENT: A single line contains a string made only of the characters ( ) [ ] { }, with positions numbered from 1. Read it from left to right. A closing bracket is wrong if no bracket is open at that moment, or if the most recently opened bracket that is still open is of a different kind. If there is a wrong closing bracket, print the position of the first one. Otherwise, if some opening brackets are never closed, print the position of the leftmost of them. If every bracket is closed correctly, print OK.
CONSTRAINTS: The string has between 1 and 10^5 characters and contains no spaces.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
match = {")": "(", "]": "[", "}": "{"}
for k in range(1, t + 1):
    s = data[k]
    stack = []
    result = None
    for i, ch in enumerate(s, 1):
        if ch in "([{":
            stack.append((ch, i))
        elif stack and stack[-1][0] == match[ch]:
            stack.pop()
        else:
            result = i
            break
    if result is None and stack:
        result = stack[0][1]
    print("OK" if result is None else result)
```
TESTS:
### input
([]{})
### output
OK
### input
)
### output
1
### input
([)]
### output
3
### input
(()[
### output
1
### input
{}[(])
### output
5
### input
()((
### output
3
### input
[
### output
1
### input
(){}[]]
### output
7
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-ticket-counter
LANGUAGE: c
BUG: empty_input_unhandled
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int queue[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int head = 0, tail = 0;
        int printed = 0;
        for (int i = 0; i < n; i++) {
            char command[8];
            scanf("%7s", command);
            if (strcmp(command, "JOIN") == 0) {
                scanf("%d", &queue[tail]);
                tail++;
            } else {
                int served = -1;
                if (head < tail) {
                    served = queue[head++];
                }
                if (printed > 0) {
                    putchar(' ');
                }
                printf("%d", served);
                printed++;
            }
        }
        putchar('\n');
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int queue[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int head = 0, tail = 0;
        int printed = 0;
        for (int i = 0; i < n; i++) {
            char command[8];
            scanf("%7s", command);
            if (strcmp(command, "JOIN") == 0) {
                scanf("%d", &queue[tail]);
                tail++;
            } else {
                int served = queue[head++];
                if (printed > 0) {
                    putchar(' ');
                }
                printf("%d", served);
                printed++;
            }
        }
        putchar('\n');
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-next-greater
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

long long values[100000];
long long answer[100000];
long long stack[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%lld", &values[i]);
        }
        int top = 0;
        for (int i = n - 1; i >= 0; i--) {
            while (top > 0 && stack[top - 1] <= values[i]) {
                top--;
            }
            answer[i] = top > 0 ? stack[top - 1] : -1;
            stack[top++] = values[i];
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                putchar(' ');
            }
            printf("%lld", answer[i]);
        }
        putchar('\n');
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long values[100000];
long long answer[100000];
long long stack[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%lld", &values[i]);
        }
        int top = 0;
        for (int i = n - 1; i >= 0; i--) {
            while (top > 0 && stack[top - 1] < values[i]) {
                top--;
            }
            answer[i] = top > 0 ? stack[top - 1] : -1;
            stack[top++] = values[i];
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                putchar(' ');
            }
            printf("%lld", answer[i]);
        }
        putchar('\n');
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-bracket-error
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

char s[100005];
char kinds[100005];
int places[100005];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        scanf("%100004s", s);
        int top = 0;
        int wrong = -1;
        for (int i = 0; s[i] != '\0'; i++) {
            char c = s[i];
            if (c == '(' || c == '[' || c == '{') {
                kinds[top] = c;
                places[top] = i;
                top++;
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (top > 0 && kinds[top - 1] == open) {
                    top--;
                } else {
                    wrong = i;
                    break;
                }
            }
        }
        if (wrong >= 0) {
            printf("%d\n", wrong + 1);
        } else if (top > 0) {
            printf("%d\n", places[0] + 1);
        } else {
            printf("OK\n");
        }
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

char s[100005];
char kinds[100005];
int places[100005];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        scanf("%100004s", s);
        int top = 0;
        int wrong = -1;
        for (int i = 0; s[i] != '\0'; i++) {
            char c = s[i];
            if (c == '(' || c == '[' || c == '{') {
                kinds[top] = c;
                places[top] = i;
                top++;
            } else {
                char open = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (top > 0 && kinds[top - 1] == open) {
                    top--;
                } else {
                    wrong = i;
                    break;
                }
            }
        }
        if (wrong >= 0) {
            printf("%d\n", wrong);
        } else if (top > 0) {
            printf("%d\n", places[0] + 1);
        } else {
            printf("OK\n");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-final-stack
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        stack<long long> st;
        for (int i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "PUSH") {
                long long x;
                cin >> x;
                st.push(x);
            } else if (st.size() > 0) {
                st.pop();
            }
        }
        if (st.empty()) {
            cout << "EMPTY" << endl;
            continue;
        }
        stack<long long> flipped;
        while (!st.empty()) {
            flipped.push(st.top());
            st.pop();
        }
        bool first = true;
        while (!flipped.empty()) {
            cout << (first ? "" : " ") << flipped.top();
            flipped.pop();
            first = false;
        }
        cout << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        stack<long long> st;
        for (int i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "PUSH") {
                long long x;
                cin >> x;
                st.push(x);
            } else if (st.size() > 1) {
                st.pop();
            }
        }
        if (st.empty()) {
            cout << "EMPTY" << endl;
            continue;
        }
        stack<long long> flipped;
        while (!st.empty()) {
            flipped.push(st.top());
            st.pop();
        }
        bool first = true;
        while (!flipped.empty()) {
            cout << (first ? "" : " ") << flipped.top();
            flipped.pop();
            first = false;
        }
        cout << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-ticket-counter
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <iostream>
#include <queue>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        queue<long long> line;
        bool first = true;
        for (int i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "JOIN") {
                long long x;
                cin >> x;
                line.push(x);
            } else {
                long long served = -1;
                if (!line.empty()) {
                    served = line.front();
                    line.pop();
                }
                cout << (first ? "" : " ") << served;
                first = false;
            }
        }
        cout << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <queue>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        queue<long long> line;
        bool first = true;
        for (int i = 1; i < n; i++) {
            string command;
            cin >> command;
            if (command == "JOIN") {
                long long x;
                cin >> x;
                line.push(x);
            } else {
                long long served = -1;
                if (!line.empty()) {
                    served = line.front();
                    line.pop();
                }
                cout << (first ? "" : " ") << served;
                first = false;
            }
        }
        cout << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-browser-history
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        stack<long long> back_pages, next_pages;
        long long current = 1;
        for (int i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "VISIT") {
                back_pages.push(current);
                cin >> current;
                next_pages = stack<long long>();
            } else if (command == "BACK") {
                if (!back_pages.empty()) {
                    next_pages.push(current);
                    current = back_pages.top();
                    back_pages.pop();
                }
            } else if (!next_pages.empty()) {
                back_pages.push(current);
                current = next_pages.top();
                next_pages.pop();
            }
            cout << (i > 0 ? " " : "") << current;
        }
        cout << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        stack<long long> back_pages, next_pages;
        long long current = 0;
        for (int i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "VISIT") {
                back_pages.push(current);
                cin >> current;
                next_pages = stack<long long>();
            } else if (command == "BACK") {
                if (!back_pages.empty()) {
                    next_pages.push(current);
                    current = back_pages.top();
                    back_pages.pop();
                }
            } else if (!next_pages.empty()) {
                back_pages.push(current);
                current = next_pages.top();
                next_pages.pop();
            }
            cout << (i > 0 ? " " : "") << current;
        }
        cout << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-browser-history
LANGUAGE: python
BUG: mutate_while_iterating
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    back, ahead = [], []
    current = 1
    shown = []
    for _ in range(n):
        parts = input().split()
        if parts[0] == "VISIT":
            back.append(current)
            current = int(parts[1])
            for page in ahead[:]:
                ahead.remove(page)
        elif parts[0] == "BACK":
            if back:
                ahead.append(current)
                current = back.pop()
        elif ahead:
            back.append(current)
            current = ahead.pop()
        shown.append(current)
    print(*shown)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    back, ahead = [], []
    current = 1
    shown = []
    for _ in range(n):
        parts = input().split()
        if parts[0] == "VISIT":
            back.append(current)
            current = int(parts[1])
            for page in ahead:
                ahead.remove(page)
        elif parts[0] == "BACK":
            if back:
                ahead.append(current)
                current = back.pop()
        elif ahead:
            back.append(current)
            current = ahead.pop()
        shown.append(current)
    print(*shown)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-next-greater
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    answer = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= values[i]:
            stack.pop()
        if stack:
            answer[i] = stack[-1]
        stack.append(values[i])
    print(*answer)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    answer = [-1] * n
    stack = []
    for i in range(n - 1, 0, -1):
        while stack and stack[-1] <= values[i]:
            stack.pop()
        if stack:
            answer[i] = stack[-1]
        stack.append(values[i])
    print(*answer)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-stk-bracket-error
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def first_error(s):
    match = {")": "(", "]": "[", "}": "{"}
    stack = []
    for i, ch in enumerate(s, 1):
        if ch in "([{":
            stack.append((ch, i))
        elif stack and stack[-1][0] == match[ch]:
            stack.pop()
        else:
            return i
    if stack:
        return stack[0][1]
    return "OK"


t = int(input())
for _ in range(t):
    print(first_error(input().strip()))
```
BUGGY:
```python
def first_error(s):
    match = {")": "(", "]": "[", "}": "{"}
    stack = []
    for i, ch in enumerate(s, 1):
        if ch in "([{":
            stack.append((ch, i))
        elif stack and stack[-1][0] == match[ch]:
            stack.pop()
        else:
            print(i)
    if stack:
        return stack[0][1]
    return "OK"


t = int(input())
for _ in range(t):
    print(first_error(input().strip()))
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
items = [4, 5, 6]
a = items.pop()
b = items.pop(0)
print(a, b)
```
OPTIONS:
A) 6 4 || correct
B) 4 6 || none
C) 6 5 || none
D) 4 5 || none
EXPLANATION: pop() with no index removes the last value, while pop(0) removes the first one, so a gets 6 and b gets 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
from collections import deque

q = deque(["A", "B", "C"])
order = ""
for _ in range(5):
    person = q.popleft()
    order += person
    q.append(person)
print(order)
```
OPTIONS:
A) ABCABC || off_by_one
B) CBACB || none
C) ABCAB || correct
D) ABCCB || none
EXPLANATION: Each turn takes the person at the front and sends them to the back, so the turns cycle A, B, C, A, B over five rounds.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
text = []
undone = []
for action in ["a", "b", "UNDO", "c", "d", "UNDO", "UNDO", "e"]:
    if action == "UNDO":
        if text:
            undone.append(text.pop())
    else:
        text.append(action)
print("".join(text), "".join(undone))
```
OPTIONS:
A) ae cdb || none
B) ae bdc || correct
C) ace bd || none
D) e bdc || none
EXPLANATION: Each UNDO pops the most recent letter still in text, so b, then d, then c are removed in that order, leaving a and the later e.
=== END ===
