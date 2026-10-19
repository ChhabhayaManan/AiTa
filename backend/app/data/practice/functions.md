# Functions

=== PROBLEM ===
ID: aita-gcd
DIFFICULTY: easy
STATEMENT: A single line contains two positive integers a and b. Print their greatest common divisor, the largest integer that divides both.
CONSTRAINTS: 1 <= a, b <= 1000000.
REFERENCE:
```python
import sys
from math import gcd

data = sys.stdin.read().split()
t = int(data[0])
for k in range(t):
    print(gcd(int(data[1 + 2 * k]), int(data[2 + 2 * k])))
```
TESTS:
### input
12 18
### output
6
### input
7 13
### output
1
### input
100 10
### output
10
### input
5 5
### output
5
### input
1 999
### output
1
### input
84 36
### output
12
=== END ===

=== PROBLEM ===
ID: aita-power
DIFFICULTY: easy
STATEMENT: A single line contains two integers a and n. Print a raised to the power n.
CONSTRAINTS: 1 <= a <= 10; 0 <= n <= 15.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(t):
    print(int(data[1 + 2 * k]) ** int(data[2 + 2 * k]))
```
TESTS:
### input
2 10
### output
1024
### input
3 0
### output
1
### input
5 1
### output
5
### input
10 15
### output
1000000000000000
### input
1 15
### output
1
### input
7 3
### output
343
=== END ===

=== PROBLEM ===
ID: aita-count-primes
DIFFICULTY: medium
STATEMENT: A single line contains an integer n. Print how many prime numbers are less than or equal to n.
CONSTRAINTS: 0 <= n <= 10000.
REFERENCE:
```python
import sys


def is_prime(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    print(sum(1 for m in range(n + 1) if is_prime(m)))
```
TESTS:
### input
10
### output
4
### input
1
### output
0
### input
2
### output
1
### input
0
### output
0
### input
100
### output
25
### input
10000
### output
1229
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int square(int x) {
    return x * x;
}

int main(void) {
    printf("%d\n", square(3) + square(2));
    return 0;
}
```
OPTIONS:
A) 25 || none
B) 13 || correct
C) 10 || none
D) 36 || none
EXPLANATION: square(3) is 9 and square(2) is 4, and their sum is 13.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int twice(int x) {
    return 2 * x;
}

int add3(int x) {
    return x + 3;
}

int main(void) {
    printf("%d %d\n", twice(add3(1)), add3(twice(1)));
    return 0;
}
```
OPTIONS:
A) 8 5 || correct
B) 5 8 || none
C) 8 8 || none
D) 5 5 || none
EXPLANATION: The inner call runs first: twice(add3(1)) is twice(4) = 8, and add3(twice(1)) is add3(2) = 5.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

void add_one(int x) {
    x = x + 1;
}

int main(void) {
    int n = 5;
    add_one(n);
    printf("%d\n", n);
    return 0;
}
```
OPTIONS:
A) 6 || none
B) 1 || none
C) 0 || none
D) 5 || correct
EXPLANATION: C passes a copy of n into x; changing the copy leaves n unchanged.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

void add_one(int *x) {
    *x = *x + 1;
}

int main(void) {
    int n = 5;
    add_one(&n);
    printf("%d\n", n);
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 6 || correct
C) The address of n || none
D) 1 || none
EXPLANATION: The function receives the address of n, so *x = *x + 1 changes n itself.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int counter(void) {
    static int count = 0;
    count++;
    return count;
}

int main(void) {
    counter();
    counter();
    printf("%d\n", counter());
    return 0;
}
```
OPTIONS:
A) 1 || wrong_initial_value
B) 0 || none
C) 3 || correct
D) 2 || off_by_one
EXPLANATION: A static local variable keeps its value between calls, so the third call raises it to 3.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

void fill(int a[], int n) {
    for (int i = 0; i < n; i++) {
        a[i] = i * i;
    }
}

int main(void) {
    int a[4] = {9, 9, 9, 9};
    fill(a, 3);
    printf("%d %d\n", a[2], a[3]);
    return 0;
}
```
OPTIONS:
A) 9 9 || none
B) 4 16 || wrong_loop_bound
C) 2 3 || none
D) 4 9 || correct
EXPLANATION: An array is passed as a pointer, so fill changes the caller's array, but only indexes 0 to 2; a[3] keeps 9.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int area(int w, int h = 2) {
    return w * h;
}

