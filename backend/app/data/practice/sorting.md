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

=== PROBLEM ===
ID: aita-sort-kth-smallest
DIFFICULTY: easy
STATEMENT: The first line contains two integers n and k. The second line contains n space-separated integers. Print the k-th smallest of them, counting repeated values separately, so k = 1 means the smallest value and k = n the largest.
CONSTRAINTS: 1 <= k <= n <= 1000; each integer is between -100000 and 100000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n, k = int(data[pos]), int(data[pos + 1])
    values = sorted(map(int, data[pos + 2:pos + 2 + n]))
    pos += 2 + n
    print(values[k - 1])
```
TESTS:
### input
5 2
7 3 9 3 1
### output
3
### input
1 1
-4
### output
-4
### input
6 6
1 2 3 4 5 6
### output
6
### input
5 3
50 40 30 20 10
### output
30
### input
4 4
2 2 2 2
### output
2
### input
6 2
-5 0 -100000 100000 -5 3
### output
-5
### input
7 4
12 -3 8 -3 0 15 4
### output
4
=== END ===

=== PROBLEM ===
ID: aita-sort-unique-values
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. Print every different value exactly once, in ascending order, separated by single spaces.
CONSTRAINTS: 1 <= n <= 1000; each integer is between -100000 and 100000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = sorted(set(map(int, data[pos + 1:pos + 1 + n])))
    pos += 1 + n
    print(" ".join(map(str, values)))
```
TESTS:
### input
6
4 1 4 2 1 4
### output
1 2 4
### input
1
0
### output
0
### input
5
-3 -1 0 2 5
### output
-3 -1 0 2 5
### input
5
9 9 9 9 9
### output
9
### input
6
10 8 6 4 2 0
### output
0 2 4 6 8 10
### input
7
0 -7 0 3 -7 3 100000
### output
-7 0 3 100000
=== END ===

=== PROBLEM ===
ID: aita-sort-min-gap
DIFFICULTY: medium
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. Choose two of them at different positions so that the absolute difference between them is as small as possible, and print that difference. If some value appears twice, the answer is 0.
CONSTRAINTS: 2 <= n <= 1000; each integer is between -100000 and 100000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = sorted(map(int, data[pos + 1:pos + 1 + n]))
    pos += 1 + n
    print(min(values[i] - values[i - 1] for i in range(1, n)))
```
TESTS:
### input
5
10 3 7 20 1
### output
2
### input
2
-5 5
### output
10
### input
4
1 4 9 16
### output
3
### input
5
40 30 25 10 -2
### output
5
### input
6
8 -1 6 8 100 -50
### output
0
### input
3
-100000 100000 0
### output
100000
### input
5
100 1 50 25 99
### output
1
=== END ===

=== PROBLEM ===
ID: aita-sort-rank-by-score
DIFFICULTY: medium
STATEMENT: The first line contains an integer n, the number of players, who are numbered 1 to n in input order. The second line contains their n scores. Print the player numbers ordered from the highest score to the lowest, separated by single spaces. Players with equal scores are listed with the smaller player number first.
CONSTRAINTS: 1 <= n <= 1000; each score is between 0 and 1000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    scores = list(map(int, data[pos + 1:pos + 1 + n]))
    pos += 1 + n
    order = sorted(range(1, n + 1), key=lambda p: (-scores[p - 1], p))
    print(" ".join(map(str, order)))
```
TESTS:
### input
4
30 50 30 10
### output
2 1 3 4
### input
1
99
### output
1
### input
5
5 4 3 2 1
### output
1 2 3 4 5
### input
5
1 2 3 4 5
### output
5 4 3 2 1
### input
6
7 7 7 7 7 7
### output
1 2 3 4 5 6
### input
6
0 1000000 20 0 1000000 20
### output
2 5 3 6 1 4
=== END ===

