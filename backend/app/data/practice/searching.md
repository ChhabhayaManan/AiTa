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
