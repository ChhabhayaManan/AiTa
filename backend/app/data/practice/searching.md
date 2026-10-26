# Searching

=== PROBLEM ===
ID: aita-count-occurrences
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. The third line contains an integer target. Print how many of the n integers are equal to target.
CONSTRAINTS: 0 <= n <= 300; every integer is between -1000 and 1000.
REFERENCE:
```python
import sys

lines = sys.stdin.read().split("\n")
t = int(lines[0])
pos = 1
for _ in range(t):
    n = int(lines[pos])
    values = list(map(int, lines[pos + 1].split()))
    target = int(lines[pos + 2])
    pos += 3
    print(values.count(target))
```
TESTS:
### input
5
1 2 2 3 2
2
### output
3
### input
3
1 1 1
1
### output
3
### input
4
5 6 7 8
9
### output
0
### input
0

4
### output
0
### input
1
-3
-3
### output
1
### input
6
4 0 4 0 4 0
0
### output
3
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {7, 3, 9, 3};
    int pos = -1;
    for (int i = 0; i < 4; i++) {
        if (a[i] == 3) {
            pos = i;
            break;
        }
    }
    printf("%d\n", pos);
    return 0;
}
```
OPTIONS:
A) 1 || correct
B) 3 || none
C) 2 || off_by_one
D) -1 || none
EXPLANATION: The loop stops at the first 3, which is at index 1.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {7, 3, 9, 3};
    int pos = -1;
    for (int i = 0; i < 4; i++) {
        if (a[i] == 3) {
            pos = i;
        }
    }
    printf("%d\n", pos);
    return 0;
}
```
OPTIONS:
A) 1 || none
B) 3 || correct
C) 2 || none
D) -1 || none
EXPLANATION: Without a break the loop keeps going, so pos is overwritten by the last match, at index 3.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int lo = 0, hi = 9;
    int mid = lo + (hi - lo) / 2;
    printf("%d\n", mid);
    return 0;
}
```
OPTIONS:
A) 5 || integer_division
B) 4.5 || integer_division
C) 4 || correct
D) 9 || none
EXPLANATION: (9 - 0) / 2 is integer division, giving 4, so the middle index is 4.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
How many times does this binary search loop run before it finds 11?
```c
#include <stdio.h>