=== PROBLEM ===
ID: aita-sort-by-frequency
DIFFICULTY: hard
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. Rearrange them so that values occurring more often come first, and values occurring the same number of times come from smallest to largest; all copies of a value stay next to each other. Print the n rearranged integers separated by single spaces.
CONSTRAINTS: 1 <= n <= 1000; each integer is between -1000 and 1000.
REFERENCE:
```python
import sys
from collections import Counter

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = list(map(int, data[pos + 1:pos + 1 + n]))
    pos += 1 + n
    count = Counter(values)
    values.sort(key=lambda v: (-count[v], v))
    print(" ".join(map(str, values)))
```
TESTS:
### input
7
4 6 4 2 6 4 9
### output
4 4 4 6 6 2 9
### input
1
-8
### output
-8
### input
5
1 2 3 4 5
### output
1 2 3 4 5
### input
6
3 3 2 2 1 1
### output
1 1 2 2 3 3
### input
8
-1 5 -1 0 5 -1 0 7
### output
-1 -1 -1 0 0 5 5 7
### input
6
9 8 7 7 8 7
### output
7 7 7 8 8 9
### input
5
1000 -1000 1000 -1000 0
### output
-1000 -1000 1000 1000 0
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-kth-smallest
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
        int a[1000];
        scanf("%d %d", &n, &k);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 1; i < n; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > key) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
        printf("%d\n", a[k - 1]);
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
        int a[1000];
        scanf("%d %d", &n, &k);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        for (int i = 1; i < n; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > key) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
        printf("%d\n", a[k]);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-min-gap
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
        int a[1000];
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
        int best = 200001;
        for (int i = 1; i < n; i++) {
            if (a[i] - a[i - 1] < best) {
                best = a[i] - a[i - 1];
            }
        }
        printf("%d\n", best);
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
        int a[1000];
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
        int best = 0;
        for (int i = 1; i < n; i++) {
            if (a[i] - a[i - 1] < best) {
                best = a[i] - a[i - 1];
            }
        }
        printf("%d\n", best);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-rank-by-score
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
        int s[1000], id[1000];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &s[i]);
            id[i] = i + 1;
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (s[id[j] - 1] < s[id[j + 1] - 1]) {
                    int tmp = id[j];
                    id[j] = id[j + 1];
                    id[j + 1] = tmp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", id[i], i == n - 1 ? "" : " ");
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
        int s[1000], id[1000];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &s[i]);
            id[i] = i + 1;
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (s[id[j] - 1] <= s[id[j + 1] - 1]) {
                    int tmp = id[j];
                    id[j] = id[j + 1];
                    id[j + 1] = tmp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%d%s", id[i], i == n - 1 ? "" : " ");
        }
        printf("\n");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-078
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
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
        for (int i = 1; i < n; i++) {
            int key = v[i];
            int j = i - 1;
            while (j >= 0 && v[j] > key) {
                v[j + 1] = v[j];
                j--;
            }
            v[j + 1] = key;
        }
        for (int i = 0; i < n; i++) {
            cout << (i == 0 ? "" : " ") << v[i];
        }
        cout << "\n";
    }
    return 0;
}
```
BUGGY:
```cpp
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
        for (int i = 1; i < n; i++) {
            int key = v[i];
            int j = i - 1;
            while (j > 0 && v[j] > key) {
                v[j + 1] = v[j];
                j--;
            }
            v[j + 1] = key;
        }
        for (int i = 0; i < n; i++) {
            cout << (i == 0 ? "" : " ") << v[i];
        }
        cout << "\n";
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-unique-values
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <algorithm>
#include <iostream>
#include <string>
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
        int prev = -1000000;
        string sep = "";
        for (int x : v) {
            if (x != prev) {
                cout << sep << x;
                sep = " ";
                prev = x;
            }
        }
        cout << "\n";
    }
    return 0;
}
```
BUGGY:
```cpp
#include <algorithm>
#include <iostream>
#include <string>
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
        int prev = 0;
        string sep = "";
        for (int x : v) {
            if (x != prev) {
                cout << sep << x;
                sep = " ";
                prev = x;
            }
        }
        cout << "\n";
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-by-frequency
LANGUAGE: cpp
BUG: wrong_comparison_operator
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
        vector<int> cnt(2001, 0);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
            cnt[v[i] + 1000]++;
        }
        sort(v.begin(), v.end(), [&](int a, int b) {
            if (cnt[a + 1000] != cnt[b + 1000]) {
                return cnt[a + 1000] > cnt[b + 1000];
            }
            return a < b;
        });
        for (int i = 0; i < n; i++) {
            cout << v[i] << (i == n - 1 ? "\n" : " ");
        }
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
        vector<int> cnt(2001, 0);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
            cnt[v[i] + 1000]++;
        }
        sort(v.begin(), v.end(), [&](int a, int b) {
            if (cnt[a + 1000] != cnt[b + 1000]) {
                return cnt[a + 1000] > cnt[b + 1000];
            }
            return a > b;
        });
        for (int i = 0; i < n; i++) {
            cout << v[i] << (i == n - 1 ? "\n" : " ");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-kth-smallest
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
        int n, k;
        cin >> n >> k;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        for (int i = 0; i < k; i++) {
            int m = i;
            for (int j = i + 1; j < n; j++) {
                if (v[j] < v[m]) {
                    m = j;
                }
            }
            swap(v[i], v[m]);
        }
        cout << v[k - 1] << "\n";
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
        int n, k;
        cin >> n >> k;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        for (int i = 0; i < k - 1; i++) {
            int m = i;
            for (int j = i + 1; j < n; j++) {
                if (v[j] < v[m]) {
                    m = j;
                }
            }
            swap(v[i], v[m]);
        }
        cout << v[k - 1] << "\n";
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-unique-values
LANGUAGE: python
BUG: mutate_while_iterating
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    for x in a[:]:
        if a.count(x) > 1:
            a.remove(x)
    print(" ".join(map(str, a)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    for x in a:
        if a.count(x) > 1:
            a.remove(x)
    print(" ".join(map(str, a)))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-min-gap
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = sorted(map(int, input().split()))
    best = a[1] - a[0]
    for i in range(2, n):
        best = min(best, a[i] - a[i - 1])
    print(best)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = sorted(map(int, input().split()))
    best = a[1] - a[0]
    for i in range(2, n - 1):
        best = min(best, a[i] - a[i - 1])
    print(best)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-sort-rank-by-score
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def ranking(scores):
    order = sorted(range(1, len(scores) + 1), key=lambda p: (-scores[p - 1], p))
    return " ".join(map(str, order))


t = int(input())
for _ in range(t):
    n = int(input())
    s = list(map(int, input().split()))
    print(ranking(s))
```
BUGGY:
```python
def ranking(scores):
    order = sorted(range(1, len(scores) + 1), key=lambda p: (-scores[p - 1], p))
    print(" ".join(map(str, order)))


t = int(input())
for _ in range(t):
    n = int(input())
    s = list(map(int, input().split()))
    print(ranking(s))
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
nums = [5, 2, 8]
nums.sort(reverse=True)
print(nums[0], nums[-1])
```
OPTIONS:
A) 2 8 || none
B) 8 2 || correct
C) 5 8 || none
D) 8 5 || none
EXPLANATION: reverse=True sorts the list largest first, giving [8, 5, 2], so the first item is 8 and the last is 2.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
pets = ["cat", "ox", "dog", "emu", "be"]
pets.sort(key=len)
print(" ".join(pets))
```
OPTIONS:
A) be ox cat dog emu || none
B) be cat dog emu ox || none
C) ox be cat dog emu || correct
D) cat dog emu ox be || none
EXPLANATION: Python's sort is stable, so words of the same length keep their original order: ox before be, then cat, dog, emu.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
scores = [("ana", 7), ("raj", 9), ("li", 7)]
ranked = sorted(scores, key=lambda p: p[1], reverse=True)
print([name for name, _ in ranked])
```
OPTIONS:
A) ['raj', 'li', 'ana'] || none
B) ['li', 'ana', 'raj'] || none
C) ['ana', 'li', 'raj'] || none
D) ['raj', 'ana', 'li'] || correct
EXPLANATION: reverse=True puts the highest score first but keeps tied items in their original order, so ana stays ahead of li.
=== END ===
