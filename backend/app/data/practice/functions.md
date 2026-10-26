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

=== PROBLEM ===
ID: aita-fn-digit-sum-winner
DIFFICULTY: easy
STATEMENT: A single line contains two positive integers a and b. Add up the digits of each number. Print the number whose digits add up to more. If both digit sums are equal, print the smaller of the two numbers. Hint: write a function that returns the digit sum of a number, and call it once for a and once for b.
CONSTRAINTS: 1 <= a, b <= 1000000000000000000.
REFERENCE:
```python
import sys


def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


data = sys.stdin.read().split()
t = int(data[0])
for k in range(t):
    a = int(data[1 + 2 * k])
    b = int(data[2 + 2 * k])
    sa, sb = digit_sum(a), digit_sum(b)
    if sa > sb:
        print(a)
    elif sb > sa:
        print(b)
    else:
        print(min(a, b))
```
TESTS:
### input
123 99
### output
99
### input
55 19
### output
19
### input
1000000000000000000 9
### output
9
### input
7 7
### output
7
### input
999999999999999999 1
### output
999999999999999999
### input
40 13
### output
13
=== END ===

=== PROBLEM ===
ID: aita-fn-round-best
DIFFICULTY: easy
STATEMENT: Three players play n rounds of a game. The first line contains an integer n. Each of the next n lines contains three integers: the scores of the three players in that round. A score can be negative. For every round take the highest of its three scores, and print the sum of these highest scores over all rounds. Hint: write a function that returns the largest of three numbers.
CONSTRAINTS: 1 <= n <= 1000; -1000000000 <= each score <= 1000000000.
REFERENCE:
```python
import sys


def max_of_three(a, b, c):
    best = a
    if b > best:
        best = b
    if c > best:
        best = c
    return best


data = sys.stdin.read().split()
pos = 0
t = int(data[pos])
pos += 1
for _ in range(t):
    n = int(data[pos])
    pos += 1
    total = 0
    for _ in range(n):
        a, b, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        total += max_of_three(a, b, c)
    print(total)
```
TESTS:
### input
3
1 5 3
4 4 2
0 -1 -2
### output
9
### input
1
-5 -2 -9
### output
-2
### input
2
1000000000 999999999 -1000000000
1000000000 1000000000 1000000000
### output
2000000000
### input
4
-1 -1 -1
2 7 7
3 -8 1
-100 -50 -75
### output
-41
### input
1
0 0 0
### output
0
### input
2
-1000000000 -1000000000 -1000000000
-3 -7 -4
### output
-1000000003
=== END ===

=== PROBLEM ===
ID: aita-fn-divisor-classes
DIFFICULTY: medium
STATEMENT: The proper divisors of a number are all its positive divisors smaller than the number itself (the proper divisors of 12 are 1, 2, 3, 4 and 6). A number is perfect if its proper divisors add up to exactly the number, abundant if they add up to more, and deficient if they add up to less. The first line contains an integer n. The second line contains n positive integers. Print three integers separated by single spaces: how many of the n numbers are deficient, how many are perfect, and how many are abundant. Hint: write a function that returns the sum of the proper divisors of a number.
CONSTRAINTS: 1 <= n <= 100; 1 <= each number <= 10000.
REFERENCE:
```python
import sys


def proper_divisor_sum(x):
    return sum(d for d in range(1, x) if x % d == 0)


data = sys.stdin.read().split()
pos = 0
t = int(data[pos])
pos += 1
for _ in range(t):
    n = int(data[pos])
    pos += 1
    counts = [0, 0, 0]
    for x in map(int, data[pos:pos + n]):
        s = proper_divisor_sum(x)
        if s < x:
            counts[0] += 1
        elif s == x:
            counts[1] += 1
        else:
            counts[2] += 1
    pos += n
    print(*counts)
```
TESTS:
### input
5
6 12 7 28 1
### output
2 2 1
### input
1
1
### output
1 0 0
### input
4
496 8128 945 2
### output
1 2 1
### input
6
10000 9999 18 20 16 25
### output
3 0 3
### input
3
2 3 4
### output
3 0 0
### input
100
9901 9902 9903 9904 9905 9906 9907 9908 9909 9910 9911 9912 9913 9914 9915 9916 9917 9918 9919 9920 9921 9922 9923 9924 9925 9926 9927 9928 9929 9930 9931 9932 9933 9934 9935 9936 9937 9938 9939 9940 9941 9942 9943 9944 9945 9946 9947 9948 9949 9950 9951 9952 9953 9954 9955 9956 9957 9958 9959 9960 9961 9962 9963 9964 9965 9966 9967 9968 9969 9970 9971 9972 9973 9974 9975 9976 9977 9978 9979 9980 9981 9982 9983 9984 9985 9986 9987 9988 9989 9990 9991 9992 9993 9994 9995 9996 9997 9998 9999 10000
### output
77 0 23
=== END ===

