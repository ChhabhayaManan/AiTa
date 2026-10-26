# Loops

=== PROBLEM ===
ID: aita-digit-sum
DIFFICULTY: easy
STATEMENT: A single line contains a non-negative integer n. Print the sum of its decimal digits.
CONSTRAINTS: 0 <= n <= 1000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    print(total)
```
TESTS:
### input
123
### output
6
### input
0
### output
0
### input
7
### output
7
### input
1000
### output
1
### input
999999999
### output
81
### input
40506
### output
15
=== END ===

=== PROBLEM ===
ID: aita-count-divisors
DIFFICULTY: easy
STATEMENT: A single line contains a positive integer n. Print how many positive integers divide n exactly, counting 1 and n itself.
CONSTRAINTS: 1 <= n <= 10000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    count = 0
    for d in range(1, n + 1):
        if n % d == 0:
            count += 1
    print(count)
```
TESTS:
### input
6
### output
4
### input
1
### output
1
### input
7
### output
2
### input
12
### output
6
### input
36
### output
9
### input
10000
### output
25
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int count = 0;
    for (int i = 0; i < 5; i++) {
        count++;
    }
    printf("%d\n", count);
    return 0;
}
```
OPTIONS:
A) 4 || off_by_one
B) 5 || correct
C) 6 || off_by_one
D) 0 || none
EXPLANATION: i takes the values 0, 1, 2, 3 and 4, so the body runs five times.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i += 3) {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```
OPTIONS:
A) 1 4 7 || wrong_loop_bound
B) 1 2 3 4 5 6 7 8 9 10 || none
C) 1 4 7 10 || correct
D) 1 4 7 10 13 || wrong_loop_bound
EXPLANATION: i goes 1, 4, 7, 10; the next value 13 fails i <= 10, so 10 is the last one printed.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int n = 10;
    int steps = 0;
    while (n > 1) {
        n = n / 2;
        steps++;
    }
    printf("%d\n", steps);
    return 0;
}
```
OPTIONS:
A) 3 || correct
B) 4 || off_by_one
C) 5 || none
D) 2 || off_by_one
EXPLANATION: n goes 10, 5, 2, 1 because integer division drops the remainder, so the loop runs three times.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int total = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = i; j < 3; j++) {
            total++;
        }
    }
    printf("%d\n", total);
    return 0;
}
```
OPTIONS:
A) 9 || none
B) 3 || none
C) 5 || off_by_one
D) 6 || correct
EXPLANATION: The inner loop starts at i, so it runs 3, then 2, then 1 times: 3 + 2 + 1 = 6.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int x = 5;
    do {
        printf("%d ", x);
        x--;
    } while (x > 5);
    printf("\n");
    return 0;
}
```
OPTIONS:
A) Nothing is printed || none
B) 5 || correct
C) 5 4 3 2 1 || wrong_loop_bound
D) 4 || off_by_one
EXPLANATION: A do-while runs its body once before checking the condition, so 5 is printed, then x > 5 is false.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int sum = 0;
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;
        }
        if (i > 7) {
            break;
        }
        sum += i;
    }
    printf("%d\n", sum);
    return 0;
}
```
OPTIONS:
A) 25 || wrong_loop_bound
B) 12 || none
C) 16 || correct
D) 9 || none
EXPLANATION: Even values are skipped by continue, and the loop stops at 9 before adding it, so the sum is 1 + 3 + 5 + 7 = 16.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int main() {
    int product = 1;
    for (int i = 1; i <= 4; i++) {
        product *= i;
    }
    cout << product << endl;
    return 0;
}
```
OPTIONS:
A) 24 || correct
B) 6 || wrong_loop_bound
C) 10 || none
D) 0 || wrong_initial_value
EXPLANATION: product becomes 1 * 1 * 2 * 3 * 4 = 24.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {3, 1, 4};
    int s = 0;
    for (int x : v) {
        s += x;
    }
    cout << s << endl;
    return 0;
}
```
OPTIONS:
A) 3 || none
B) 314 || none
C) 8 || correct
D) 7 || off_by_one
EXPLANATION: The range-based for visits every element, so s = 3 + 1 + 4 = 8.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int main() {
    int i = 0;
    while (i < 10) {
        i += 4;
    }
    cout << i << endl;
    return 0;
}
```
OPTIONS:
A) 8 || off_by_one
B) 10 || none
C) 16 || none
D) 12 || correct
EXPLANATION: i goes 0, 4, 8, 12; the check happens before each step, so the loop stops only after i reaches 12.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 0, j = 5; i < j; i++, j--) {
        cout << i << j << " ";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 05 14 23 || correct
B) 05 14 23 32 || wrong_loop_bound
C) 05 14 || off_by_one
D) 0 5 1 4 2 3 || none
EXPLANATION: The pairs are (0,5), (1,4), (2,3); after that i = 3 and j = 2, so i < j is false.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= i; j++) {
            cout << j;
        }
        cout << " ";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 1 22 333 || none
B) 1 12 123 || correct
C) 123 123 123 || none
D) 1 12 || wrong_loop_bound
EXPLANATION: On pass i the inner loop prints 1 up to i, giving 1, then 12, then 123.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 1234;
    int rev = 0;
    while (n > 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    cout << rev << endl;
    return 0;
}
```
OPTIONS:
A) 1234 || none
B) 10 || none
C) 4321 || correct
D) 432 || off_by_one
EXPLANATION: Each pass moves the last digit of n onto the end of rev, so the digits come out reversed.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
for i in range(2, 11, 4):
    print(i, end=" ")