int main(void) {
    int a[] = {1, 3, 5, 7, 9, 11};
    int target = 11;
    int lo = 0, hi = 5, steps = 0;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        steps++;
        if (a[mid] == target) {
            break;
        } else if (a[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    printf("%d\n", steps);
    return 0;
}
```
OPTIONS:
A) 6 || none
B) 2 || none
C) 1 || none
D) 3 || correct
EXPLANATION: mid goes 2 (value 5), then 4 (value 9), then 5 (value 11): three steps, each halving the range.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {4, 8, 15, 16, 23};
    int target = 42;
    int checks = 0;
    int found = 0;
    for (int i = 0; i < 5; i++) {
        checks++;
        if (a[i] == target) {
            found = 1;
            break;
        }
    }
    printf("%d %d\n", found, checks);
    return 0;
}
```
OPTIONS:
A) 0 5 || correct
B) 0 4 || off_by_one
C) 1 5 || none
D) 0 0 || none
EXPLANATION: 42 is not in the array, so a linear search has to check all five elements before giving up.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
This binary search finds the first position whose value is at least x. What does it print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {2, 4, 4, 4, 8};
    int x = 4;
    int lo = 0, hi = 5;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] < x) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    printf("%d\n", lo);
    return 0;
}
```
OPTIONS:
A) 2 || none
B) 3 || none
C) 1 || correct
D) 4 || none
EXPLANATION: mid 2 (4) moves hi to 2, mid 1 (4) moves hi to 1, mid 0 (2) moves lo to 1; the first 4 is at index 1.
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
    vector<int> v = {4, 8, 15};
    auto it = find(v.begin(), v.end(), 8);
    cout << (it - v.begin()) << endl;
    return 0;
}
```
OPTIONS:
A) 8 || none
B) 2 || off_by_one
C) 1 || correct
D) 0 || none
EXPLANATION: find returns an iterator to the match; subtracting begin() turns it into the index, 1.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello";
    cout << (s.find('z') == string::npos) << endl;
    return 0;
}
```
OPTIONS:
A) 0 || none
B) 1 || correct
C) -1 || none
D) 5 || none
EXPLANATION: When find has no match it returns string::npos, so the comparison is true and prints as 1.
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
    vector<int> v = {1, 3, 5, 7};
    cout << binary_search(v.begin(), v.end(), 7)
         << binary_search(v.begin(), v.end(), 4) << endl;
    return 0;
}
```
OPTIONS:
A) 10 || correct
B) 01 || none
C) 11 || none
D) 30 || none
EXPLANATION: binary_search only reports whether the value is present: 7 is, 4 is not.
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
    vector<int> v = {10, 20, 30, 40};
    cout << lower_bound(v.begin(), v.end(), 25) - v.begin() << endl;
    return 0;
}
```
OPTIONS:
A) 1 || off_by_one
B) 25 || none
C) 30 || none
D) 2 || correct
EXPLANATION: lower_bound points at the first element not less than 25, which is 30 at index 2.
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
    vector<int> v = {2, 1, 2, 2};
    cout << count(v.begin(), v.end(), 2) << endl;
    return 0;
}
```
OPTIONS:
A) 2 || none
B) 3 || correct
C) 1 || none
D) 0 || none
EXPLANATION: count checks every element and counts the ones equal to 2.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 2, 2, 5};
    auto first = lower_bound(v.begin(), v.end(), 2);
    auto last = upper_bound(v.begin(), v.end(), 2);
    cout << last - first << endl;
    return 0;
}
```
OPTIONS:
A) 2 || off_by_one
B) 4 || none
C) 3 || correct
D) 1 || none
EXPLANATION: lower_bound finds the first 2 (index 1) and upper_bound the first element after the 2s (index 4); the distance is how many 2s there are.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
nums = [5, 3, 8]
print(nums.index(8), 3 in nums)
```
OPTIONS:
A) 3 True || off_by_one
B) 2 True || correct
C) 2 False || none
D) 8 True || none
EXPLANATION: index gives the position of the value, counting from 0, and in checks membership.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
s = "banana"
print(s.find("na"), s.find("x"))
```
OPTIONS:
A) 2 -1 || correct
B) 2 None || none
C) 4 -1 || none
D) 3 0 || off_by_one
EXPLANATION: find returns the index of the first match, and -1 when there is none.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
import bisect

a = [1, 3, 3, 7]
print(bisect.bisect_left(a, 3), bisect.bisect_right(a, 3))
```
OPTIONS:
A) 1 2 || off_by_one
B) 2 3 || none
C) 1 3 || correct
D) 0 3 || none
EXPLANATION: bisect_left gives the position before the existing 3s and bisect_right the position after them.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
Binary search only gives correct answers when what is true about the data?
OPTIONS:
A) The data has no duplicates || none
B) The data is sorted || correct
C) The data holds fewer than 100 elements || none
D) The data holds only positive numbers || none
EXPLANATION: Binary search throws away half the range after each comparison, which is only safe when the order tells it which half the target must be in.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
About how many comparisons does binary search need, at most, to search 1000 sorted elements?
OPTIONS:
A) About 1000 || none
B) About 500 || none
C) About 100 || none
D) About 10 || correct
EXPLANATION: Each comparison halves the range, and 1000 can be halved about 10 times before one element is left.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
Linear search looks for a value that is not in a list of n elements. How many elements does it check?
OPTIONS:
A) All n of them || correct
B) About half of them || none
C) Only the first one || none
D) None, because it knows the value is missing || none
EXPLANATION: Linear search can only conclude a value is missing after checking every element.
=== END ===