=== PROBLEM ===
ID: aita-fn-nearest-prime
DIFFICULTY: medium
STATEMENT: A single line contains a positive integer n. Print the prime number closest to n. If n itself is prime, print n. If two primes are equally close to n, print the smaller one. Hint: write a function that checks whether a number is prime, then call it on the numbers n, n - 1, n + 1, n - 2, n + 2 and so on.
CONSTRAINTS: 1 <= n <= 1000000.
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


def nearest_prime(n):
    d = 0
    while True:
        if is_prime(n - d):
            return n - d
        if is_prime(n + d):
            return n + d
        d += 1


data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    print(nearest_prime(int(data[k])))
```
TESTS:
### input
10
### output
11
### input
1
### output
2
### input
2
### output
2
### input
9
### output
7
### input
4
### output
3
### input
120
### output
113
### input
24
### output
23
### input
1000000
### output
1000003
=== END ===

=== PROBLEM ===
ID: aita-fn-triple-prime-kth
DIFFICULTY: hard
STATEMENT: Call a number a triple prime if three numbers are all prime: the number itself, the number written with its digits in reverse order, and the sum of its digits. For example, 113 is a triple prime because 113, 311 and 1 + 1 + 3 = 5 are all prime. 13 is not, because 1 + 3 = 4 is not prime, and 23 is not, because 32 is not prime. The smallest triple primes are 2, 3, 5, 7, 11, 101, 113. A single line contains an integer k. Print the k-th smallest triple prime. Hint: write separate functions for checking a prime, reversing a number and adding up its digits, and reuse them.
CONSTRAINTS: 1 <= k <= 300.
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


def reverse_number(x):
    r = 0
    while x > 0:
        r = r * 10 + x % 10
        x //= 10
    return r


def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


def is_triple_prime(x):
    return is_prime(x) and is_prime(reverse_number(x)) and is_prime(digit_sum(x))


data = sys.stdin.read().split()
t = int(data[0])
ks = [int(v) for v in data[1:1 + t]]
found = []
x = 1
while len(found) < max(ks):
    x += 1
    if is_triple_prime(x):
        found.append(x)
for k in ks:
    print(found[k - 1])
```
TESTS:
### input
1
### output
2
### input
5
### output
11
### input
6
### output
101
### input
10
### output
157
### input
25
### output
919
### input
100
### output
7817
### input
300
### output
19001
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-digit-sum-winner
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int digit_sum(long long x) {
    int total = 0;
    while (x > 0) {
        total += x % 10;
        x /= 10;
    }
    return total;
}