int main() {
    cout << area(3) << " " << area(3, 4) << endl;
    return 0;
}
```
OPTIONS:
A) 6 12 || correct
B) 3 12 || none
C) 6 6 || none
D) 12 12 || none
EXPLANATION: area(3) uses the default h = 2; area(3, 4) passes 4 for h.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

bool isEven(int n) {
    return n % 2 == 0;
}

int main() {
    cout << isEven(4) << isEven(7) << endl;
    return 0;
}
```
OPTIONS:
A) truefalse || none
B) 01 || none
C) 10 || correct
D) 11 || none
EXPLANATION: cout prints true as 1 and false as 0; 4 is even and 7 is not.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

void swapVals(int &a, int &b) {
    int t = a;
    a = b;
    b = t;
}

int main() {
    int x = 1, y = 2;
    swapVals(x, y);
    cout << x << " " << y << endl;
    return 0;
}
```
OPTIONS:
A) 1 2 || none
B) 2 1 || correct
C) 2 2 || none
D) 1 1 || none
EXPLANATION: The parameters are references (&), so the function swaps x and y themselves.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

void shout(string s) {
    s += "!";
}

int main() {
    string w = "hi";
    shout(w);
    cout << w << endl;
    return 0;
}
```
OPTIONS:
A) hi! || none
B) ! || none
C) hi || correct
D) hi!! || none
EXPLANATION: s is a copy of w because the parameter is not a reference, so w is unchanged.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int f(int x) {
    return x + 1;
}

double f(double x) {
    return x * 2;
}

int main() {
    cout << f(3) << " " << f(3.0) << endl;
    return 0;
}
```
OPTIONS:
A) 4 4 || none
B) 6 6 || none
C) 4 6 || correct
D) 6 4 || none
EXPLANATION: The compiler picks the overload that matches the argument's type: 3 is an int and 3.0 is a double.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int f(int x) {
    cout << x << " ";
    return x * 2;
}

int main() {
    int r = f(f(1));
    cout << r << endl;
    return 0;
}
```
OPTIONS:
A) 2 1 4 || none
B) 1 2 4 || correct
C) 1 2 || none
D) 4 || none
EXPLANATION: The inner f(1) runs first and prints 1, returning 2; the outer f(2) prints 2 and returns 4, which is printed last.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
def f(x=2):
    return x * 3

print(f(), f(4))
```
OPTIONS:
A) 6 12 || correct
B) 2 4 || none
C) 6 6 || none
D) None 12 || none
EXPLANATION: f() uses the default x = 2, and f(4) uses 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
def double(x):
    print(x * 2, end=" ")

result = double(4)
print(result)
```
OPTIONS:
A) 8 8 || return_vs_print
B) 8 || none
C) 8 None || correct
D) None || none
EXPLANATION: double prints 8 but returns nothing, so result is None.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
def add(item, items=[]):
    items.append(item)
    return items

add(1)
print(add(2))
```
OPTIONS:
A) [2] || none
B) [1, 2] || correct
C) [1] || none
D) [2, 1] || none
EXPLANATION: The default list is created once, when the function is defined, so both calls append to the same list.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What is the difference between a function returning a value and a function printing it?
OPTIONS:
A) There is no difference; both give the value to the caller || return_vs_print
B) Returning hands the value back to the calling code so it can be used further; printing only shows it on the screen || correct
C) Printing stores the value in a variable; returning shows it on the screen || none
D) Returning ends the whole program; printing does not || none
EXPLANATION: Only a returned value can be stored, compared or passed on by the caller; printed text is just output.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A caller's variable n holds 5 and is passed to a function by value, so the function gets its own copy in a parameter x. The function sets x to 100. What is n after the call?
OPTIONS:
A) 5 || correct
B) 100 || none
C) 0 || none
D) It cannot be known || none
EXPLANATION: Passing by value copies the value; changing the copy never touches the caller's variable.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What is the main reason to split a program into functions?
OPTIONS:
A) Each function runs at the same time as the others, so the program is faster || none
B) A program with functions does not need to be compiled or interpreted || none
C) To give one task a name so it can be reused, read and tested on its own || correct
D) Variables cannot exist outside a function || none
EXPLANATION: Functions let you write a task once, call it wherever it is needed, and check it separately.
=== END ===

=== DEBUG ===
PROBLEM: aita-gcd
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(gcd(a, b))
```
BUGGY:
```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    print(a)


t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(gcd(a, b))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-gcd
LANGUAGE: c
BUG: return_vs_print
CORRECT:
```c
#include <stdio.h>

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\n", gcd(a, b));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return b;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\n", gcd(a, b));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-gcd
LANGUAGE: cpp
BUG: infinite_loop
CORRECT:
```cpp
#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int a, b;
        cin >> a >> b;
        cout << gcd(a, b) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
    }
    return a;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int a, b;
        cin >> a >> b;
        cout << gcd(a, b) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-power
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
def power(a, n):
    result = 1
    for _ in range(n):
        result *= a
    return result


t = int(input())
for _ in range(t):
    a, n = map(int, input().split())
    print(power(a, n))
```
BUGGY:
```python
def power(a, n):
    result = 0
    for _ in range(n):
        result *= a
    return result


t = int(input())
for _ in range(t):
    a, n = map(int, input().split())
    print(power(a, n))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-power
LANGUAGE: c
BUG: wrong_loop_bound
CORRECT:
```c
#include <stdio.h>

