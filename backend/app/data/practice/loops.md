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
