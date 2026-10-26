# Conditionals

=== PROBLEM ===
ID: aita-max-of-three
DIFFICULTY: easy
STATEMENT: A single line contains three integers a, b and c separated by spaces. Print the largest of them.
CONSTRAINTS: Each integer is between -1000 and 1000.
REFERENCE:
```python
import sys

lines = sys.stdin.read().split("\n")
t = int(lines[0])
for k in range(1, t + 1):
    a, b, c = map(int, lines[k].split())
    print(max(a, b, c))
```
TESTS:
### input
1 2 3
### output
3
### input
3 2 1
### output
3
### input
2 3 1
### output
3
### input
5 5 2
### output
5
### input
-1 -5 -3
### output
-1
### input
7 7 7
### output
7
=== END ===

=== PROBLEM ===
ID: aita-leap-year
DIFFICULTY: easy
STATEMENT: A single line contains a year y. Print YES if y is a leap year and NO otherwise. A year is a leap year if it divides by 4, except that a year dividing by 100 is a leap year only when it also divides by 400.
CONSTRAINTS: 1 <= y <= 10000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    y = int(data[k])
    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    print("YES" if leap else "NO")
```
TESTS:
### input
2024
### output
YES
### input
2023
### output
NO
### input
1900
### output
NO
### input
2000
### output
YES
### input
2100
### output
NO
### input
1600
### output
YES
=== END ===

=== PROBLEM ===
ID: aita-letter-grade
DIFFICULTY: easy
STATEMENT: A single line contains an integer score. Print A for a score of 90 or more, B for 80 to 89, C for 70 to 79, D for 60 to 69, and F for anything below 60.
CONSTRAINTS: 0 <= score <= 100.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    score = int(data[k])
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 70:
        print("C")
    elif score >= 60:
        print("D")
    else:
        print("F")
```
TESTS:
### input
95
### output
A
### input
90
### output
A
### input
80
### output
B
### input
75
### output
C
### input
60
### output
D
### input
59
### output
F
### input
0
### output
F
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int x = 7;
    if (x > 5) {
        printf("big\n");
    } else {
        printf("small\n");
    }
    return 0;
}
```
OPTIONS:
A) small || none
B) big || correct
C) big small || none
D) Nothing is printed || none
EXPLANATION: 7 > 5 is true, so only the if block runs.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int n = 0;
    if (n) {
        printf("yes\n");
    } else {
        printf("no\n");
    }
    return 0;
}
```
OPTIONS:
A) no || correct
B) yes || none
C) 0 || none
D) Nothing is printed || none
EXPLANATION: In C a condition is false when its value is 0 and true for any other value, so n = 0 picks the else block.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a = 3;
    if (a = 0) {
        printf("zero\n");
    } else {
        printf("%d\n", a);
    }
    return 0;
}
```
OPTIONS:
A) zero || wrong_comparison_operator
B) 3 || wrong_comparison_operator
C) 0 || correct
D) Nothing is printed || none
EXPLANATION: a = 0 is an assignment, not a comparison: it stores 0 in a and the condition's value is 0 (false), so the else block prints the new a.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int x = 5, y = 10;
    if (x > 3 && y < 5) {
        printf("A\n");
    } else if (x > 3 || y < 5) {
        printf("B\n");
    } else {
        printf("C\n");
    }
    return 0;
}
```
OPTIONS:
A) A || none
B) C || none
C) A B || none
D) B || correct
EXPLANATION: y < 5 is false, so the && condition fails; the || condition only needs x > 3, so B is printed.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int d = 2;
    switch (d) {
        case 1:
            printf("one ");
        case 2:
            printf("two ");
        case 3:
            printf("three ");
        default:
            printf("other");
    }
    printf("\n");
    return 0;
}
```
OPTIONS:
A) two || none
B) two other || none
C) two three other || correct
D) one two three other || none
EXPLANATION: Without break, a switch keeps running every case after the one that matched, so it falls through from case 2 to the end.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a = 5, b = 2;
    if (a > 3)
        if (b > 3)
            printf("X\n");
        else
            printf("Y\n");
    return 0;
}
```
OPTIONS:
A) X || none
B) Y || correct
C) Nothing is printed || none
D) X Y || none
EXPLANATION: An else belongs to the nearest if without an else, here if (b > 3); a > 3 is true and b > 3 is false, so Y is printed.
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
    int age = 18;
    cout << (age >= 18 ? "adult" : "minor") << endl;
    return 0;
}
```
OPTIONS:
A) minor || wrong_comparison_operator
B) adult || correct
C) 1 || none
D) adultminor || none
EXPLANATION: The ?: operator picks the first value when the condition is true, and 18 >= 18 is true.
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
    int n = 15;
    if (n % 3 == 0 && n % 5 == 0) {
        cout << "both" << endl;
    } else if (n % 3 == 0) {
        cout << "three" << endl;
    } else {
        cout << "neither" << endl;
    }
    return 0;
}
```
OPTIONS:
A) three || none
B) both three || none
C) neither || none
D) both || correct
EXPLANATION: 15 divides by both 3 and 5, so the first block runs and the rest of the chain is skipped.
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
    bool flag = 5 > 3 && 2 > 4;
    cout << flag << endl;
    return 0;
}
```
OPTIONS:
A) false || none
B) 1 || none
C) 0 || correct
D) true || none
EXPLANATION: 2 > 4 is false, so the && is false, and cout prints a false bool as 0.
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
    int x = 10;
    if (x > 5) {
        cout << "A";
    }
    if (x > 8) {
        cout << "B";
    } else {
        cout << "C";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) A || none
B) AB || correct
C) ABC || none
D) AC || none
EXPLANATION: These are two separate if statements: both conditions are true, so A and then B are printed; the else belongs only to the second if.
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
    char g = 'B';
    switch (g) {
        case 'A':
            cout << "excellent";
            break;
        case 'B':
        case 'C':
            cout << "good";
            break;
        default:
            cout << "try again";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) good || correct
B) excellent || none
C) goodtry again || none
D) try again || none
EXPLANATION: case 'B' has no code of its own, so it runs on into case 'C', prints good, and break leaves the switch.
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
    int a = 0;
    if (a == 0 || 10 / a > 1) {
        cout << "safe" << endl;
    } else {
        cout << "unsafe" << endl;
    }
    return 0;
}
```
OPTIONS:
A) unsafe || none
B) The program crashes dividing by zero || none
C) safe || correct
D) Nothing is printed || none
EXPLANATION: || stops as soon as its left side is true, so 10 / a is never evaluated.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
x = 0
if x:
    print("truthy")
