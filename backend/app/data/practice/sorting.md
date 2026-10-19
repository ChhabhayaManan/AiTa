# Sorting

=== PROBLEM ===
ID: aita-sort-descending
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. Print them sorted from largest to smallest, separated by single spaces.
CONSTRAINTS: 1 <= n <= 300; each integer is between -10000 and 10000.
REFERENCE:
```python
import sys

lines = sys.stdin.read().split("\n")
t = int(lines[0])
pos = 1
for _ in range(t):
    n = int(lines[pos])
    values = list(map(int, lines[pos + 1].split()))
    pos += 2
    print(" ".join(map(str, sorted(values, reverse=True))))
```
TESTS:
### input
5
3 1 4 1 5
### output
5 4 3 1 1
### input
1
7
### output
7
### input
4
-2 -8 0 3
### output
3 0 -2 -8
### input
3
2 2 2
### output
2 2 2
### input
6
10 9 8 7 6 5
### output
10 9 8 7 6 5
### input
5
1 2 3 4 5
### output
5 4 3 2 1
=== END ===

=== PROBLEM ===
ID: aita-median
DIFFICULTY: easy
STATEMENT: The first line contains an odd integer n. The second line contains n space-separated integers. Print their median, the middle value once the integers are sorted.
CONSTRAINTS: 1 <= n <= 299 and n is odd; each integer is between -10000 and 10000.
REFERENCE:
```python
import sys

lines = sys.stdin.read().split("\n")
t = int(lines[0])
pos = 1
for _ in range(t):
    n = int(lines[pos])
    values = sorted(map(int, lines[pos + 1].split()))
    pos += 2
    print(values[n // 2])
```
TESTS:
### input
3
3 1 2
### output
2
### input
1
5
### output
5
### input
5
9 1 8 2 7
### output
7
### input
5
4 4 1 4 2
### output
4
### input
7
-3 -1 -2 0 5 6 -10
### output
-1
### input
3
100 -100 0
### output
0
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
This is one pass of bubble sort. What does the program print?
```c
#include <stdio.h>

int main(void) {
    int a[4] = {4, 3, 2, 1};
    for (int j = 0; j < 3; j++) {
        if (a[j] > a[j + 1]) {
            int t = a[j];
            a[j] = a[j + 1];
            a[j + 1] = t;
        }
    }
    printf("%d %d %d %d\n", a[0], a[1], a[2], a[3]);
    return 0;
}
```
OPTIONS:
A) 1 2 3 4 || none
B) 3 4 2 1 || none
C) 3 2 1 4 || correct
D) 1 4 3 2 || none
EXPLANATION: One pass carries the largest value, 4, step by step to the end; the rest are not sorted yet.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[3] = {3, 1, 2};
    int swaps = 0;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2 - i; j++) {
            if (a[j] > a[j + 1]) {
                int t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
                swaps++;
            }
        }
    }
    printf("%d\n", swaps);
    return 0;
}
```
OPTIONS:
A) 1 || none
B) 3 || none
C) 0 || none
D) 2 || correct
EXPLANATION: 3 swaps with 1, then with 2, giving 1 2 3; the second pass finds nothing to swap.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
This is the first step of selection sort. What does the program print?
```c
#include <stdio.h>