print()
```
OPTIONS:
A) 2 6 || wrong_loop_bound
B) 2 6 10 || correct
C) 2 4 6 8 10 || none
D) 6 10 || off_by_one
EXPLANATION: range(2, 11, 4) gives 2, 6 and 10; the stop value 11 is never reached.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
total = 0
for i in range(1, 4):
    for j in range(i):
        total += j
print(total)
```
OPTIONS:
A) 6 || none
B) 3 || off_by_one
C) 10 || none
D) 4 || correct
EXPLANATION: j runs 0; then 0, 1; then 0, 1, 2. Adding those gives 0 + 1 + 3 = 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
i = 0
while True:
    i += 3
    if i % 5 == 0:
        break
print(i)
```
OPTIONS:
A) 15 || correct
B) 5 || none
C) 12 || off_by_one
D) 18 || none
EXPLANATION: i takes the values 3, 6, 9, 12, 15; 15 is the first one divisible by 5, so the loop breaks there.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A loop's condition never becomes false and its body has no break or return. What happens when the program runs?
OPTIONS:
A) It stops on its own after a fixed number of repetitions || none
B) It keeps running until the program is stopped from outside || correct
C) It refuses to start because the condition is always true || none
D) It runs the body once and then stops || none
EXPLANATION: Nothing in the language limits how often a loop repeats; without a way out it is an infinite loop.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A loop counter starts at 0, the loop keeps going while the counter is less than n, and the counter goes up by 1 after each pass. For n greater than 0, how many times does the body run?
OPTIONS:
A) n - 1 times || off_by_one
B) n + 1 times || off_by_one
C) n times || correct
D) n / 2 times || none
EXPLANATION: The counter takes the values 0, 1, ..., n - 1, which is n values, one per pass.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A break statement runs inside an inner loop that sits inside an outer loop. What does it do?
OPTIONS:
A) It ends both loops at once || none
B) It skips the rest of this pass of the inner loop and starts its next pass || none
C) It ends the whole program || none
D) It ends only the inner loop; the outer loop carries on || correct
EXPLANATION: break leaves the nearest enclosing loop only; skipping to the next pass is what continue does.
=== END ===

=== DEBUG ===
PROBLEM: dsa-fizzbuzz
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) {
            if (i % 15 == 0) {
                printf("FizzBuzz\n");
            } else if (i % 3 == 0) {
                printf("Fizz\n");
            } else if (i % 5 == 0) {
                printf("Buzz\n");
            } else {
                printf("%d\n", i);
            }
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
        int n;
        scanf("%d", &n);
        for (int i = 1; i < n; i++) {
            if (i % 15 == 0) {
                printf("FizzBuzz\n");
            } else if (i % 3 == 0) {
                printf("Fizz\n");
            } else if (i % 5 == 0) {
                printf("Buzz\n");
            } else {
                printf("%d\n", i);
            }
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-fizzbuzz
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        for (int i = 1; i <= n; i++) {
            if (i % 15 == 0) {
                cout << "FizzBuzz" << endl;
            } else if (i % 3 == 0) {
                cout << "Fizz" << endl;
            } else if (i % 5 == 0) {
                cout << "Buzz" << endl;
            } else {
                cout << i << endl;
            }
        }
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        for (int i = 0; i <= n; i++) {
            if (i % 15 == 0) {
                cout << "FizzBuzz" << endl;
            } else if (i % 3 == 0) {
                cout << "Fizz" << endl;
            } else if (i % 5 == 0) {
                cout << "Buzz" << endl;
            } else {
                cout << i << endl;
            }
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-divisors
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    count = 0
    for d in range(1, n + 1):
        if n % d == 0:
            count += 1
    print(count)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    count = 0
    for d in range(1, n):
        if n % d == 0:
            count += 1
    print(count)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-divisors
LANGUAGE: c
BUG: wrong_initial_value
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int count = 0;
        for (int d = 1; d <= n; d++) {
            if (n % d == 0) {
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

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int count = 1;
        for (int d = 1; d <= n; d++) {
            if (n % d == 0) {
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
PROBLEM: aita-count-divisors
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int count = 0;
        for (int d = 1; d <= n; d++) {
            if (n % d == 0) {
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

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int count = 0;
        for (int d = 2; d <= n; d++) {
            if (n % d == 0) {
                count++;
            }
        }
        cout << count << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    print(total)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    while n > 9:
        total += n % 10
        n //= 10
    print(total)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum
LANGUAGE: c
BUG: uninitialised_variable
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int total = 0;
        while (n > 0) {
            total += n % 10;
            n /= 10;
        }
        printf("%d\n", total);
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
    int total = 0;
    while (t--) {
        int n;
        scanf("%d", &n);
        while (n > 0) {
            total += n % 10;
            n /= 10;
        }
        printf("%d\n", total);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int total = 0;
        while (n > 0) {
            total += n % 10;
            n /= 10;
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

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int total = n % 10;
        while (n > 0) {
            total += n % 10;
            n /= 10;
        }
        cout << total << endl;
    }
    return 0;
}
```
=== END ===

