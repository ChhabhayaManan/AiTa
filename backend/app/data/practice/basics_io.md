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

=== PROBLEM ===
ID: aita-reverse-three
DIFFICULTY: easy
STATEMENT: A single line contains a three-digit integer n. Print the number you get by writing its digits in reverse order. Leading zeros are dropped, so 120 becomes 21.
CONSTRAINTS: 100 <= n <= 999.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    print(n % 10 * 100 + n // 10 % 10 * 10 + n // 100)
```
TESTS:
### input
123
### output
321
### input
120
### output
21
### input
100
### output
1
### input
999
### output
999
### input
505
### output
505
### input
908
### output
809
### input
110
### output
11
=== END ===

=== PROBLEM ===
ID: aita-benches-needed
DIFFICULTY: easy
STATEMENT: A single line contains two integers n and k: n students must sit on benches, and each bench seats at most k students. Print the smallest number of benches needed so that every student gets a seat.
CONSTRAINTS: 0 <= n <= 1000000; 1 <= k <= 1000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    n = int(data[1 + 2 * i])
    k = int(data[2 + 2 * i])
    print((n + k - 1) // k)
```
TESTS:
### input
10 3
### output
4
### input
12 3
### output
4
### input
0 5
### output
0
### input
1 1000
### output
1
### input
1000000 1
### output
1000000
### input
7 7
### output
1
### input
999999 1000
### output
1000
=== END ===

=== PROBLEM ===
ID: aita-average-temperature
DIFFICULTY: easy
STATEMENT: A single line contains three integers a, b and c: the temperatures, in degrees Celsius, recorded in the morning, the afternoon and the night. Print their average with exactly 2 digits after the decimal point.
CONSTRAINTS: -50 <= a, b, c <= 50.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    a, b, c = (int(x) for x in data[1 + 3 * i:4 + 3 * i])
    print(f"{(a + b + c) / 3:.2f}")
```
TESTS:
### input
30 31 33
### output
31.33
### input
20 20 20
### output
20.00
### input
0 0 1
### output
0.33
### input
-5 -5 -4
### output
-4.67
### input
50 50 49
### output
49.67
### input
-1 0 0
### output
-0.33
### input
0 0 0
### output
0.00
=== END ===

=== PROBLEM ===
ID: aita-show-duration
DIFFICULTY: medium
STATEMENT: A single line contains four integers sh, sm, eh and em: a show starts at sh hours sm minutes and ends at eh hours em minutes, on a 24-hour clock. If the end time is earlier than the start time, the show ran past midnight and ended the next day. If both times are the same, the show lasted 0 minutes. Print how long the show lasted as whole hours and minutes, separated by a single space, where the minutes are less than 60.
CONSTRAINTS: 0 <= sh, eh <= 23; 0 <= sm, em <= 59. Every show lasts less than 24 hours.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    sh, sm, eh, em = (int(x) for x in data[1 + 4 * i:5 + 4 * i])
    d = (eh * 60 + em - (sh * 60 + sm)) % 1440
    print(d // 60, d % 60)
```
TESTS:
### input
18 30 21 0
### output
2 30
### input
23 15 1 5
### output
1 50
### input
9 0 9 0
### output
0 0
### input
0 0 23 59
### output
23 59
### input
23 59 0 0
### output
0 1
### input
10 45 10 44
### output
23 59
### input
7 5 7 20
### output
0 15
=== END ===

=== PROBLEM ===
ID: aita-bill-total
DIFFICULTY: medium
STATEMENT: A single line contains three integers r, p and q: one item costs r rupees and p paise, and a customer buys q of them. 100 paise make 1 rupee. Print the total cost in the form R.PP, where R is the number of whole rupees and PP is the remaining paise written with exactly two digits (so 5 paise is written as 05).
CONSTRAINTS: 0 <= r <= 10000; 0 <= p <= 99; 1 <= q <= 1000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    r, p, q = (int(x) for x in data[1 + 3 * i:4 + 3 * i])
    total = (r * 100 + p) * q
    print(f"{total // 100}.{total % 100:02d}")
```
TESTS:
### input
12 50 2
### output
25.00
### input
0 5 1
### output
0.05
### input
3 35 3
### output
10.05
### input
0 99 1000
### output
990.00
### input
10000 99 1000
### output
10000990.00
### input
7 0 4
### output
28.00
### input
1 1 1
### output
1.01
=== END ===

=== DEBUG ===
PROBLEM: aita-average-temperature
LANGUAGE: c
BUG: integer_division
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        double avg = (a + b + c) / 3.0;
        printf("%.2f\n", avg);
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
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        double avg = (a + b + c) / 3;
        printf("%.2f\n", avg);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-benches-needed
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, k;
        scanf("%d %d", &n, &k);
        int benches = (n + k - 1) / k;
        printf("%d\n", benches);
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
        int n, k;
        scanf("%d %d", &n, &k);
        int benches = (n + k) / k;
        printf("%d\n", benches);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-bill-total
LANGUAGE: c
BUG: integer_division
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int r, p, q;
        scanf("%d %d %d", &r, &p, &q);
        int total = (r * 100 + p) * q;
        printf("%d.%02d\n", total / 100, total % 100);
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
        int r, p, q;
        scanf("%d %d %d", &r, &p, &q);
        int total = (r + p / 100) * 100 * q;
        printf("%d.%02d\n", total / 100, total % 100);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-benches-needed
LANGUAGE: cpp
BUG: empty_input_unhandled
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, k;
        cin >> n >> k;
        int benches = (n + k - 1) / k;
        cout << benches << endl;
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
        int n, k;
        cin >> n >> k;
        int benches = (n - 1) / k + 1;
        cout << benches << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-average-temperature
LANGUAGE: cpp
BUG: integer_division
CORRECT:
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int a, b, c;
        cin >> a >> b >> c;
        cout << fixed << setprecision(2) << (a + b + c) / 3.0 << endl;
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
        int a, b, c;
        cin >> a >> b >> c;
        cout << fixed << setprecision(2) << (a + b + c) / 3 << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-show-duration
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int sh, sm, eh, em;
        cin >> sh >> sm >> eh >> em;
        int d = (eh * 60 + em) - (sh * 60 + sm);
        if (d < 0) {
            d += 1440;
        }
        cout << d / 60 << " " << d % 60 << endl;
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
        int sh, sm, eh, em;
        cin >> sh >> sm >> eh >> em;
        int d = (eh * 60 + em) - (sh * 60 + sm);
        if (d <= 0) {
            d += 1440;
        }
        cout << d / 60 << " " << d % 60 << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-reverse-three
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    hundreds = n // 100
    tens = n // 10 % 10
    units = n % 10
    print(units * 100 + tens * 10 + hundreds)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    hundreds = n / 100
    tens = n // 10 % 10
    units = n % 10
    print(units * 100 + tens * 10 + hundreds)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-benches-needed
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    print((n + k - 1) // k)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    print(n // k + 1)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-show-duration
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    sh, sm, eh, em = map(int, input().split())
    d = (eh * 60 + em - (sh * 60 + sm)) % 1440
    hours = d // 60
    minutes = d % 60
    print(hours, minutes)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    sh, sm, eh, em = map(int, input().split())
    d = (eh * 60 + em - (sh * 60 + sm)) % 1440
    hours = d / 60
    minutes = d % 60
    print(hours, minutes)
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-284
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    prime = n >= 2
    d = 2
    while d * d <= n:
        if n % d == 0:
            prime = False
            break
        d += 1
    print("Prime" if prime else "Composite")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    prime = n > 2
    d = 2
    while d * d <= n:
        if n % d == 0:
            prime = False
            break
        d += 1
    print("Prime" if prime else "Composite")
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
print(10 / 4)
```
OPTIONS:
A) 2 || integer_division
B) 2.5 || correct
C) 2.50 || none
D) 3 || none
EXPLANATION: In Python, / always gives the exact result as a float, so 10 / 4 is 2.5.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
print(int("12") + int("3"), "12" + "3")
```
OPTIONS:
A) 15 15 || none
B) 123 123 || none
C) 15 123 || correct
D) 123 15 || none
EXPLANATION: int() turns the text into numbers that add to 15, while + on two strings joins them into "123".
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
print(-7 // 2, -7 % 2)
```
OPTIONS:
A) -3 -1 || integer_division
B) -3 1 || none
C) -4 -1 || none
D) -4 1 || correct
EXPLANATION: Python's // rounds down towards minus infinity, so -7 // 2 is -4, and the remainder -7 - (-4 * 2) is 1.
=== END ===