else:
    print("falsy")
```
OPTIONS:
A) truthy || none
B) 0 || none
C) falsy || correct
D) Nothing is printed || none
EXPLANATION: The number 0 counts as false in a condition, so the else block runs.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
x = 5
print(1 < x < 10, 10 < x < 20)
```
OPTIONS:
A) True True || none
B) True False || correct
C) False False || none
D) 1 0 || none
EXPLANATION: A chained comparison like 1 < x < 10 means 1 < x and x < 10; 5 is between 1 and 10 but not between 10 and 20.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
a = 15
if a > 10:
    print("A", end=" ")
elif a > 5:
    print("B", end=" ")
if a > 12:
    print("C")
```
OPTIONS:
A) A B C || none
B) A || none
C) C || none
D) A C || correct
EXPLANATION: In the if/elif chain only the first true branch runs, printing A; the second if is a separate statement, and 15 > 12, so C follows.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
An if / else-if / else chain has several conditions that are all true. How many of its blocks run?
OPTIONS:
A) Every block whose condition is true || none
B) Only the first block whose condition is true || correct
C) Only the last block whose condition is true || none
D) None of them, because the conditions conflict || none
EXPLANATION: The chain is checked top to bottom and stops at the first true condition; the rest are skipped.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
Which condition is true exactly when a number n is between 1 and 10, including 1 and 10?
OPTIONS:
A) n >= 1 AND n <= 10 || correct
B) n >= 1 OR n <= 10 || none
C) n > 1 AND n < 10 || off_by_one
D) n >= 1 AND n >= 10 || wrong_comparison_operator
EXPLANATION: Both limits must hold at once, so AND is needed, and >= / <= include the end points.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A program checks the condition A AND B, and A turns out to be false. What does it know about the whole condition before looking at B?
OPTIONS:
A) Nothing yet; it depends on B || none
B) It is true || none
C) It is false || correct
D) It is an error to stop before checking B || none
EXPLANATION: AND needs both sides to be true, so one false side settles it; most languages skip B in this case.
=== END ===

=== DEBUG ===
PROBLEM: aita-max-of-three
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    print(largest)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    largest = 0
    if a > largest:
        largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    print(largest)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-max-of-three
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        int largest;
        if (a >= b && a >= c) {
            largest = a;
        } else if (b >= a && b >= c) {
            largest = b;
        } else {
            largest = c;
        }
        printf("%d\n", largest);
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
        int largest;
        if (a > b && a > c) {
            largest = a;
        } else if (b > a && b > c) {
            largest = b;
        } else {
            largest = c;
        }
        printf("%d\n", largest);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-max-of-three
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
        int a, b, c;
        cin >> a >> b >> c;
        int largest = a;
        if (b > largest) {
            largest = b;
        }
        if (c > largest) {
            largest = c;
        }
        cout << largest << endl;
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
        int a, b, c;
        cin >> a >> b >> c;
        int largest = a;
        if (b < largest) {
            largest = b;
        }
        if (c > largest) {
            largest = c;
        }
        cout << largest << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-leap-year
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    y = int(input())
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        print("YES")
    else:
        print("NO")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    y = int(input())
    if (y % 4 == 0 and y % 100 == 0) or y % 400 == 0:
        print("YES")
    else:
        print("NO")
```
=== END ===