long long power(int a, int n) {
    long long result = 1;
    for (int i = 0; i < n; i++) {
        result *= a;
    }
    return result;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, n;
        scanf("%d %d", &a, &n);
        printf("%lld\n", power(a, n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

long long power(int a, int n) {
    long long result = 1;
    for (int i = 0; i <= n; i++) {
        result *= a;
    }
    return result;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, n;
        scanf("%d %d", &a, &n);
        printf("%lld\n", power(a, n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-power
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
using namespace std;

long long power(int a, int n) {
    long long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= a;
    }
    return result;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int a, n;
        cin >> a >> n;
        cout << power(a, n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

long long power(int a, int n) {
    long long result = 1;
    for (int i = 1; i < n; i++) {
        result *= a;
    }
    return result;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int a, n;
        cin >> a >> n;
        cout << power(a, n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-primes
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
def is_prime(m):
    if m < 2:
        return False
    for d in range(2, int(m ** 0.5) + 1):
        if m % d == 0:
            return False
    return True


t = int(input())
for _ in range(t):
    n = int(input())
    count = 0
    for m in range(n + 1):
        if is_prime(m):
            count += 1
    print(count)
```
BUGGY:
```python
def is_prime(m):
    if m < 2:
        return False
    for d in range(2, int(m ** 0.5)):
        if m % d == 0:
            return False
    return True


t = int(input())
for _ in range(t):
    n = int(input())
    count = 0
    for m in range(n + 1):
        if is_prime(m):
            count += 1
    print(count)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-primes
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int is_prime(int m) {
    if (m < 2) {
        return 0;
    }
    for (int d = 2; d * d <= m; d++) {
        if (m % d == 0) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int count = 0;
        for (int m = 2; m <= n; m++) {
            if (is_prime(m)) {
                count++;
            }
        }
        printf("%d\n", count);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int is_prime(int m) {
    for (int d = 2; d * d <= m; d++) {
        if (m % d == 0) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int count = 0;
        for (int m = 1; m <= n; m++) {
            if (is_prime(m)) {
                count++;
            }
        }
        printf("%d\n", count);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-primes
LANGUAGE: cpp
BUG: return_vs_print
CORRECT:
```cpp
#include <iostream>
using namespace std;

bool isPrime(int m) {
    if (m < 2) {
        return false;
    }
    for (int d = 2; d * d <= m; d++) {
        if (m % d == 0) {
            return false;
        }
    }
    return true;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int count = 0;
        for (int m = 2; m <= n; m++) {
            if (isPrime(m)) {
                count++;
            }
        }
        cout << count << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

bool isPrime(int m) {
    if (m < 2) {
        return false;
    }
    for (int d = 2; d * d <= m; d++) {
        if (m % d == 0) {
            return false;
        } else {
            return true;
        }
    }
    return true;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int count = 0;
        for (int m = 2; m <= n; m++) {
            if (isPrime(m)) {
                count++;
            }
        }
        cout << count << endl;
    }
    return 0;
}
```
=== END ===