long long winner(long long a, long long b) {
    int sa = digit_sum(a);
    int sb = digit_sum(b);
    if (sa > sb) {
        return a;
    }
    if (sb > sa) {
        return b;
    }
    return a < b ? a : b;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        printf("%lld\n", winner(a, b));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int digit_sum(long long x) {
    int total = 0;
    while (x > 0) {
        total += x % 10;
        x /= 10;
    }
    return total;
}

long long winner(long long a, long long b) {
    int sa = digit_sum(a);
    int sb = digit_sum(b);
    if (sa > sb) {
        return a;
    }
    if (sb > sa) {
        return b;
    }
    return a > b ? a : b;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        printf("%lld\n", winner(a, b));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-divisor-classes
LANGUAGE: c
BUG: wrong_loop_bound
CORRECT:
```c
#include <stdio.h>

int proper_divisor_sum(int x) {
    int sum = 0;
    for (int d = 1; d < x; d++) {
        if (x % d == 0) {
            sum += d;
        }
    }
    return sum;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int deficient = 0, perfect = 0, abundant = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            int s = proper_divisor_sum(x);
            if (s < x) {
                deficient++;
            } else if (s == x) {
                perfect++;
            } else {
                abundant++;
            }
        }
        printf("%d %d %d\n", deficient, perfect, abundant);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int proper_divisor_sum(int x) {
    int sum = 0;
    for (int d = 1; d <= x; d++) {
        if (x % d == 0) {
            sum += d;
        }
    }
    return sum;
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int deficient = 0, perfect = 0, abundant = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            int s = proper_divisor_sum(x);
            if (s < x) {
                deficient++;
            } else if (s == x) {
                perfect++;
            } else {
                abundant++;
            }
        }
        printf("%d %d %d\n", deficient, perfect, abundant);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-nearest-prime
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

int nearest_prime(int n) {
    int d = 0;
    while (1) {
        if (is_prime(n - d)) {
            return n - d;
        }
        if (is_prime(n + d)) {
            return n + d;
        }
        d++;
    }
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%d\n", nearest_prime(n));
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int is_prime(int m) {
    if (m < 2) {
        return 0;
    }
    for (int d = 2; d * d < m; d++) {
        if (m % d == 0) {
            return 0;
        }
    }
    return 1;
}

int nearest_prime(int n) {
    int d = 0;
    while (1) {
        if (is_prime(n - d)) {
            return n - d;
        }
        if (is_prime(n + d)) {
            return n + d;
        }
        d++;
    }
}

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        printf("%d\n", nearest_prime(n));
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-round-best
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
using namespace std;

long long maxOfThree(long long a, long long b, long long c) {
    long long best = a;
    if (b > best) {
        best = b;
    }
    if (c > best) {
        best = c;
    }
    return best;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long total = 0;
        for (int i = 0; i < n; i++) {
            long long a, b, c;
            cin >> a >> b >> c;
            total += maxOfThree(a, b, c);
        }
        cout << total << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

long long maxOfThree(long long a, long long b, long long c) {
    long long best = 0;
    if (a > best) {
        best = a;
    }
    if (b > best) {
        best = b;
    }
    if (c > best) {
        best = c;
    }
    return best;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long total = 0;
        for (int i = 0; i < n; i++) {
            long long a, b, c;
            cin >> a >> b >> c;
            total += maxOfThree(a, b, c);
        }
        cout << total << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-nearest-prime
LANGUAGE: cpp
BUG: wrong_comparison_operator
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

int nearestPrime(int n) {
    int d = 0;
    while (true) {
        if (isPrime(n - d)) {
            return n - d;
        }
        if (isPrime(n + d)) {
            return n + d;
        }
        d++;
    }
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << nearestPrime(n) << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

bool isPrime(int m) {
    if (m <= 2) {
        return false;
    }
    for (int d = 2; d * d <= m; d++) {
        if (m % d == 0) {
            return false;
        }
    }
    return true;
}

int nearestPrime(int n) {
    int d = 0;
    while (true) {
        if (isPrime(n - d)) {
            return n - d;
        }
        if (isPrime(n + d)) {
            return n + d;
        }
        d++;
    }
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        cout << nearestPrime(n) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-triple-prime-kth
LANGUAGE: cpp
BUG: wrong_loop_bound
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

int reverseNumber(int x) {
    int r = 0;
    while (x > 0) {
        r = r * 10 + x % 10;
        x /= 10;
    }
    return r;
}

int digitSum(int x) {
    int s = 0;
    while (x > 0) {
        s += x % 10;
        x /= 10;
    }
    return s;
}

bool isTriplePrime(int x) {
    return isPrime(x) && isPrime(reverseNumber(x)) && isPrime(digitSum(x));
}

int kthTriplePrime(int k) {
    int count = 0;
    int x = 1;
    while (count < k) {
        x++;
        if (isTriplePrime(x)) {
            count++;
        }
    }
    return x;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int k;
        cin >> k;
        cout << kthTriplePrime(k) << endl;
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
        }
    }
    return true;
}

int reverseNumber(int x) {
    int r = 0;
    while (x > 9) {
        r = r * 10 + x % 10;
        x /= 10;
    }
    return r;
}

int digitSum(int x) {
    int s = 0;
    while (x > 0) {
        s += x % 10;
        x /= 10;
    }
    return s;
}

bool isTriplePrime(int x) {
    return isPrime(x) && isPrime(reverseNumber(x)) && isPrime(digitSum(x));
}

int kthTriplePrime(int k) {
    int count = 0;
    int x = 1;
    while (count < k) {
        x++;
        if (isTriplePrime(x)) {
            count++;
        }
    }
    return x;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int k;
        cin >> k;
        cout << kthTriplePrime(k) << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-digit-sum-winner
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


def winner(a, b):
    sa = digit_sum(a)
    sb = digit_sum(b)
    if sa > sb:
        best = a
    elif sb > sa:
        best = b
    else:
        best = min(a, b)
    return best


t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(winner(a, b))
```
BUGGY:
```python
def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


def winner(a, b):
    sa = digit_sum(a)
    sb = digit_sum(b)
    if sa > sb:
        best = a
    elif sb > sa:
        best = b
    else:
        best = min(a, b)
    print(best)


t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(winner(a, b))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-divisor-classes
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
def proper_divisor_sum(x):
    total = 0
    for d in range(1, x // 2 + 1):
        if x % d == 0:
            total += d
    return total


t = int(input())
for _ in range(t):
    n = int(input())
    nums = list(map(int, input().split()))
    deficient = perfect = abundant = 0
    for x in nums:
        s = proper_divisor_sum(x)
        if s < x:
            deficient += 1
        elif s == x:
            perfect += 1
        else:
            abundant += 1
    print(deficient, perfect, abundant)
```
BUGGY:
```python
def proper_divisor_sum(x):
    total = 0
    for d in range(1, x // 2):
        if x % d == 0:
            total += d
    return total


t = int(input())
for _ in range(t):
    n = int(input())
    nums = list(map(int, input().split()))
    deficient = perfect = abundant = 0
    for x in nums:
        s = proper_divisor_sum(x)
        if s < x:
            deficient += 1
        elif s == x:
            perfect += 1
        else:
            abundant += 1
    print(deficient, perfect, abundant)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-fn-triple-prime-kth
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
def is_prime(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def reverse_number(x):
    r = 0
    while x > 0:
        r = r * 10 + x % 10
        x //= 10
    return r


def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


def kth_triple_prime(k):
    count = 0
    x = 1
    while count < k:
        x += 1
        if is_prime(x) and is_prime(reverse_number(x)) and is_prime(digit_sum(x)):
            count += 1
    return x


t = int(input())
for _ in range(t):
    k = int(input())
    print(kth_triple_prime(k))
```
BUGGY:
```python
def is_prime(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def reverse_number(x):
    r = 0
    while x > 0:
        r = r * 10 + x % 10
        x //= 10
    return r


def digit_sum(x):
    total = 0
    while x > 0:
        total += x % 10
        x //= 10
    return total


def kth_triple_prime(k):
    count = 1
    x = 1
    while count < k:
        x += 1
        if is_prime(x) and is_prime(reverse_number(x)) and is_prime(digit_sum(x)):
            count += 1
    return x


t = int(input())
for _ in range(t):
    k = int(input())
    print(kth_triple_prime(k))
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
x = 10

def change():
    x = 5
    return x

y = change()
print(x, y)
```
OPTIONS:
A) 5 5 || none
B) 10 5 || correct
C) 10 10 || none
D) 5 10 || none
EXPLANATION: The x inside change is a new local variable, so the outer x stays 10 while the function returns 5.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
def first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return -1

print(first_even([3, 7, 8, 4]), first_even([1, 5]))
```
OPTIONS:
A) 4 -1 || none
B) 8 None || none
C) 8 -1 || correct
D) 8 4 -1 || none
EXPLANATION: return stops the function at the first even number, 8, and the second list has no even number so the loop ends and -1 is returned.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
def update(nums, k):
    nums.append(k)
    k = k + 1
    nums = [0]
    return k

a = [1]
b = 5
c = update(a, b)
print(a, b, c)
```
OPTIONS:
A) [0] 6 6 || none
B) [1] 5 6 || none
C) [0] 5 6 || none
D) [1, 5] 5 6 || correct
EXPLANATION: append changes the caller's list, but giving k or nums a new value only changes the function's local names, so b stays 5 and a keeps [1, 5].
=== END ===