=== DEBUG ===
PROBLEM: mbpp-160
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    position = -1
    for i in range(n):
        if values[i] == target:
            position = i
            break
    print(position)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    position = -1
    for i in range(n):
        if values[i] == target:
            position = i
    print(position)
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-160
LANGUAGE: c
BUG: wrong_initial_value
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int position = -1;
        for (int i = 0; i < n; i++) {
            if (a[i] == target) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
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
        int n, target;
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int position = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] == target) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-160
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
        int target;
        cin >> target;
        int position = -1;
        for (int i = 0; i < n; i++) {
            if (v[i] == target) {
                position = i;
                break;
            }
        }
        cout << position << endl;
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
        int target;
        cin >> target;
        int position = -1;
        for (int i = 1; i < n; i++) {
            if (v[i] == target) {
                position = i;
                break;
            }
        }
        cout << position << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-binary-search
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        int a[500];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int lo = 0, hi = n - 1, answer = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) {
                answer = mid;
                break;
            } else if (a[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        printf("%d\n", answer);
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
        int n, target;
        int a[500];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int lo = 0, hi = n - 1, answer = -1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) {
                answer = mid;
                break;
            } else if (a[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        printf("%d\n", answer);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-binary-search
LANGUAGE: cpp
BUG: infinite_loop
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
        int target;
        cin >> target;
        int lo = 0, hi = n - 1, answer = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (v[mid] == target) {
                answer = mid;
                break;
            } else if (v[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        cout << answer << endl;
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
        int target;
        cin >> target;
        int lo = 0, hi = n - 1, answer = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (v[mid] == target) {
                answer = mid;
                break;
            } else if (v[mid] < target) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        cout << answer << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-occurrences
LANGUAGE: python
BUG: uninitialised_variable
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    count = 0
    for value in values:
        if value == target:
            count += 1
    print(count)
```
BUGGY:
```python
t = int(input())
count = 0
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    for value in values:
        if value == target:
            count += 1
    print(count)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-count-occurrences
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int count = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] == target) {
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
        int n, target;
        int a[300];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int count = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] = target) {
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
PROBLEM: aita-count-occurrences
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
        int target;
        cin >> target;
        int count = 0;
        for (int i = 0; i < n; i++) {
            if (v[i] == target) {
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
        int target;
        cin >> target;
        int count = 0;
        for (int i = 0; i < n - 1; i++) {
            if (v[i] == target) {
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
ID: aita-srch-last-occurrence
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. The third line contains an integer target. Print the 0-based position of the last occurrence of target among the n integers. If target does not appear, print -1.
CONSTRAINTS: 1 <= n <= 100000; every integer and target are between -1000000000 and 1000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = list(map(int, data[pos + 1:pos + 1 + n]))
    target = int(data[pos + 1 + n])
    pos += n + 2
    answer = -1
    for i in range(n):
        if values[i] == target:
            answer = i
    print(answer)
```
TESTS:
### input
6
4 7 4 1 4 9
4
### output
4
### input
1
5
5
### output
0
### input
5
3 8 2 6 1
3
### output
0
### input
4
2 9 9 9
9
### output
3
### input
5
10 20 30 40 50
25
### output
-1
### input
3
-2 -2 -2
7
### output
-1
### input
1
-8
3
### output
-1
=== END ===

=== PROBLEM ===
ID: aita-srch-first-above
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. The third line contains an integer k. Print the 0-based position of the first integer that is strictly greater than k. If no integer is greater than k, print -1.
CONSTRAINTS: 1 <= n <= 100000; every integer and k are between -1000000000 and 1000000000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = list(map(int, data[pos + 1:pos + 1 + n]))
    k = int(data[pos + 1 + n])
    pos += n + 2
    answer = -1
    for i in range(n):
        if values[i] > k:
            answer = i
            break
    print(answer)
```
TESTS:
### input
5
3 10 7 12 4
8
### output
1
### input
4
6 6 9 2
6
### output
2
### input
3
1 2 3
5
### output
-1
### input
1
0
-1
### output
0
### input
4
-5 -3 -9 -1
-2
### output
3
### input
2
7 7
7
### output
-1
### input
3
50 1 1
49
### output
0
=== END ===

=== PROBLEM ===
ID: aita-srch-insert-position
DIFFICULTY: medium
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers in non-decreasing order. The third line contains an integer q. The fourth line contains q space-separated query values. For each query value x, print the smallest 0-based position at which x could be inserted so that the list stays in non-decreasing order, which is the number of list values strictly less than x. Print the q answers on one line, separated by single spaces.
CONSTRAINTS: 1 <= n <= 100000; 1 <= q <= 100000; every list value and query value is between -1000000000 and 1000000000.
REFERENCE:
```python
import sys
from bisect import bisect_left

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = list(map(int, data[pos + 1:pos + 1 + n]))
    pos += n + 1
    q = int(data[pos])
    queries = list(map(int, data[pos + 1:pos + 1 + q]))
    pos += q + 1
    print(" ".join(str(bisect_left(values, x)) for x in queries))
```
TESTS:
### input
5
2 4 4 4 9
4
4 1 9 10
### output
1 0 4 5
### input
1
7
3
7 6 8
### output
0 0 1
### input
6
-3 -1 0 0 5 8
2
0 6
### output
2 5
### input
4
10 20 30 40
3
25 40 41
### output
2 3 4
### input
3
5 5 5
3
5 4 6
### output
0 0 3
### input
5
1 3 5 7 9
5
1 3 5 7 9
### output
0 1 2 3 4
=== END ===

=== PROBLEM ===
ID: aita-srch-int-sqrt
DIFFICULTY: medium
STATEMENT: A single line contains a non-negative integer x. Print the largest integer r such that r * r <= x.
CONSTRAINTS: 0 <= x <= 1000000000. Do not use a floating-point square root; r * r can exceed the range of a 32-bit int while searching.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    x = int(data[k])
    lo, hi, answer = 0, x, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            answer = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(answer)
```
TESTS:
### input
16
### output
4
### input
0
### output
0
### input
1
### output
1
### input
2
### output
1
### input
17
### output
4
### input
999999999
### output
31622
### input
1000000000
### output
31622
=== END ===

=== PROBLEM ===
ID: aita-srch-day-pages
DIFFICULTY: hard
STATEMENT: The first line contains two integers n and d. The second line contains n space-separated positive integers; the i-th is the number of pages in chapter i. A student reads the chapters in the given order over at most d days. Each day they read one or more whole chapters that come next in order, and a chapter is never split across days. Print the smallest possible value of the largest number of pages read on any single day.
CONSTRAINTS: 1 <= d <= n <= 100000; 1 <= pages in a chapter <= 1000000000; the total number of pages fits in a 64-bit integer.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1


def days_needed(pages, limit):
    days, current = 1, 0
    for p in pages:
        if current + p > limit:
            days += 1
            current = p
        else:
            current += p
    return days


for _ in range(t):
    n, d = int(data[pos]), int(data[pos + 1])
    pages = list(map(int, data[pos + 2:pos + 2 + n]))
    pos += n + 2
    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(pages, mid) <= d:
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
TESTS:
### input
4 2
10 20 30 40
### output
60
### input
1 1
7
### output
7
### input
3 1
3 3 3
### output
9
### input
5 5
4 1 8 2 6
### output
8
### input
3 3
2 3 9
### output
9
### input
6 3
5 5 5 5 5 5
### output
10
### input
4 3
1000000000 1000000000 1000000000 1000000000
### output
2000000000
### input
5 2
1 2 3 4 5
### output
9
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-first-above
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int a[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, k;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &k);
        int position = -1;
        for (int i = 0; i < n; i++) {
            if (a[i] > k) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int a[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, k;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &k);
        int position = -1;
        for (int i = 0; i < n; i++) {
            if (a[i] >= k) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-last-occurrence
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int a[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int position = -1;
        for (int i = n - 1; i >= 0; i--) {
            if (a[i] == target) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int a[100000];

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int position = -1;
        for (int i = n - 1; i > 0; i--) {
            if (a[i] == target) {
                position = i;
                break;
            }
        }
        printf("%d\n", position);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-int-sqrt
LANGUAGE: c
BUG: wrong_loop_bound
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long x;
        scanf("%lld", &x);
        long long lo = 0, hi = x, answer = 0;
        while (lo <= hi) {
            long long mid = lo + (hi - lo) / 2;
            if (mid * mid <= x) {
                answer = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        printf("%lld\n", answer);
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
        long long x;
        scanf("%lld", &x);
        long long lo = 0, hi = x, answer = 0;
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (mid * mid <= x) {
                answer = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        printf("%lld\n", answer);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-insert-position
LANGUAGE: cpp
BUG: wrong_initial_value
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
        int q;
        cin >> q;
        for (int j = 0; j < q; j++) {
            int x;
            cin >> x;
            int lo = 0, hi = n;
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (v[mid] < x) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            if (j > 0) {
                cout << " ";
            }
            cout << lo;
        }
        cout << endl;
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
        int q;
        cin >> q;
        for (int j = 0; j < q; j++) {
            int x;
            cin >> x;
            int lo = 0, hi = n - 1;
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (v[mid] < x) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            if (j > 0) {
                cout << " ";
            }
            cout << lo;
        }
        cout << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-int-sqrt
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
        long long x;
        cin >> x;
        long long lo = 0, hi = x, answer = 0;
        while (lo <= hi) {
            long long mid = lo + (hi - lo) / 2;
            if (mid * mid <= x) {
                answer = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        cout << answer << endl;
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
        long long x;
        cin >> x;
        long long lo = 0, hi = x, answer = 0;
        while (lo <= hi) {
            long long mid = lo + (hi - lo) / 2;
            if (mid * mid <= x) {
                answer = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        cout << lo << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-day-pages
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
#include <vector>
using namespace std;

int daysNeeded(const vector<long long>& pages, long long limit) {
    int days = 1;
    long long current = 0;
    for (long long p : pages) {
        if (current + p > limit) {
            days++;
            current = p;
        } else {
            current += p;
        }
    }
    return days;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, d;
        cin >> n >> d;
        vector<long long> pages(n);
        long long lo = 0, hi = 0;
        for (int i = 0; i < n; i++) {
            cin >> pages[i];
            if (pages[i] > lo) {
                lo = pages[i];
            }
            hi += pages[i];
        }
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (daysNeeded(pages, mid) <= d) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        cout << lo << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <vector>
using namespace std;

int daysNeeded(const vector<long long>& pages, long long limit) {
    int days = 1;
    long long current = 0;
    for (long long p : pages) {
        if (current + p >= limit) {
            days++;
            current = p;
        } else {
            current += p;
        }
    }
    return days;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, d;
        cin >> n >> d;
        vector<long long> pages(n);
        long long lo = 0, hi = 0;
        for (int i = 0; i < n; i++) {
            cin >> pages[i];
            if (pages[i] > lo) {
                lo = pages[i];
            }
            hi += pages[i];
        }
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (daysNeeded(pages, mid) <= d) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        cout << lo << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-binary-search
LANGUAGE: python
BUG: integer_division
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    lo, hi = 0, n - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            answer = mid
            break
        elif values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print(answer)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    lo, hi = 0, n - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) / 2
        if values[mid] == target:
            answer = mid
            break
        elif values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print(answer)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-last-occurrence
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def last_position(values, target):
    position = -1
    for i in range(len(values)):
        if values[i] == target:
            position = i
    return position


t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    print(last_position(values, target))
```
BUGGY:
```python
def last_position(values, target):
    position = -1
    for i in range(len(values)):
        if values[i] == target:
            position = i
    print(position)


t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    print(last_position(values, target))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-insert-position
LANGUAGE: python
BUG: wrong_comparison_operator
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    q = int(input())
    queries = list(map(int, input().split()))
    answers = []
    for x in queries:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if values[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        answers.append(str(lo))
    print(" ".join(answers))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    q = int(input())
    queries = list(map(int, input().split()))
    answers = []
    for x in queries:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if values[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        answers.append(str(lo))
    print(" ".join(answers))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-srch-day-pages
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
def days_needed(pages, limit):
    days, current = 1, 0
    for p in pages:
        if current + p > limit:
            days += 1
            current = p
        else:
            current += p
    return days


t = int(input())
for _ in range(t):
    n, d = map(int, input().split())
    pages = list(map(int, input().split()))
    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(pages, mid) <= d:
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
BUGGY:
```python
def days_needed(pages, limit):
    days, current = 1, 0
    for p in pages:
        if current + p > limit:
            days += 1
            current = p
        else:
            current += p
    return days


t = int(input())
for _ in range(t):
    n, d = map(int, input().split())
    pages = list(map(int, input().split()))
    lo, hi = 1, sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(pages, mid) <= d:
            hi = mid
        else:
            lo = mid + 1
    print(lo)
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
nums = [3, 12, 7, 15]
answer = -1
for i, x in enumerate(nums):
    if x > 10:
        answer = i
        break
print(answer, nums[answer])
```
OPTIONS:
A) 3 15 || none
B) 1 12 || correct
C) 2 7 || off_by_one
D) -1 15 || none
EXPLANATION: The loop stops at the first value above 10, which is 12 at index 1.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
The value 9 is not in the list. What does this program print?
```python
a = [2, 5, 8, 11, 14]
x = 9
lo, hi = 0, len(a) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if a[mid] < x:
        lo = mid + 1
    else:
        hi = mid - 1
print(lo, hi)
```
OPTIONS:
A) 3 2 || correct
B) 2 3 || none
C) 3 3 || off_by_one
D) -1 -1 || none
EXPLANATION: mid 2 (value 8) moves lo to 3, mid 3 (value 11) moves hi to 2, so the loop ends with lo at the position where 9 would be inserted.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
def root(n):
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


print(root(30), root(36))
```
OPTIONS:
A) 6 6 || none
B) 5 5 || off_by_one
C) 5 6 || correct
D) 15 18 || integer_division
EXPLANATION: The search keeps the largest mid whose square is at most n, so it finds 5 for 30 (25 <= 30 < 36) and exactly 6 for 36.
=== END ===
