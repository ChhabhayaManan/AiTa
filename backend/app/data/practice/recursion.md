# Recursion

=== PROBLEM ===
ID: aita-factorial
DIFFICULTY: easy
STATEMENT: A single line contains an integer n. Print n factorial, the product 1 * 2 * ... * n, where the factorial of 0 is 1.
CONSTRAINTS: 0 <= n <= 20.
REFERENCE:
```python
import sys
from math import factorial

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(factorial(int(data[k])))
```
TESTS:
### input
5
### output
120
### input
0
### output
1
### input
1
### output
1
### input
10
### output
3628800
### input
20
### output
2432902008176640000
### input
3
### output
6
=== END ===

=== PROBLEM ===
ID: aita-to-binary
DIFFICULTY: medium
STATEMENT: A single line contains a non-negative integer n. Print n written in binary, without leading zeros; for 0 print 0.
CONSTRAINTS: 0 <= n <= 1000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(bin(int(data[k]))[2:])
```
TESTS:
### input
5
### output
101
### input
0
### output
0
### input
1
### output
1
### input
8
### output
1000
### input
255
### output
11111111
### input
1000000000
### output
111011100110101100101000000000
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int f(int n) {
    if (n == 0) {
        return 0;
    }
    return n + f(n - 1);
}

int main(void) {
    printf("%d\n", f(4));
    return 0;
}
```
OPTIONS:
A) 4 || none
B) 10 || correct
C) 24 || none
D) 6 || off_by_one
EXPLANATION: f(4) = 4 + f(3) = 4 + 3 + 2 + 1 + f(0), and f(0) is 0.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

void countdown(int n) {
    if (n == 0) {
        return;
    }
    printf("%d ", n);
    countdown(n - 1);
}

int main(void) {
    countdown(3);
    printf("\n");
    return 0;
}
```
OPTIONS:
A) 1 2 3 || none
B) 3 2 1 0 || missing_base_case
C) 3 2 1 || correct
D) 3 || none
EXPLANATION: Each call prints n before calling itself with n - 1; the call with 0 returns without printing.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

void up(int n) {
    if (n == 0) {
        return;
    }
    up(n - 1);
    printf("%d ", n);
}

int main(void) {
    up(3);
    printf("\n");
    return 0;
}
```
OPTIONS:
A) 1 2 3 || correct
B) 3 2 1 || none
C) 0 1 2 3 || missing_base_case
D) 3 || none
EXPLANATION: The recursive call comes before the printf, so the deepest call prints first and the output comes out in increasing order.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int power(int b, int e) {
    if (e == 0) {
        return 1;
    }
    return b * power(b, e - 1);
}

int main(void) {
    printf("%d\n", power(2, 5));
    return 0;
}
```
OPTIONS:
A) 10 || none
B) 16 || off_by_one
C) 25 || none
D) 32 || correct
EXPLANATION: power(2, 5) multiplies 2 five times before reaching power(2, 0) = 1.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int g(int n) {
    if (n <= 1) {
        return 1;
    }
    return g(n - 1) + g(n - 2);
}

int main(void) {
    printf("%d\n", g(5));
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 13 || none
C) 8 || correct
D) 120 || none
EXPLANATION: With g(0) = g(1) = 1, the values go 1, 1, 2, 3, 5, 8 for n = 0 to 5.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int calls = 0;

int h(int n) {
    calls++;
    if (n <= 1) {
        return n;
    }
    return h(n - 1) + h(n - 2);
}

int main(void) {
    h(4);
    printf("%d\n", calls);
    return 0;
}
```
OPTIONS:
A) 4 || none
B) 5 || none
C) 7 || none
D) 9 || correct
EXPLANATION: Each call counts itself plus its two sub-calls: calls(0) = calls(1) = 1, calls(2) = 3, calls(3) = 5, calls(4) = 1 + 5 + 3 = 9.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int sumDigits(int n) {
    if (n < 10) {
        return n;
    }
    return n % 10 + sumDigits(n / 10);
}

