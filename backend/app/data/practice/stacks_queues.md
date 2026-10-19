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