=== PROBLEM ===
ID: aita-alternating-sum
DIFFICULTY: easy
STATEMENT: A single line contains a positive integer n. Work out 1 - 2 + 3 - 4 + 5 - ... up to n, where every odd number is added and every even number is subtracted, and print the result.
CONSTRAINTS: 1 <= n <= 1000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    total = 0
    for i in range(1, n + 1):
        if i % 2 == 1:
            total += i
        else:
            total -= i
    print(total)
```
TESTS:
### input
5
### output
3
### input
1
### output
1
### input
2
### output
-1
### input
10
### output
-5
### input
999999
### output
500000
### input
1000000
### output
-500000
=== END ===

=== PROBLEM ===
ID: aita-countdown-rows
DIFFICULTY: easy
STATEMENT: A single line contains a positive integer n. Print n lines. Line number i (counting from 1) contains the integers from i down to 1, separated by single spaces.
CONSTRAINTS: 1 <= n <= 20.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    for i in range(1, n + 1):
        print(" ".join(str(j) for j in range(i, 0, -1)))
```
TESTS:
### input
3
### output
1
2 1
3 2 1
### input
1
### output
1
### input
2
### output
1
2 1
### input
5
### output
1
2 1
3 2 1
4 3 2 1
5 4 3 2 1
### input
12
### output
1
2 1
3 2 1
4 3 2 1
5 4 3 2 1
6 5 4 3 2 1
7 6 5 4 3 2 1
8 7 6 5 4 3 2 1
9 8 7 6 5 4 3 2 1
10 9 8 7 6 5 4 3 2 1
11 10 9 8 7 6 5 4 3 2 1
12 11 10 9 8 7 6 5 4 3 2 1
=== END ===