int main() {
    cout << sumDigits(482) << endl;
    return 0;
}
```
OPTIONS:
A) 14 || correct
B) 12 || none
C) 482 || none
D) 8 || none
EXPLANATION: 2 + sumDigits(48) = 2 + 8 + sumDigits(4) = 2 + 8 + 4.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

string rev(string s) {
    if (s.empty()) {
        return "";
    }
    return rev(s.substr(1)) + s[0];
}

int main() {
    cout << rev("abc") << endl;
    return 0;
}
```
OPTIONS:
A) abc || none
B) cba || correct
C) bca || none
D) a || none
EXPLANATION: The first character is added after the reversed rest, so it ends up last.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int fact(int n) {
    return n <= 1 ? 1 : n * fact(n - 1);
}

int main() {
    cout << fact(5) / fact(3) << endl;
    return 0;
}
```
OPTIONS:
A) 2 || none
B) 120 || none
C) 20 || correct
D) 60 || none
EXPLANATION: fact(5) is 120 and fact(3) is 6, and 120 / 6 = 20.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int countEven(const vector<int> &v, int i) {
    if (i == (int) v.size()) {
        return 0;
    }
    return (v[i] % 2 == 0) + countEven(v, i + 1);
}

int main() {
    vector<int> v = {1, 2, 4, 7, 8};
    cout << countEven(v, 0) << endl;
    return 0;
}
```
OPTIONS:
A) 2 || off_by_one
B) 5 || none
C) 14 || none
D) 3 || correct
EXPLANATION: Each call adds 1 when its element is even (2, 4 and 8) and stops once i reaches the size.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

void hello(int n) {
    if (n > 0) {
        cout << n;
        hello(n - 1);
        cout << n;
    }
}

int main() {
    hello(3);
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 321 || none
B) 123321 || none
C) 321123 || correct
D) 332211 || none
EXPLANATION: Each call prints n on the way down and again on the way back up, after the deeper calls have finished.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

int main() {
    cout << gcd(48, 18) << gcd(17, 5) << endl;
    return 0;
}
```
OPTIONS:
A) 61 || correct
B) 31 || none
C) 6 1 || none
D) 185 || none
EXPLANATION: gcd(48, 18) → gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6, and 17 and 5 share no factor, so their gcd is 1; they print side by side.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
def f(n):
    return 1 if n == 0 else 2 * f(n - 1)

print(f(4))
```
OPTIONS:
A) 8 || off_by_one
B) 16 || correct
C) 32 || off_by_one
D) 4 || none
EXPLANATION: Each call doubles the result of the one below, and f(0) is 1, so f(4) = 2 * 2 * 2 * 2.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
def s(lst):
    return 0 if not lst else lst[0] + s(lst[1:])

print(s([3, 4, 5]))
```
OPTIONS:
A) 12 || correct
B) 3 || none
C) 9 || none
D) 345 || none
EXPLANATION: Each call adds the first element to the sum of the rest; the empty list returns 0.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
def p(n):
    if n > 0:
        p(n - 1)
    print(n, end=" ")

p(3)
print()
```
OPTIONS:
A) 3 2 1 0 || none
B) 1 2 3 || missing_base_case
C) 0 1 2 3 || correct
D) 3 2 1 || none
EXPLANATION: Every call prints after its recursive call returns, including the call with n = 0, so the numbers come out from 0 upward.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What is the base case of a recursive function?
OPTIONS:
A) The first line of the function || none
B) The case where the function returns an answer without calling itself again || correct
C) The largest input the function can handle || none
D) The call that the main program makes first || none
EXPLANATION: The base case is the stopping point; every chain of recursive calls must eventually reach it.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A recursive function has no base case, so it always calls itself again. What happens when it runs?
OPTIONS:
A) It returns 0 after a few calls || none
B) It runs once and stops || none
C) It calls itself until the call stack runs out of memory and the program crashes || correct
D) The compiler or interpreter adds a base case automatically || none
EXPLANATION: Each call takes some stack memory; with no way to stop, the calls pile up until the stack overflows.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A recursive factorial(n) has the base case n == 0. Which recursive call moves it toward that base case?
OPTIONS:
A) factorial(n) || infinite_loop
B) factorial(n + 1) || none
C) factorial(n * 2) || none
D) factorial(n - 1) || correct
EXPLANATION: Each call must make the problem smaller; n - 1 reaches 0 after n steps.
=== END ===

