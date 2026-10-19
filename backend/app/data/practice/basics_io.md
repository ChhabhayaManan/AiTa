# Basics & I/O

=== PROBLEM ===
ID: aita-split-seconds
DIFFICULTY: easy
STATEMENT: A single line contains a non-negative integer s, a number of seconds. Print it as whole hours, minutes and seconds, separated by single spaces, where the minutes and seconds are each less than 60.
CONSTRAINTS: 0 <= s <= 1000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    s = int(data[k])
    print(s // 3600, s % 3600 // 60, s % 60)
```
TESTS:
### input
3661
### output
1 1 1
### input
0
### output
0 0 0
### input
59
### output
0 0 59
### input
3600
### output
1 0 0
### input
86399
### output
23 59 59
### input
100000
### output
27 46 40
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    printf("%d\n", 7 / 2);
    return 0;
}
```
OPTIONS:
A) 3.5 || integer_division
B) 4 || none
C) 3 || correct
D) 3.500000 || integer_division
EXPLANATION: Both 7 and 2 are int, so / is integer division and the fraction is dropped.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a = 5, b = 2;
    printf("%d %d\n", a % b, a * b);
    return 0;
}
```
OPTIONS:
A) 1 10 || correct
B) 2 10 || none
C) 2.5 10 || integer_division
D) 1 7 || none
EXPLANATION: a % b is the remainder of 5 divided by 2, which is 1; a * b is 10.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    printf("%.2f\n", 7 / 2.0);
    return 0;
}
```
OPTIONS:
A) 3.00 || integer_division
B) 3.5 || none
C) 4.00 || none
D) 3.50 || correct
EXPLANATION: 2.0 is a double, so the division keeps the fraction, and %.2f prints exactly two decimals.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int x = 10;
    x += 5;
    x *= 2;
    printf("%d\n", x);
    return 0;
}
```
OPTIONS:
A) 25 || none
B) 30 || correct
C) 20 || none
D) 15 || none
EXPLANATION: x becomes 10 + 5 = 15, then 15 * 2 = 30.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char c = 'A';
    printf("%c %d\n", c + 2, c);
    return 0;
}
```
OPTIONS:
A) A2 65 || none
B) B 65 || off_by_one
C) C 65 || correct
D) 67 A || none
EXPLANATION: A char is stored as a number: 'A' is 65, so c + 2 is 67, which %c prints as C.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int i = 5;
    int j = i++ + 2;
    printf("%d %d\n", i, j);
    return 0;
}
```
OPTIONS:
A) 5 7 || none
B) 6 8 || none
C) 5 8 || none
D) 6 7 || correct
EXPLANATION: i++ gives the old value 5 to the expression and then raises i to 6, so j is 5 + 2 = 7.
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
    cout << 17 % 5 << endl;
    return 0;
}
```
OPTIONS:
A) 3 || none
B) 2 || correct
C) 3.4 || integer_division
D) 12 || none
EXPLANATION: % gives the remainder: 17 = 3 * 5 + 2.
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
    int x = 7;
    x = x * 2 - 3;
    cout << x << endl;
    return 0;
}
```
OPTIONS:
A) 7 || none
B) -7 || none
C) 8 || none
D) 11 || correct
EXPLANATION: The right side is worked out first with the old x: 7 * 2 - 3 = 11, which then replaces x.
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
    int a = 3;
    double b = a / 2;
    cout << b << endl;
    return 0;
}
```
OPTIONS:
A) 1 || correct
B) 1.5 || integer_division
C) 2 || none
D) 1.0 || none
EXPLANATION: a / 2 is worked out with two ints first, giving 1; storing it in a double does not bring the .5 back.
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
    cout << 5 + 3 << "2" << endl;
    return 0;
}
```
OPTIONS:
A) 10 || none
B) 82 || correct
C) 532 || none
D) 5+32 || none
EXPLANATION: 5 + 3 is printed as 8, then the text "2" is printed straight after it.
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

int main() {
    string s = "ab";
    cout << s + "cd" << s.size() << endl;
    return 0;
}
```
OPTIONS:
A) abcd4 || none
B) ab2 || none
C) abcd2 || correct
D) abcd 2 || none
EXPLANATION: s + "cd" makes a new string without changing s, so s.size() is still 2.
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
    cout << (10 / 3) * 3 + 10 % 3 << endl;
    return 0;
}
```
OPTIONS:
A) 9 || integer_division
B) 11 || none
C) 13 || none
D) 10 || correct
EXPLANATION: 10 / 3 is 3, times 3 is 9, and 10 % 3 adds the remainder 1, giving back 10.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
print(7 // 2, 7 % 2)
```
OPTIONS:
A) 3.5 1 || integer_division
B) 3 1 || correct
C) 4 1 || none
D) 3 0.5 || none
EXPLANATION: // divides and drops the fraction, and % gives the remainder, so 7 // 2 is 3 and 7 % 2 is 1.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
x = "5"
y = 3
print(x * y)
```
OPTIONS:
A) 15 || none
B) 8 || none
C) 555 || correct
D) 53 || none
EXPLANATION: x is the text "5", and multiplying text by 3 repeats it three times.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
a, b = 3, 4
a, b = b, a + b
print(a, b)
```
OPTIONS:
A) 4 8 || none
B) 4 7 || correct
C) 3 7 || none
D) 7 4 || none
EXPLANATION: The right side is worked out first using the old values, (4, 3 + 4), and only then assigned.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What is 23 modulo 4, that is, the remainder when 23 is divided by 4?
OPTIONS:
A) 5 || none
B) 5.75 || integer_division
C) 3 || correct
D) 19 || none
EXPLANATION: 4 goes into 23 five whole times (20), leaving 3.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A variable x holds 10. Then the statement x = x + 5 runs. What does it do?
OPTIONS:
A) Nothing, because x can never equal x + 5 || none
B) It creates a second variable called x || none
C) It checks whether x is equal to x + 5 || none
D) It works out 10 + 5 and stores 15 in x, replacing 10 || correct
EXPLANATION: = is assignment, not mathematical equality: the right side is computed first and the result is stored in x.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Why must a program convert what the user types before doing arithmetic with it?
OPTIONS:
A) Typed input arrives as characters, which must be turned into a number before it can be added or multiplied || correct
B) Numbers typed on a keyboard are always stored as negative values || none
C) The computer can only do arithmetic on numbers it wrote itself || none
D) Conversion makes the program run faster but is not needed || none
EXPLANATION: The keyboard sends characters such as '4' and '2'; reading them as a number (for example with scanf("%d"), cin >> or int()) turns them into the value 42.
=== END ===

