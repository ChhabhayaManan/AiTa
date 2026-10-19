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
