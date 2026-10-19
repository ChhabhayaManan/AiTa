# Arrays

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[5] = {4, 8, 15, 16, 23};
    printf("%d %d\n", a[1], a[4]);
    return 0;
}
```
OPTIONS:
A) 4 16 || off_by_one
B) 8 16 || none
C) 8 23 || correct
D) 4 23 || none
EXPLANATION: Indexes start at 0, so a[1] is the second element (8) and a[4] is the fifth and last (23).
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {1, 2, 3, 4};
    int sum = 0;
    for (int i = 0; i < 4; i++) {
        sum += a[i];
    }
    printf("%d\n", sum);
    return 0;
}
```
OPTIONS:
A) 10 || correct
B) 6 || wrong_loop_bound
C) 4 || none
D) 1234 || none
EXPLANATION: The loop visits indexes 0 to 3 and adds 1 + 2 + 3 + 4.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[5] = {1, 2};
    printf("%d %d\n", a[1], a[4]);
    return 0;
}
```
OPTIONS:
A) 1 0 || off_by_one
B) 2 0 || correct
C) 2 2 || none
D) 2 5 || none
EXPLANATION: When an array is initialised with fewer values than its size, the remaining elements are set to 0.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[6];
    printf("%d\n", (int) (sizeof(a) / sizeof(a[0])));
    return 0;
}
```
OPTIONS:
A) 24 || none
B) 5 || off_by_one
C) 4 || none
D) 6 || correct
EXPLANATION: sizeof(a) is the size of the whole array in bytes; dividing by the size of one element gives the element count.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[5] = {1, 2, 3, 4, 5};
    for (int i = 0; i < 5 / 2; i++) {
        int t = a[i];
        a[i] = a[4 - i];
        a[4 - i] = t;
    }
    for (int i = 0; i < 5; i++) {
        printf("%d", a[i]);
    }
    printf("\n");
    return 0;
}
```
OPTIONS:
A) 12345 || wrong_loop_bound
B) 54321 || correct
C) 52341 || none
D) 54123 || none
EXPLANATION: Swapping the first and last, then the second and second-to-last, reverses the array; the middle element stays put.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int g[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("%d\n", g[1][0] + g[0][2]);
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 6 || none
C) 7 || correct
D) 9 || none
EXPLANATION: g[1][0] is the first element of the second row (4) and g[0][2] is the last element of the first row (3).
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
    vector<int> v = {5, 10, 15};
    v.push_back(20);
    cout << v.size() << " " << v.back() << endl;
    return 0;
}
```
OPTIONS:
A) 3 15 || none
B) 4 20 || correct
C) 4 5 || none
D) 3 20 || none
EXPLANATION: push_back adds 20 at the end, so the vector now holds 4 elements and back() is 20.
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
    int a[] = {3, 6, 9};
    cout << a[0] + a[2] << endl;
    return 0;
}
```
OPTIONS:
A) 9 || off_by_one
B) 15 || off_by_one
C) 18 || none
D) 12 || correct
EXPLANATION: a[0] is 3 and a[2] is 9, the first and third elements.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v(3, 7);
    v[1] = 0;
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 3 0 7 || none
B) 7 0 7 || correct
C) 0 7 7 || off_by_one
D) 7 7 7 || none
EXPLANATION: vector<int> v(3, 7) makes three elements that are all 7; then the middle one is set to 0.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3};
    for (int x : v) {
        x *= 2;
    }
    cout << v[0] << v[1] << v[2] << endl;
    return 0;
}
```
OPTIONS:
A) 246 || none
B) 2 4 6 || none
C) 123 || correct
D) 1 2 3 || none
EXPLANATION: int x is a copy of each element, so doubling it leaves the vector unchanged; int &x would have changed it.
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
    vector<int> v = {4, 1, 3};
    sort(v.begin(), v.end());
    cout << v[0] << v[2] << endl;
    return 0;
}
```
OPTIONS:
A) 14 || correct
B) 43 || none
C) 41 || none
D) 13 || none
EXPLANATION: After sorting the vector is {1, 3, 4}, so the first element is 1 and the last is 4.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {2, 9, 4, 9, 1};
    int best = 0;
    for (int i = 1; i < (int) v.size(); i++) {
        if (v[i] > v[best]) {
            best = i;
        }
    }
    cout << best << endl;
    return 0;
}
```
OPTIONS:
A) 3 || wrong_comparison_operator
B) 9 || none
C) 4 || none
D) 1 || correct
EXPLANATION: best is an index; the second 9 is not greater than the first, so the first 9's index, 1, is kept.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
nums = [10, 20, 30, 40]
print(nums[-1], nums[1:3])
```
OPTIONS:
A) 40 [20, 30] || correct
B) 10 [20, 30, 40] || none
C) 40 [10, 20, 30] || off_by_one
D) 30 [20, 30] || off_by_one
EXPLANATION: Index -1 is the last element, and the slice 1:3 takes indexes 1 and 2, stopping before 3.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
a = [1, 2, 3]
b = a
b.append(4)
print(len(a))
```
OPTIONS:
A) 3 || none
B) 4 || correct
C) 1 || none
D) 7 || none
EXPLANATION: b = a does not copy the list; both names refer to the same list, so appending through b changes a too.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
grid = [[0] * 2] * 2
grid[0][0] = 5
print(grid)
```
OPTIONS:
A) [[5, 0], [0, 0]] || none
B) [[5, 5], [0, 0]] || none
C) [[5, 0], [5, 0]] || correct
D) [[5, 5], [5, 5]] || none
EXPLANATION: Multiplying the outer list repeats a reference to the same inner list, so both rows are one list.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
An array has 10 elements and its indexes start at 0. What is the index of its last element?
OPTIONS:
A) 10 || off_by_one
B) 9 || correct
C) 11 || none
D) 1 || none
EXPLANATION: Counting from 0, the ten indexes are 0 to 9.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Why is reading the element at index n of an array with n elements (indexes starting at 0) a mistake?
OPTIONS:
A) The valid indexes are 0 to n - 1, so index n is past the end || correct
B) Index n is the first element, not the last || none
C) An array can never hold exactly n elements || none
D) It is not a mistake; index n is the last element || index_out_of_range
EXPLANATION: With indexes starting at 0, the last valid index is one less than the length; going past it reads memory or raises an error.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What is the main advantage of keeping 100 test scores in one array instead of in 100 separate variables?
OPTIONS:
A) The scores take no memory when they are in an array || none
B) A loop can visit every score by its index, so the same code handles any number of scores || correct
C) Arrays sort themselves automatically || none
D) Each score can then hold several values at once || none
EXPLANATION: An array gives every value a numbered position, so one loop replaces 100 separate lines of code.
=== END ===

=== DEBUG ===
PROBLEM: dsa-second-largest
LANGUAGE: python
BUG: empty_input_unhandled
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    distinct = sorted(set(values))
    if len(distinct) < 2:
        print("None")
    else:
        print(distinct[-2])
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    distinct = sorted(set(values))
    print(distinct[-2])
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-second-largest
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
        int has_first = 0, has_second = 0;
        int first = 0, second = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            if (!has_first || x > first) {
                if (has_first) {
                    second = first;
                    has_second = 1;
                }
                first = x;
                has_first = 1;
            } else if (x != first && (!has_second || x > second)) {
                second = x;
                has_second = 1;
            }
        }
        if (has_second) {
            printf("%d\n", second);
        } else {
            printf("None\n");
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
        int has_first = 0, has_second = 0;
        int first = 0, second = 0;
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            if (!has_first || x >= first) {
                if (has_first) {
                    second = first;
                    has_second = 1;
                }
                first = x;
                has_first = 1;
            } else if (x != first && (!has_second || x > second)) {
                second = x;
                has_second = 1;
            }
        }
        if (has_second) {
            printf("%d\n", second);
        } else {
            printf("None\n");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-second-largest
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <climits>
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long first = LLONG_MIN, second = LLONG_MIN;
        for (int i = 0; i < n; i++) {
            long long x;
            cin >> x;
            if (x > first) {
                second = first;
                first = x;
            } else if (x < first && x > second) {
                second = x;
            }
        }
        if (second == LLONG_MIN) {
            cout << "None" << endl;
        } else {
            cout << second << endl;
        }
    }
    return 0;
}
```
BUGGY:
```cpp
#include <climits>
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long first = 0, second = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            cin >> x;
            if (x > first) {
                second = first;
                first = x;
            } else if (x < first && x > second) {
                second = x;
            }
        }
        if (second == LLONG_MIN) {
            cout << "None" << endl;
        } else {
            cout << second << endl;
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-move-zeroes
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    pos = 0
    for i in range(n):
        if values[i] != 0:
            values[pos] = values[i]
            pos += 1
    for i in range(pos, n):
        values[i] = 0
    print(" ".join(map(str, values)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    pos = 0
    for i in range(n):
        if values[i] != 0:
            values[pos] = values[i]
            pos += 1
    for i in range(pos + 1, n):
        values[i] = 0
    print(" ".join(map(str, values)))
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-move-zeroes
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
        int a[300];
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int pos = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] != 0) {
                a[pos] = a[i];
                pos++;
            }
        }
        for (int i = pos; i < n; i++) {
            a[i] = 0;
        }
        for (int i = 0; i < n; i++) {
            printf("%d%c", a[i], i == n - 1 ? '\n' : ' ');
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
        int a[300];
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int pos = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] != 0) {
                a[pos] = a[i];
                pos++;
            }
        }
        for (int i = pos; i < n - 1; i++) {
            a[i] = 0;
        }
        for (int i = 0; i < n; i++) {
            printf("%d%c", a[i], i == n - 1 ? '\n' : ' ');
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-move-zeroes
LANGUAGE: cpp
BUG: wrong_comparison_operator
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
        vector<int> out;
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            if (x != 0) {
                out.push_back(x);
            }
        }
        while ((int) out.size() < n) {
            out.push_back(0);
        }
        for (int i = 0; i < n; i++) {
            cout << out[i] << (i == n - 1 ? "\n" : " ");
        }
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
        vector<int> out;
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            if (x > 0) {
                out.push_back(x);
            }
        }
        while ((int) out.size() < n) {
            out.push_back(0);
        }
        for (int i = 0; i < n; i++) {
            cout << out[i] << (i == n - 1 ? "\n" : " ");
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-merge-sorted
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    i = j = 0
    merged = []
    while i < n and j < m:
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged += a[i:]
    merged += b[j:]
    print(" ".join(map(str, merged)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    i = j = 0
    merged = []
    while i < n and j < m:
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged += a[i:]
    print(" ".join(map(str, merged)))
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-merge-sorted
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, m;
        int a[300], b[300], merged[600];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &m);
        for (int j = 0; j < m; j++) {
            scanf("%d", &b[j]);
        }
        int i = 0, j = 0, k = 0;
        while (i < n && j < m) {
            if (a[i] <= b[j]) {
                merged[k++] = a[i++];
            } else {
                merged[k++] = b[j++];
            }
        }
        while (i < n) {
            merged[k++] = a[i++];
        }
        while (j < m) {
            merged[k++] = b[j++];
        }
        for (int x = 0; x < k; x++) {
            printf("%d%s", merged[x], x == k - 1 ? "" : " ");
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
        int n, m;
        int a[300], b[300], merged[600];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &m);
        for (int j = 0; j < m; j++) {
            scanf("%d", &b[j]);
        }
        int i = 0, j = 0, k = 0;
        while (i < n && j < m) {
            if (a[i] >= b[j]) {
                merged[k++] = a[i++];
            } else {
                merged[k++] = b[j++];
            }
        }
        while (i < n) {
            merged[k++] = a[i++];
        }
        while (j < m) {
            merged[k++] = b[j++];
        }
        for (int x = 0; x < k; x++) {
            printf("%d%s", merged[x], x == k - 1 ? "" : " ");
        }
        printf("\n");
    }
    return 0;
}
```
=== END ===