=== DEBUG ===
PROBLEM: aita-leap-year
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int y;
        scanf("%d", &y);
        if ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) {
            printf("YES\n");
        } else {
            printf("NO\n");
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
        int y;
        scanf("%d", &y);
        if ((y % 4 == 0 && y % 100 != 0) || y % 400 != 0) {
            printf("YES\n");
        } else {
            printf("NO\n");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-leap-year
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
        int y;
        cin >> y;
        bool leap = false;
        if (y % 400 == 0) {
            leap = true;
        } else if (y % 100 == 0) {
            leap = false;
        } else if (y % 4 == 0) {
            leap = true;
        }
        cout << (leap ? "YES" : "NO") << endl;
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
        int y;
        cin >> y;
        bool leap = true;
        if (y % 400 == 0) {
            leap = true;
        } else if (y % 100 == 0) {
            leap = false;
        } else if (y % 4 == 0) {
            leap = true;
        }
        cout << (leap ? "YES" : "NO") << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-letter-grade
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    score = int(input())
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 70:
        print("C")
    elif score >= 60:
        print("D")
    else:
        print("F")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    score = int(input())
    if score > 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 70:
        print("C")
    elif score >= 60:
        print("D")
    else:
        print("F")
```
=== END ===

=== DEBUG ===
PROBLEM: aita-letter-grade
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int score;
        scanf("%d", &score);
        if (score >= 90) {
            printf("A\n");
        } else if (score >= 80) {
            printf("B\n");
        } else if (score >= 70) {
            printf("C\n");
        } else if (score >= 60) {
            printf("D\n");
        } else {
            printf("F\n");
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
        int score;
        scanf("%d", &score);
        if (score >= 90) {
            printf("A\n");
        } else if (score >= 80) {
            printf("B\n");
        } else if (score >= 70) {
            printf("C\n");
        } else if (score >= 61) {
            printf("D\n");
        } else {
            printf("F\n");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-letter-grade
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
        int score;
        cin >> score;
        char grade;
        if (score >= 90) {
            grade = 'A';
        } else if (score >= 80) {
            grade = 'B';
        } else if (score >= 70) {
            grade = 'C';
        } else if (score >= 60) {
            grade = 'D';
        } else {
            grade = 'F';
        }
        cout << grade << endl;
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
        int score;
        cin >> score;
        char grade;
        if (score >= 90) {
            grade = 'A';
        } else if (score > 80) {
            grade = 'B';
        } else if (score >= 70) {
            grade = 'C';
        } else if (score >= 60) {
            grade = 'D';
        } else {
            grade = 'F';
        }
        cout << grade << endl;
    }
    return 0;
}
```
=== END ===

=== PROBLEM ===
ID: aita-ticket-price
DIFFICULTY: easy
STATEMENT: A single line contains two integers: a visitor's age and s, which is 1 if the visitor is a student and 0 if not. A museum ticket costs 0 for children under 5, 100 for ages 5 to 17, 200 for ages 18 to 59, and 120 for ages 60 and above. Students aged 18 to 25 pay 150 instead of 200. Print the ticket price.
CONSTRAINTS: 0 <= age <= 120. s is 0 or 1.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    age, s = int(data[pos]), int(data[pos + 1])
    pos += 2
    if age < 5:
        price = 0
    elif age < 18:
        price = 100
    elif age < 60:
        price = 150 if s == 1 and age <= 25 else 200
    else:
        price = 120
    print(price)
```
TESTS:
### input
3 0
### output
0
### input
4 1
### output
0
### input
5 0
### output
100
### input
17 1
### output
100
### input
18 0
### output
200
### input
18 1
### output
150
### input
25 1
### output
150
### input
26 1
### output
200
### input
59 0
### output
200
### input
60 1
### output
120
### input
90 0
### output
120
=== END ===

=== PROBLEM ===
ID: aita-point-quadrant
DIFFICULTY: easy
STATEMENT: A single line contains two integers x and y, the coordinates of a point. Print ORIGIN if the point is (0, 0), X-AXIS if it lies on the x-axis but is not the origin, and Y-AXIS if it lies on the y-axis but is not the origin. Otherwise print the quadrant it is in: Q1 when x > 0 and y > 0, Q2 when x < 0 and y > 0, Q3 when x < 0 and y < 0, and Q4 when x > 0 and y < 0.
CONSTRAINTS: -1000000000 <= x, y <= 1000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    x, y = int(data[pos]), int(data[pos + 1])
    pos += 2
    if x == 0 and y == 0:
        print("ORIGIN")
    elif y == 0:
        print("X-AXIS")
    elif x == 0:
        print("Y-AXIS")
    elif x > 0 and y > 0:
        print("Q1")
    elif x < 0 and y > 0:
        print("Q2")
    elif x < 0:
        print("Q3")
    else:
        print("Q4")
```
TESTS:
### input
3 4
### output
Q1
### input
-3 4
### output
Q2
### input
-3 -4
### output
Q3
### input
3 -4
### output
Q4
### input
0 0
### output
ORIGIN
### input
5 0
### output
X-AXIS
### input
-5 0
### output
X-AXIS
### input
0 7
### output
Y-AXIS
### input
0 -7
### output
Y-AXIS
### input
1000000000 -1000000000
### output
Q4
=== END ===

=== PROBLEM ===
ID: aita-triangle-kind
DIFFICULTY: medium
STATEMENT: A single line contains three integers a, b and c, the lengths of three sticks. The sticks form a triangle only if every pair of sticks is longer in total than the third stick. Print INVALID if they do not form a triangle. Otherwise print EQUILATERAL if all three lengths are equal, ISOSCELES if exactly two are equal, and SCALENE if all three are different.
CONSTRAINTS: 1 <= a, b, c <= 1000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    a, b, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
    pos += 3
    if a + b <= c or a + c <= b or b + c <= a:
        print("INVALID")
    elif a == b == c:
        print("EQUILATERAL")
    elif a == b or b == c or a == c:
        print("ISOSCELES")
    else:
        print("SCALENE")
```
TESTS:
### input
3 4 5
### output
SCALENE
### input
5 5 5
### output
EQUILATERAL
### input
5 5 8
### output
ISOSCELES
### input
8 5 5
### output
ISOSCELES
### input
5 8 5
### output
ISOSCELES
### input
1 2 3
### output
INVALID
### input
1 10 2
### output
INVALID
### input
10 1 1
### output
INVALID
### input
2 2 4
### output
INVALID
### input
1000000 1000000 1
### output
ISOSCELES
### input
2 3 4
### output
SCALENE
=== END ===

=== PROBLEM ===
ID: aita-electricity-bill
DIFFICULTY: medium
STATEMENT: A single line contains u, the number of electricity units a house used. The bill is worked out in slabs: each of the first 100 units costs 3, each unit from 101 to 200 costs 5, and each unit above 200 costs 8. If this total is more than 5000, a surcharge of one tenth of the total (rounded down) is added to it. Print the final bill.
CONSTRAINTS: 0 <= u <= 1000000. The answer fits in a 32-bit integer.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    u = int(data[k])
    if u <= 100:
        bill = u * 3
    elif u <= 200:
        bill = 300 + (u - 100) * 5
    else:
        bill = 800 + (u - 200) * 8
    if bill > 5000:
        bill += bill // 10
    print(bill)
```
TESTS:
### input
0
### output
0
### input
1
### output
3
### input
100
### output
300
### input
101
### output
305
### input
150
### output
550
### input
200
### output
800
### input
201
### output
808
### input
725
### output
5000
### input
726
### output
5508
### input
1000
### output
7920
### input
1000000
### output
8799120
=== END ===

=== PROBLEM ===
ID: aita-next-date
DIFFICULTY: hard
STATEMENT: A single line contains a valid date as three integers d, m and y (day, month, year). Print the date of the next day in the same form: d, m and y separated by single spaces, with no leading zeros. April, June, September and November have 30 days; February has 29 days in a leap year and 28 otherwise; every other month has 31 days. A year is a leap year if it divides by 4, except that a year dividing by 100 is a leap year only when it also divides by 400.
CONSTRAINTS: 1 <= y <= 9998. The input is always a real date.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    d, m, y = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
    pos += 3
    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    if m == 2:
        days = 29 if leap else 28
    elif m in (4, 6, 9, 11):
        days = 30
    else:
        days = 31
    if d < days:
        d += 1
    elif m < 12:
        d, m = 1, m + 1
    else:
        d, m, y = 1, 1, y + 1
    print(d, m, y)
```
TESTS:
### input
15 6 2023
### output
16 6 2023
### input
30 6 2023
### output
1 7 2023
### input
30 1 2023
### output
31 1 2023
### input
31 1 2024
### output
1 2 2024
### input
30 11 2023
### output
1 12 2023
### input
28 2 2024
### output
29 2 2024
### input
29 2 2024
### output
1 3 2024
### input
28 2 2023
### output
1 3 2023
### input
28 2 1900
### output
1 3 1900
### input
28 2 2000
### output
29 2 2000
### input
31 12 2023
### output
1 1 2024
=== END ===

=== DEBUG ===
PROBLEM: aita-ticket-price
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int age, s;
        scanf("%d %d", &age, &s);
        int price;
        if (age < 5) {
            price = 0;
        } else if (age < 18) {
            price = 100;
        } else if (age < 60) {
            if (s == 1 && age <= 25) {
                price = 150;
            } else {
                price = 200;
            }
        } else {
            price = 120;
        }
        printf("%d\n", price);
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
        int age, s;
        scanf("%d %d", &age, &s);
        int price;
        if (age < 5) {
            price = 0;
        } else if (age <= 18) {
            price = 100;
        } else if (age < 60) {
            if (s == 1 && age <= 25) {
                price = 150;
            } else {
                price = 200;
            }
        } else {
            price = 120;
        }
        printf("%d\n", price);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-triangle-kind
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        if (a + b <= c || a + c <= b || b + c <= a) {
            printf("INVALID\n");
        } else if (a == b && b == c) {
            printf("EQUILATERAL\n");
        } else if (a == b || b == c || a == c) {
            printf("ISOSCELES\n");
        } else {
            printf("SCALENE\n");
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
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        if (a + b < c || a + c < b || b + c < a) {
            printf("INVALID\n");
        } else if (a == b && b == c) {
            printf("EQUILATERAL\n");
        } else if (a == b || b == c || a == c) {
            printf("ISOSCELES\n");
        } else {
            printf("SCALENE\n");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-next-date
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int d, m, y;
        scanf("%d %d %d", &d, &m, &y);
        int leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        int days;
        if (m == 2) {
            days = leap ? 29 : 28;
        } else if (m == 4 || m == 6 || m == 9 || m == 11) {
            days = 30;
        } else {
            days = 31;
        }
        d++;
        if (d > days) {
            d = 1;
            m++;
            if (m > 12) {
                m = 1;
                y++;
            }
        }
        printf("%d %d %d\n", d, m, y);
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
        int d, m, y;
        scanf("%d %d %d", &d, &m, &y);
        int leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        int days;
        if (m == 2) {
            days = leap ? 29 : 28;
        } else if (m == 4 || m == 6 || m == 9 || m == 11) {
            days = 30;
        } else {
            days = 31;
        }
        d++;
        if (d > days) {
            d = 1;
            m++;
            if (m >= 12) {
                m = 1;
                y++;
            }
        }
        printf("%d %d %d\n", d, m, y);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-point-quadrant
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
        int x, y;
        cin >> x >> y;
        if (x > 0 && y > 0) {
            cout << "Q1" << endl;
        } else if (x < 0 && y > 0) {
            cout << "Q2" << endl;
        } else if (x < 0 && y < 0) {
            cout << "Q3" << endl;
        } else if (x > 0 && y < 0) {
            cout << "Q4" << endl;
        } else if (x == 0 && y == 0) {
            cout << "ORIGIN" << endl;
        } else if (y == 0) {
            cout << "X-AXIS" << endl;
        } else {
            cout << "Y-AXIS" << endl;
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
        int x, y;
        cin >> x >> y;
        if (x >= 0 && y > 0) {
            cout << "Q1" << endl;
        } else if (x < 0 && y > 0) {
            cout << "Q2" << endl;
        } else if (x < 0 && y < 0) {
            cout << "Q3" << endl;
        } else if (x > 0 && y < 0) {
            cout << "Q4" << endl;
        } else if (x == 0 && y == 0) {
            cout << "ORIGIN" << endl;
        } else if (y == 0) {
            cout << "X-AXIS" << endl;
        } else {
            cout << "Y-AXIS" << endl;
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-electricity-bill
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
        long long u;
        cin >> u;
        long long bill;
        if (u <= 100) {
            bill = u * 3;
        } else if (u <= 200) {
            bill = 300 + (u - 100) * 5;
        } else {
            bill = 800 + (u - 200) * 8;
        }
        if (bill > 5000) {
            bill += bill / 10;
        }
        cout << bill << endl;
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
        long long u;
        cin >> u;
        long long bill;
        if (u <= 100) {
            bill = u * 3;
        } else if (u <= 200) {
            bill = 300 + (u - 101) * 5;
        } else {
            bill = 800 + (u - 200) * 8;
        }
        if (bill > 5000) {
            bill += bill / 10;
        }
        cout << bill << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-next-date
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
        int d, m, y;
        cin >> d >> m >> y;
        bool leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        int days = 31;
        if (m == 2) {
            days = leap ? 29 : 28;
        } else if (m == 4 || m == 6 || m == 9 || m == 11) {
            days = 30;
        }
        if (d < days) {
            d++;
        } else {
            d = 1;
            if (m == 12) {
                m = 1;
                y++;
            } else {
                m++;
            }
        }
        cout << d << " " << m << " " << y << endl;
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
        int d, m, y;
        cin >> d >> m >> y;
        bool leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        int days = 31;
        if (m == 2) {
            days = leap ? 29 : 28;
        } else if (m == 4 || m == 6 || m == 9 || m == 11) {
            days = 30;
        }
        if (d <= days) {
            d++;
        } else {
            d = 1;
            if (m == 12) {
                m = 1;
                y++;
            } else {
                m++;
            }
        }
        cout << d << " " << m << " " << y << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-point-quadrant
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    if x == 0 and y == 0:
        print("ORIGIN")
    elif y == 0:
        print("X-AXIS")
    elif x == 0:
        print("Y-AXIS")
    elif x > 0:
        print("Q1" if y > 0 else "Q4")
    else:
        print("Q2" if y > 0 else "Q3")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    if x == 0 and y == 0:
        print("ORIGIN")
    elif y == 0:
        print("X-AXIS")
    elif x == 0:
        print("Y-AXIS")
    elif x < 0:
        print("Q1" if y > 0 else "Q4")
    else:
        print("Q2" if y > 0 else "Q3")
```
=== END ===

=== DEBUG ===
PROBLEM: aita-triangle-kind
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    if a + b <= c or a + c <= b or b + c <= a:
        print("INVALID")
        continue
    kind = "SCALENE"
    if a == b or b == c or a == c:
        kind = "ISOSCELES"
    if a == b and b == c:
        kind = "EQUILATERAL"
    print(kind)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    if a + b <= c or a + c <= b or b + c <= a:
        print("INVALID")
        continue
    kind = "ISOSCELES"
    if a == b or b == c or a == c:
        kind = "ISOSCELES"
    if a == b and b == c:
        kind = "EQUILATERAL"
    print(kind)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-ticket-price
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    age, s = map(int, input().split())
    if age < 5:
        print(0)
    elif age <= 17:
        print(100)
    elif age >= 60:
        print(120)
    elif s == 1 and age <= 25:
        print(150)
    else:
        print(200)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    age, s = map(int, input().split())
    if age < 5:
        print(0)
    elif age <= 17:
        print(100)
    elif age >= 60:
        print(120)
    elif s == 1 and age < 25:
        print(150)
    else:
        print(200)
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
temp = 30
if temp > 30:
    print("hot")
elif temp > 20:
    print("warm")
else:
    print("cold")
```
OPTIONS:
A) hot || wrong_comparison_operator
B) warm || correct
C) cold || none
D) hot warm || none
EXPLANATION: 30 > 30 is false because > does not include the equal value, so the chain moves on and 30 > 20 picks warm.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
n = 12
label = "even"
if n % 2 == 0:
    if n % 3 == 0:
        label += " six"
    elif n % 4 == 0:
        label += " four"
else:
    label = "odd"
print(label)
```
OPTIONS:
A) even six four || none
B) even four || none
C) even six || correct
D) odd || none
EXPLANATION: 12 is even and divides by 3, so the inner if adds six and its elif is skipped even though 12 also divides by 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
x = 0
y = 7
print(x or y, x and y)
```
OPTIONS:
A) True False || none
B) 0 7 || none
C) True 0 || none
D) 7 0 || correct
EXPLANATION: Python's or gives back the first truthy value (7) and and gives back the first falsy value (0), not True or False.
=== END ===