int main(void) {
    int a[4] = {5, 2, 8, 1};
    int min = 0;
    for (int j = 1; j < 4; j++) {
        if (a[j] < a[min]) {
            min = j;
        }
    }
    int t = a[0];
    a[0] = a[min];
    a[min] = t;
    printf("%d %d %d %d\n", a[0], a[1], a[2], a[3]);
    return 0;
}
```
OPTIONS:
A) 1 2 8 5 || correct
B) 1 2 5 8 || none
C) 2 5 8 1 || none
D) 1 5 2 8 || none
EXPLANATION: The smallest value, 1, is found and swapped with the first element; nothing else moves.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *x, const void *y) {
    return *(const int *) y - *(const int *) x;
}

int main(void) {
    int a[] = {3, 9, 1};
    qsort(a, 3, sizeof(int), cmp);
    printf("%d %d %d\n", a[0], a[1], a[2]);
    return 0;
}
```
OPTIONS:
A) 1 3 9 || wrong_comparison_operator
B) 9 3 1 || correct
C) 3 9 1 || none
D) 9 1 3 || none
EXPLANATION: The comparator returns y - x, which puts larger values first, so the array is sorted in descending order.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {1, 3, 3, 7};
    int sorted = 1;
    for (int i = 0; i + 1 < 4; i++) {
        if (a[i] > a[i + 1]) {
            sorted = 0;
        }
    }
    printf("%d\n", sorted);
    return 0;
}
```
OPTIONS:
A) 0 || wrong_comparison_operator
B) 3 || none
C) 1 || correct
D) 4 || none
EXPLANATION: No element is greater than the one after it; the two equal 3s do not break the ascending order.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {2, 0, 2, 1, 0};
    int c[3] = {0};
    for (int i = 0; i < 5; i++) {
        c[a[i]]++;
    }
    for (int v = 0; v < 3; v++) {
        for (int k = 0; k < c[v]; k++) {
            printf("%d", v);
        }
    }
    printf("\n");
    return 0;
}
```
OPTIONS:
A) 012 || none
B) 22100 || none
C) 20210 || none
D) 00122 || correct
EXPLANATION: This is counting sort: it counts each value, then prints every value as many times as it was counted, smallest first.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9};
    sort(v.begin(), v.end());
    cout << v[0] << " " << v[2] << endl;
    return 0;
}
```
OPTIONS:
A) 5 9 || none
B) 2 9 || correct
C) 9 2 || none
D) 2 5 || off_by_one
EXPLANATION: sort puts the vector in ascending order, {2, 5, 9}.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <functional>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 3, 2};
    sort(v.begin(), v.end(), greater<int>());
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 3 2 1 || correct
B) 1 2 3 || none
C) 1 3 2 || none
D) 2 3 1 || none
EXPLANATION: greater<int>() tells sort to put larger values first.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> w = {"pear", "apple", "fig"};
    sort(w.begin(), w.end());
    cout << w[0] << " " << w[2] << endl;
    return 0;
}
```
OPTIONS:
A) fig pear || none
B) pear apple || none
C) apple fig || none
D) apple pear || correct
EXPLANATION: Strings sort alphabetically: apple, fig, pear.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> w = {"ccc", "a", "bb"};
    sort(w.begin(), w.end(), [](const string &x, const string &y) {
        return x.size() < y.size();
    });
    cout << w[0] << " " << w[1] << " " << w[2] << endl;
    return 0;
}
```
OPTIONS:
A) ccc bb a || none
B) a bb ccc || correct
C) a ccc bb || none
D) ccc a bb || none
EXPLANATION: The lambda compares lengths, so shorter strings come first.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {4, 3, 2, 1};
    sort(v.begin(), v.begin() + 2);
    for (int x : v) {
        cout << x;
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 1234 || wrong_loop_bound
B) 4321 || none
C) 3421 || correct
D) 3412 || none
EXPLANATION: Only the first two elements, from begin() up to but not including begin() + 2, are sorted.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int main() {
    vector<pair<int, int>> p = {{2, 1}, {1, 5}, {2, 0}};
    sort(p.begin(), p.end());
    cout << p[0].second << p[1].second << p[2].second << endl;
    return 0;
}
```
OPTIONS:
A) 150 || none
B) 501 || correct
C) 510 || none
D) 105 || none
EXPLANATION: Pairs sort by first value, then by second value when the firsts are equal: (1, 5), (2, 0), (2, 1).
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
nums = [3, 1, 2]
print(sorted(nums), nums)
```
OPTIONS:
A) [1, 2, 3] [1, 2, 3] || none
B) [1, 2, 3] [3, 1, 2] || correct
C) [3, 1, 2] [1, 2, 3] || none
D) None [1, 2, 3] || none
EXPLANATION: sorted returns a new sorted list and leaves the original list as it was.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
words = ["bb", "a", "ccc"]
words.sort(key=len, reverse=True)
print(words)
```
OPTIONS:
A) ['a', 'bb', 'ccc'] || none
B) ['ccc', 'bb', 'a'] || correct
C) ['bb', 'a', 'ccc'] || none
D) ['a', 'ccc', 'bb'] || none
EXPLANATION: key=len sorts by length, and reverse=True puts the longest first.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
x = [3, 1, 2].sort()
print(x)
```
OPTIONS:
A) [1, 2, 3] || return_vs_print
B) [3, 1, 2] || none
C) None || correct
D) [] || none
EXPLANATION: list.sort() sorts the list in place and returns None, so x is None.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
Bubble sort, sorting into ascending order, compares two neighbouring elements. When does it swap them?
OPTIONS:
A) When the left one is greater than the right one || correct
B) When the left one is smaller than the right one || wrong_comparison_operator
C) When they are equal || none
D) Always, on every comparison || none
EXPLANATION: A swap is needed only when a pair is out of order; for ascending order that means the left value is larger.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
What does it mean for a sorting method to be stable?
OPTIONS:
A) It never crashes, whatever the input || none
B) It always takes the same time for every input || none
C) Elements that compare as equal keep their original order relative to each other || correct
D) It sorts the data without using any extra memory || none
EXPLANATION: Stability matters when sorting records by one field, for example students by grade, keeping their earlier order within each grade.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A simple sort such as bubble sort or selection sort is used on n elements. Roughly how does the number of comparisons grow with n?
OPTIONS:
A) It stays about the same whatever n is || none
B) It grows about like n || none
C) It grows about like n * n || correct
D) It grows about like 2 to the power n || none
EXPLANATION: These sorts compare each element with most of the others, which is about n * n / 2 comparisons.
=== END ===

=== DEBUG ===
PROBLEM: mbpp-078
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    print(" ".join(map(str, a)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    for i in range(n - 1):
        for j in range(n - 2 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    print(" ".join(map(str, a)))
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-078
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
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            int min = i;
            for (int j = i + 1; j < n; j++) {
                if (a[j] < a[min]) {
                    min = j;
                }
            }
            int tmp = a[i];
            a[i] = a[min];
            a[min] = tmp;
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", a[i], i == n - 1 ? "" : " ");
        }
        printf("\n");
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
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            int min = i;
            for (int j = i + 1; j < n; j++) {
                if (a[j] > a[min]) {
                    min = j;
                }
            }
            int tmp = a[i];
            a[i] = a[min];
            a[min] = tmp;
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", a[i], i == n - 1 ? "" : " ");
        }
        printf("\n");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-descending
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] < key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    print(" ".join(map(str, a)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    print(" ".join(map(str, a)))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-descending
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
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (a[j] < a[j + 1]) {
                    int tmp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = tmp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", a[i], i == n - 1 ? "" : " ");
        }
        printf("\n");
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
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 1; j < n - 1 - i; j++) {
                if (a[j] < a[j + 1]) {
                    int tmp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = tmp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", a[i], i == n - 1 ? "" : " ");
        }
        printf("\n");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-descending
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        for (int i = 0; i < n - 1; i++) {
            int best = i;
            for (int j = i + 1; j < n; j++) {
                if (v[j] > v[best]) {
                    best = j;
                }
            }
            swap(v[i], v[best]);
        }
        for (int i = 0; i < n; i++) {
            cout << v[i] << (i == n - 1 ? "\n" : " ");
        }
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        for (int i = 0; i < n - 1; i++) {
            int best = 0;
            for (int j = i + 1; j < n; j++) {
                if (v[j] > v[best]) {
                    best = j;
                }
            }
            swap(v[i], v[best]);
        }
        for (int i = 0; i < n; i++) {
            cout << v[i] << (i == n - 1 ? "\n" : " ");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-median
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = sorted(map(int, input().split()))
    print(a[n // 2])
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = sorted(map(int, input().split()))
    print(a[n // 2 + 1])
```
=== END ===

=== DEBUG ===
PROBLEM: aita-median
LANGUAGE: c
BUG: wrong_loop_bound
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (a[j] > a[j + 1]) {
                    int tmp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = tmp;
                }
            }
        }
        printf("%d\n", a[n / 2]);
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
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 0; i < 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (a[j] > a[j + 1]) {
                    int tmp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = tmp;
                }
            }
        }
        printf("%d\n", a[n / 2]);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-median
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        sort(v.begin(), v.end());
        cout << v[n / 2] << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        sort(v.begin(), v.begin() + n / 2);
        cout << v[n / 2] << endl;
    }
    return 0;
}
```
=== END ===