=== PROBLEM ===
ID: aita-savings-days
DIFFICULTY: medium
STATEMENT: A single line contains three integers a, d and s. Riya saves a rupees on day 1, and on every later day she saves d rupees more than she saved the day before. Print the number of days after which her total savings first become at least s rupees.
CONSTRAINTS: 1 <= a <= 1000, 0 <= d <= 1000, 1 <= s <= 1000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    a, d, s = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
    pos += 3
    total = 0
    amount = a
    days = 0
    while total < s:
        total += amount
        amount += d
        days += 1
    print(days)
```
TESTS:
### input
3 2 100
### output
10
### input
5 0 5
### output
1
### input
5 0 6
### output
2
### input
1 1 10
### output
4
### input
1 0 1000000
### output
1000000
### input
1000 1000 1000000
### output
45
=== END ===

=== PROBLEM ===
ID: aita-digit-sum-steps
DIFFICULTY: medium
STATEMENT: A single line contains a non-negative integer n. Replace n by the sum of its digits, and keep doing this until n has only one digit. Print how many replacements were made. If n already has one digit, print 0.
CONSTRAINTS: 0 <= n <= 1000000000000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    steps = 0
    while n >= 10:
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        n = s
        steps += 1
    print(steps)
```
TESTS:
### input
99
### output
2
### input
0
### output
0
### input
7
### output
0
### input
10
### output
1
### input
199
### output
3
### input
1000000000000000000
### output
1
### input
999999999999999999
### output
2
=== END ===

=== PROBLEM ===
ID: aita-digit-sum-divides
DIFFICULTY: hard
STATEMENT: A single line contains two integers L and R. Count how many integers x with L <= x <= R are divisible by the sum of their own digits, and print the count. For example, 12 counts because 1 + 2 = 3 divides 12, but 13 does not count because 1 + 3 = 4 does not divide 13.
CONSTRAINTS: 1 <= L <= R <= 1000000000, R - L <= 100000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    low, high = int(data[pos]), int(data[pos + 1])
    pos += 2
    count = 0
    for x in range(low, high + 1):
        m = x
        s = 0
        while m > 0:
            s += m % 10
            m //= 10
        if x % s == 0:
            count += 1
    print(count)
