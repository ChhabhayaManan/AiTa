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

=== PROBLEM ===
ID: aita-rec-digit-product
DIFFICULTY: easy
STATEMENT: A single line contains a non-negative integer n. Print the product of all the digits of n. The number 0 has the single digit 0, so its product is 0. Solve it with a recursive function: the product for n is its last digit times the product for n with that digit removed.
CONSTRAINTS: 0 <= n <= 1000000000000000000.
REFERENCE:
```python
import sys


def product(n):
    if n < 10:
        return n
    return (n % 10) * product(n // 10)


data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(product(int(data[k])))
```
TESTS:
### input
234
### output
24
### input
0
### output
0
### input
7
### output
7
### input
105
### output
0
### input
10
### output
0
### input
9876
### output
3024
### input
999999999999999999
### output
150094635296999121
### input
1000000000000000000
### output
0
=== END ===

=== PROBLEM ===
ID: aita-rec-digital-root
DIFFICULTY: easy
STATEMENT: A single line contains a non-negative integer n. Replace n by the sum of its digits, and keep doing this until only one digit is left. Print that digit. For example, 38 becomes 3 + 8 = 11, then 1 + 1 = 2, so the answer is 2. A number that already has one digit is its own answer. Solve it with recursion.
CONSTRAINTS: 0 <= n <= 1000000000000000000.
REFERENCE:
```python
import sys


def digit_sum(n):
    if n == 0:
        return 0
    return n % 10 + digit_sum(n // 10)


def root(n):
    if n < 10:
        return n
    return root(digit_sum(n))


data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(root(int(data[k])))
```
TESTS:
### input
38
### output
2
### input
0
### output
0
### input
9
### output
9
### input
10
### output
1
### input
98765
### output
8
### input
999999999999999999
### output
9
### input
1000000000000000000
### output
1
=== END ===

=== PROBLEM ===
ID: aita-rec-ladder-123
DIFFICULTY: medium
STATEMENT: A single line contains an integer n. A ladder has n rungs, and with each move you climb up 1, 2 or 3 rungs. Print the number of different sequences of moves that take you from the ground to exactly the top rung. A ladder with 0 rungs has exactly one way: make no moves. Use recursion and remember the answers you have already worked out, so each n is computed only once.
CONSTRAINTS: 0 <= n <= 60. The answer fits in a 64-bit signed integer.
REFERENCE:
```python
import sys

memo = {}


def ways(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n not in memo:
        memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3)
    return memo[n]


data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(ways(int(data[k])))
```
TESTS:
### input
4
### output
7
### input
0
### output
1
### input
1
### output
1
### input
2
### output
2
### input
3
### output
4
### input
10
### output
274
### input
25
### output
2555757
### input
60
### output
4680045560037375
=== END ===

=== PROBLEM ===
ID: aita-rec-power-mod-halving
DIFFICULTY: medium
STATEMENT: A single line contains two integers b and e. Print b raised to the power e, modulo 1000000007; b to the power 0 is 1. Multiplying e times is far too slow for large e, so use divide and conquer: b^e is (b^(e/2))^2 when e is even, and that times one more b when e is odd, with e/2 rounded down.
CONSTRAINTS: 1 <= b <= 1000000000, 0 <= e <= 1000000000000000000.
REFERENCE:
```python
import sys

MOD = 1000000007


def power(b, e):
    if e == 0:
        return 1
    half = power(b, e // 2)
    result = half * half % MOD
    if e % 2 == 1:
        result = result * b % MOD
    return result


data = sys.stdin.read().split()
t = int(data[0])
for k in range(t):
    b = int(data[1 + 2 * k])
    e = int(data[2 + 2 * k])
    print(power(b % MOD, e))
```
TESTS:
### input
2 10
### output
1024
### input
5 0
### output
1
### input
3 1
### output
3
### input
7 13
### output
889009735
### input
1 1000000000000000000
### output
1
### input
2 1000000006
### output
1
### input
123456789 987654321
### output
652541198
### input
1000000000 1000000000000000000
### output
259616729
=== END ===

=== PROBLEM ===
ID: aita-rec-hanoi-kth-move
DIFFICULTY: hard
STATEMENT: A single line contains two integers n and k. In the Tower of Hanoi puzzle, n disks numbered 1 (smallest) to n (largest) start stacked on peg 1, and all of them must be moved to peg 3, one disk at a time, never placing a larger disk on a smaller one; peg 2 is the spare. The shortest solution takes 2^n - 1 moves: move disks 1 to n-1 from peg 1 to peg 2, then move disk n from peg 1 to peg 3, then move disks 1 to n-1 from peg 2 to peg 3, solving each smaller tower the same way. Print the k-th move of this shortest solution as three integers: the disk number, the peg it leaves and the peg it lands on. Listing all the moves is far too slow; work out which third of the solution move k falls in and recurse into just that part.
CONSTRAINTS: 1 <= n <= 60, 1 <= k <= 2^n - 1.
REFERENCE:
```python
import sys


def kth(n, src, dst, spare, k):
    mid = 1 << (n - 1)
    if k == mid:
        return n, src, dst
    if k < mid:
        return kth(n - 1, src, spare, dst, k)
    return kth(n - 1, spare, dst, src, k - mid)


data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    n = int(data[1 + 2 * i])
    k = int(data[2 + 2 * i])
    print(*kth(n, 1, 3, 2, k))
```
TESTS:
### input
3 6
### output
2 2 3
### input
1 1
### output
1 1 3
### input
2 1
### output
1 1 2
### input
2 2
### output
2 1 3
### input
4 12
### output
3 2 3
### input
5 13
### output
1 1 3
### input
60 1
### output
1 1 2
### input
60 576460752303423488
### output
60 1 3
### input
60 1152921504606846975
### output
1 2 3
### input
60 123456789012345678
### output
2 3 2
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-digit-product
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