=== DEBUG ===
PROBLEM: mbpp-127
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    line = input()
    if n == 0:
        print("0.00")
        continue
    values = list(map(int, line.split()))
    print(f"{sum(values) / n:.2f}")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    line = input()
    if n == 0:
        print("0.00")
        continue
    values = list(map(int, line.split()))
    print(f"{sum(values) // n:.2f}")
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-127
LANGUAGE: c
BUG: integer_division
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            sum += x;
        }
        if (n == 0) {
            printf("0.00\n");
        } else {
            printf("%.2f\n", (double) sum / n);
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
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            sum += x;
        }
        if (n == 0) {
            printf("0.00\n");
        } else {
            printf("%.2f\n", (double) (sum / n));
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-127
LANGUAGE: cpp
BUG: empty_input_unhandled
CORRECT:
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            sum += x;
        }
        double average = 0.0;
        if (n > 0) {
            average = (double) sum / n;
        }
        cout << fixed << setprecision(2) << average << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            sum += x;
        }
        double average = (double) sum / n;
        cout << fixed << setprecision(2) << average << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-284
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int prime = n >= 2;
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prime = 0;
                break;
            }
        }
        printf("%s\n", prime ? "Prime" : "Composite");
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
        int prime = n >= 2;
        for (int d = 2; d * d < n; d++) {
            if (n % d == 0) {
                prime = 0;
                break;
            }
        }
        printf("%s\n", prime ? "Prime" : "Composite");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-284
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
        bool prime = true;
        if (n < 2) {
            prime = false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prime = false;
                break;
            }
        }
        cout << (prime ? "Prime" : "Composite") << endl;
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
        bool prime = true;
        if (n < 1) {
            prime = false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prime = false;
                break;
            }
        }
        cout << (prime ? "Prime" : "Composite") << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-split-seconds
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = int(input())
    hours = s // 3600
    minutes = s % 3600 // 60
    seconds = s % 60
    print(hours, minutes, seconds)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = int(input())
    hours = s / 3600
    minutes = s % 3600 // 60
    seconds = s % 60
    print(hours, minutes, seconds)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-split-seconds
LANGUAGE: c
BUG: integer_division
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int s;
        scanf("%d", &s);
        int hours = s / 3600;
        int minutes = s % 3600 / 60;
        int seconds = s % 60;
        printf("%d %d %d\n", hours, minutes, seconds);
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
        int s;
        scanf("%d", &s);
        double hours = s / 3600.0;
        int minutes = s % 3600 / 60;
        int seconds = s % 60;
        printf("%.0f %d %d\n", hours, minutes, seconds);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-split-seconds
LANGUAGE: cpp
BUG: integer_division
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int s;
        cin >> s;
        int hours = s / 3600;
        int minutes = s % 3600 / 60;
        int seconds = s % 60;
        cout << hours << " " << minutes << " " << seconds << endl;
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
        int s;
        cin >> s;
        double hours = s / 3600.0;
        int minutes = s % 3600 / 60;
        int seconds = s % 60;
        cout << hours << " " << minutes << " " << seconds << endl;
    }
    return 0;
}
```
=== END ===