```
TESTS:
### input
11 20
### output
3
### input
1 1
### output
1
### input
11 11
### output
0
### input
1 10
### output
10
### input
1 100
### output
33
### input
123456 123999
### output
58
### input
999900000 1000000000
### output
4130
=== END ===

=== DEBUG ===
PROBLEM: aita-alternating-sum
LANGUAGE: c
BUG: wrong_initial_value
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        long long total = 0;
        int sign = 1;
        for (int i = 1; i <= n; i++) {
            total += sign * i;
            sign = -sign;
        }
        printf("%lld\n", total);
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
        int n;
        scanf("%d", &n);
        long long total = 0;
        int sign = -1;
        for (int i = 1; i <= n; i++) {
            total += sign * i;
            sign = -sign;
        }
        printf("%lld\n", total);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-savings-days
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long a, d, s;
        scanf("%lld %lld %lld", &a, &d, &s);
        long long total = 0;
        long long amount = a;
        int days = 0;
        while (total < s) {
            total += amount;
            amount += d;
            days++;
        }
        printf("%d\n", days);
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
        long long a, d, s;
        scanf("%lld %lld %lld", &a, &d, &s);
        long long total = 0;
        long long amount = a;
        int days = 0;
        while (total <= s) {
            total += amount;
            amount += d;
            days++;
        }
        printf("%d\n", days);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum-steps
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n;
        scanf("%lld", &n);
        int steps = 0;
        while (n >= 10) {
            long long s = 0;
            while (n > 0) {
                s += n % 10;
                n /= 10;
            }
            n = s;
            steps++;
        }
        printf("%d\n", steps);
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
        long long n;
        scanf("%lld", &n);
        int steps = 0;
        do {
            long long s = 0;
            while (n > 0) {
                s += n % 10;
                n /= 10;
            }
            n = s;
            steps++;
        } while (n >= 10);
        printf("%d\n", steps);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-countdown-rows
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        for (int i = 1; i <= n; i++) {
            for (int j = i; j >= 1; j--) {
                cout << j;
                if (j > 1) {
                    cout << " ";
                }
            }
            cout << endl;
        }
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        for (int i = 1; i <= n; i++) {
            for (int j = n; j >= 1; j--) {
                cout << j;
                if (j > 1) {
                    cout << " ";
                }
            }
            cout << endl;
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum-divides
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long low, high;
        cin >> low >> high;
        int count = 0;
        for (long long x = low; x <= high; x++) {
            long long m = x;
            long long s = 0;
            while (m > 0) {
                s += m % 10;
                m /= 10;
            }
            if (x % s == 0) {
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

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long low, high;
        cin >> low >> high;
        int count = 0;
        for (long long x = low; x < high; x++) {
            long long m = x;
            long long s = 0;
            while (m > 0) {
                s += m % 10;
                m /= 10;
            }
            if (x % s == 0) {
                count++;
            }
        }
        cout << count << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum-steps
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int steps = 0;
        while (n >= 10) {
            long long s = 0;
            while (n > 0) {
                s += n % 10;
                n /= 10;
            }
            n = s;
            steps++;
        }
        cout << steps << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int steps = 0;
        while (n >= 10) {
            long long s = 0;
            while (n > 9) {
                s += n % 10;
                n /= 10;
            }
            n = s;
            steps++;
        }
        cout << steps << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-fizzbuzz
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    for i in range(n):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-alternating-sum
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    for i in range(1, n + 1, 2):
        total += i
    for i in range(2, n + 1, 2):
        total -= i
    print(total)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    for i in range(1, n + 1, 2):
        total += i
    for i in range(2, n, 2):
        total -= i
    print(total)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-savings-days
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    a, d, s = map(int, input().split())
    total = 0
    amount = a
    days = 0
    while total < s:
        total += amount
        amount += d
        days += 1
    print(days)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    a, d, s = map(int, input().split())
    total = a
    amount = a
    days = 0
    while total < s:
        total += amount
        amount += d
        days += 1
    print(days)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-digit-sum-divides
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    low, high = map(int, input().split())
    count = 0
    for x in range(low, high + 1):
        m = x
        s = 0
        while m > 0:
            s += m % 10
            m //= 10
        if x % s == 0:
            count += 1
    print(count)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    low, high = map(int, input().split())
    count = 0
    for x in range(low, high + 1):
        m = x
        s = 0
        while m > 0:
            s += m % 10
            m /= 10
        if x % s == 0:
            count += 1
    print(count)
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
for i in range(5, 0, -1):
    print(i, end=" ")
print()
```
OPTIONS:
A) 5 4 3 2 1 0 || wrong_loop_bound
B) Nothing is printed || none
C) 5 4 3 2 1 || correct
D) 4 3 2 1 0 || off_by_one
EXPLANATION: With a step of -1 the range counts down from 5 and stops just before reaching 0.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
total = 0
for i in range(5):
    i += 2
    total += i
print(total)
```
OPTIONS:
A) 7 || none
B) 20 || correct
C) 10 || none
D) 27 || off_by_one
EXPLANATION: Changing i inside the body does not affect the next pass, so i is still 0 to 4 and the sum is 2 + 3 + 4 + 5 + 6 = 20.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
for n in range(3):
    pass
else:
    print("A", end="")
for n in range(3):
    if n == 1:
        break
else:
    print("B", end="")
print(n)
```
OPTIONS:
A) AB2 || none
B) A1 || correct
C) AB1 || none
D) A2 || none
EXPLANATION: A loop's else part runs only when the loop finishes without break, so only A is printed, and n is still 1 from the pass that broke out.
=== END ===