long long product(long long n) {
    if (n < 10) {
        return n;
    }
    return (n % 10) * product(n / 10);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n;
        scanf("%lld", &n);
        printf("%lld\n", product(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long product(long long n) {
    if (n <= 10) {
        return n;
    }
    return (n % 10) * product(n / 10);
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n;
        scanf("%lld", &n);
        printf("%lld\n", product(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-ladder-123
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

long long memo[61];
int known[61];

long long ways(int n) {
    if (n < 0) {
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    if (known[n]) {
        return memo[n];
    }
    memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3);
    known[n] = 1;
    return memo[n];
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", ways(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long memo[61];
int known[61];

long long ways(int n) {
    if (n < 1) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    if (known[n]) {
        return memo[n];
    }
    memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3);
    known[n] = 1;
    return memo[n];
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%lld\n", ways(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-digital-root
LANGUAGE: c
BUG: wrong_initial_value
CORRECT:
```c
#include <stdio.h>

long long digit_sum(long long n) {
    if (n == 0) {
        return 0;
    }
    return n % 10 + digit_sum(n / 10);
}

long long root(long long n) {
    if (n < 10) {
        return n;
    }
    return root(digit_sum(n));
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n;
        scanf("%lld", &n);
        printf("%lld\n", root(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long digit_sum(long long n) {
    if (n == 0) {
        return 1;
    }
    return n % 10 + digit_sum(n / 10);
}

long long root(long long n) {
    if (n < 10) {
        return n;
    }
    return root(digit_sum(n));
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n;
        scanf("%lld", &n);
        printf("%lld\n", root(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-digit-product
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
using namespace std;

long long product(long long n) {
    if (n < 10) {
        return n;
    }
    return (n % 10) * product(n / 10);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        cout << product(n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

long long product(long long n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) * product(n / 10);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        cout << product(n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-ladder-123
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
#include <vector>
using namespace std;

vector<long long> memo(61, -1);

long long ways(int n) {
    if (n < 0) {
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3);
    return memo[n];
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << ways(n) << endl;
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

long long ways(int n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3);
    return memo[n];
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << ways(n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-power-mod-halving
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
using namespace std;

const long long MOD = 1000000007;

long long power(long long b, long long e) {
    if (e == 0) {
        return 1;
    }
    long long half = power(b, e / 2);
    long long result = half * half % MOD;
    if (e % 2 == 1) {
        result = result * b % MOD;
    }
    return result;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long b, e;
        cin >> b >> e;
        cout << power(b % MOD, e) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

const long long MOD = 1000000007;

long long power(long long b, long long e) {
    if (e <= 1) {
        return b;
    }
    long long half = power(b, e / 2);
    long long result = half * half % MOD;
    if (e % 2 == 1) {
        result = result * b % MOD;
    }
    return result;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long b, e;
        cin >> b >> e;
        cout << power(b % MOD, e) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-digit-product
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
def product(n):
    if n < 10:
        return n
    return (n % 10) * product(n // 10)


t = int(input())
for _ in range(t):
    print(product(int(input())))
```
BUGGY:
```python
def product(n):
    if n < 10:
        return n
    return (n % 10) * product(n / 10)


t = int(input())
for _ in range(t):
    print(product(int(input())))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-digital-root
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def digit_sum(n):
    if n == 0:
        return 0
    return n % 10 + digit_sum(n // 10)


def root(n):
    if n < 10:
        return n
    return root(digit_sum(n))


t = int(input())
for _ in range(t):
    print(root(int(input())))
```
BUGGY:
```python
def digit_sum(n):
    if n == 0:
        return 0
    return n % 10 + digit_sum(n // 10)


def root(n):
    if n < 10:
        return n
    root(digit_sum(n))


t = int(input())
for _ in range(t):
    print(root(int(input())))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-rec-ladder-123
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
memo = {}


def ways(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n not in memo:
        memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3)
    return memo[n]


t = int(input())
for _ in range(t):
    print(ways(int(input())))
```
BUGGY:
```python
memo = {}


def ways(n):
    if n < 0:
        return 0
    if n == 0:
        return 0
    if n not in memo:
        memo[n] = ways(n - 1) + ways(n - 2) + ways(n - 3)
    return memo[n]


t = int(input())
for _ in range(t):
    print(ways(int(input())))
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
def count(n):
    if n == 0:
        return 0
    return 1 + count(n // 10)

print(count(5072))
```
OPTIONS:
A) 3 || off_by_one
B) 4 || correct
C) 14 || none
D) 5 || off_by_one
EXPLANATION: Each call removes one digit and adds 1, and the call with 0 adds nothing, so a four-digit number gives 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
def show(s):
    if s == "":
        return
    show(s[1:])
    print(s[0], end="")

show("loop")
print()
```
OPTIONS:
A) loop || none
B) oopl || none
C) pool || correct
D) p || none
EXPLANATION: Each call prints its first character only after the call on the rest of the string has finished, so the last character is printed first.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
def walk(n):
    if n == 0:
        return
    walk(n - 1)
    print(n, end="")
    walk(n - 1)

walk(3)
print()
```
OPTIONS:
A) 123 || none
B) 121 || off_by_one
C) 3212123 || none
D) 1213121 || correct
EXPLANATION: walk(1) prints 1, walk(2) prints walk(1), then 2, then walk(1) again, giving 121, and walk(3) wraps 3 between two copies of that.
=== END ===