=== DEBUG ===
PROBLEM: dsa-fibonacci
LANGUAGE: python
BUG: missing_base_case
CORRECT:
```python
memo = {}


def fib(n):
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]


t = int(input())
for _ in range(t):
    print(fib(int(input())))
```
BUGGY:
```python
memo = {}


def fib(n):
    if n == 0:
        return 0
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]


t = int(input())
for _ in range(t):
    print(fib(int(input())))
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-fibonacci
LANGUAGE: c
BUG: missing_base_case
CORRECT:
```c
#include <stdio.h>

long long memo[61];
int known[61];

long long fib(int n) {
    if (n < 2) {
        return n;
    }
    if (known[n]) {
        return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    known[n] = 1;
    return memo[n];
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", fib(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long memo[61];
int known[61];

long long fib(int n) {
    if (n == 0) {
        return 0;
    }
    if (known[n]) {
        return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    known[n] = 1;
    return memo[n];
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", fib(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-fibonacci
LANGUAGE: cpp
BUG: missing_base_case
CORRECT:
```cpp
#include <iostream>
#include <vector>
using namespace std;

vector<long long> memo(61, -1);

long long fib(int n) {
    if (n < 2) {
        return n;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    return memo[n];
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << fib(n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <vector>
using namespace std;

vector<long long> memo(61, -1);

long long fib(int n) {
    if (n < 2) {
        return 1;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    return memo[n];
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << fib(n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-factorial
LANGUAGE: python
BUG: missing_base_case
CORRECT:
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


t = int(input())
for _ in range(t):
    print(factorial(int(input())))
```
BUGGY:
```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


t = int(input())
for _ in range(t):
    print(factorial(int(input())))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-factorial
LANGUAGE: c
BUG: missing_base_case
CORRECT:
```c
#include <stdio.h>

long long factorial(int n) {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", factorial(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long factorial(int n) {
    if (n == 0) {
        return 0;
    }
    return n * factorial(n - 1);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", factorial(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-factorial
LANGUAGE: cpp
BUG: infinite_loop
CORRECT:
```cpp
#include <iostream>
using namespace std;

long long factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << factorial(n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

long long factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << factorial(n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-to-binary
LANGUAGE: python
BUG: missing_base_case
CORRECT:
```python
def to_binary(n):
    if n < 2:
        return str(n)
    return to_binary(n // 2) + str(n % 2)


t = int(input())
for _ in range(t):
    print(to_binary(int(input())))
```
BUGGY:
```python
def to_binary(n):
    if n == 0:
        return ""
    return to_binary(n // 2) + str(n % 2)


t = int(input())
for _ in range(t):
    print(to_binary(int(input())))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-to-binary
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

void print_binary(int n) {
    if (n >= 2) {
        print_binary(n / 2);
    }
    printf("%d", n % 2);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        print_binary(n);
        printf("\n");
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

void print_binary(int n) {
    if (n > 2) {
        print_binary(n / 2);
    }
    printf("%d", n % 2);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        print_binary(n);
        printf("\n");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-to-binary
LANGUAGE: cpp
BUG: missing_base_case
CORRECT:
```cpp
#include <iostream>
#include <string>
using namespace std;

string toBinary(int n) {
    if (n < 2) {
        return to_string(n);
    }
    return toBinary(n / 2) + to_string(n % 2);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << toBinary(n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <string>
using namespace std;

string toBinary(int n) {
    if (n == 1) {
        return "1";
    }
    return toBinary(n / 2) + to_string(n % 2);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << toBinary(n) << endl;
    }
    return 0;
}
```
=== END ===
