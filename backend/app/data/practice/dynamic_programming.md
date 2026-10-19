# Dynamic Programming

=== PROBLEM ===
ID: aita-climb-stairs
DIFFICULTY: easy
STATEMENT: A single line contains an integer n. A staircase has n steps and you climb it taking either 1 or 2 steps at a time. Print the number of different ways to reach the top.
CONSTRAINTS: 1 <= n <= 45.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    print(b)
```
TESTS:
### input
1
### output
1
### input
2
### output
2
### input
3
### output
3
### input
5
### output
8
### input
10
### output
89
### input
45
### output
1836311903
=== END ===

=== PROBLEM ===
ID: aita-min-coins
DIFFICULTY: medium
STATEMENT: A single line contains an amount n. Coins of value 1, 3 and 4 are available, as many of each as needed. Print the smallest number of coins whose values add up to exactly n.
CONSTRAINTS: 0 <= n <= 1000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    n = int(data[k])
    best = [0] + [n + 1] * n
    for amount in range(1, n + 1):
        for coin in (1, 3, 4):
            if coin <= amount:
                best[amount] = min(best[amount], best[amount - coin] + 1)
    print(best[n])
```
TESTS:
### input
6
### output
2
### input
0
### output
0
### input
1
### output
1
### input
7
### output
2
### input
10
### output
3
### input
1000
### output
250
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int f[6];
    f[0] = 0;
    f[1] = 1;
    for (int i = 2; i < 6; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }
    printf("%d\n", f[5]);
    return 0;
}
```
OPTIONS:
A) 8 || off_by_one
B) 3 || off_by_one
C) 5 || correct
D) 6 || none
EXPLANATION: The table fills in as 0, 1, 1, 2, 3, 5, each entry built from the two before it.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int a[] = {3, 1, 4, 1};
    int pre[5] = {0};
    for (int i = 0; i < 4; i++) {
        pre[i + 1] = pre[i] + a[i];
    }
    printf("%d\n", pre[4] - pre[1]);
    return 0;
}
```
OPTIONS:
A) 9 || none
B) 6 || correct
C) 5 || off_by_one
D) 8 || none
EXPLANATION: pre[k] holds the sum of the first k values, so pre[4] - pre[1] is the sum of a[1] to a[3]: 1 + 4 + 1.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int dp[5] = {1};
    for (int i = 1; i < 5; i++) {
        dp[i] = dp[i - 1] * 2;
    }
    printf("%d\n", dp[4]);
    return 0;
}
```
OPTIONS:
A) 8 || off_by_one
B) 32 || off_by_one
C) 0 || wrong_initial_value
D) 16 || correct
EXPLANATION: dp[0] is 1 and every entry doubles the previous one: 1, 2, 4, 8, 16.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
ways[i][j] counts the paths from the top-left corner of a grid, moving only right or down. What does this program print?
```c
#include <stdio.h>

int main(void) {
    int ways[3][3];
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (i == 0 || j == 0) {
                ways[i][j] = 1;
            } else {
                ways[i][j] = ways[i - 1][j] + ways[i][j - 1];
            }
        }
    }
    printf("%d\n", ways[2][2]);
    return 0;
}
```
OPTIONS:
A) 4 || none
B) 9 || none
C) 6 || correct
D) 3 || none
EXPLANATION: Each cell adds the paths arriving from above and from the left; the table's last row is 1, 3, 6.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int memo[10];
int calls = 0;

int fib(int n) {
    calls++;
    if (n < 2) {
        return n;
    }
    if (memo[n]) {
        return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    return memo[n];
}

int main(void) {
    fib(6);
    printf("%d\n", calls);
    return 0;
}
```
OPTIONS:
A) 25 || none
B) 11 || correct
C) 7 || none
D) 6 || none
EXPLANATION: The first chain fib(6) down to fib(2) makes 5 calls and fib(2) calls fib(1) and fib(0); after that each second call (fib(1), then fib(2), fib(3), fib(4)) is answered at once, giving 5 + 2 + 4 = 11. Without the memo it would be 25.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
ways[s] counts the ways to make the sum s from coins of value 1 and 2, ignoring order. What does this program print?
```c
#include <stdio.h>

int main(void) {
    int coins[] = {1, 2};
    int ways[5] = {1, 0, 0, 0, 0};
    for (int c = 0; c < 2; c++) {
        for (int s = coins[c]; s <= 4; s++) {
            ways[s] += ways[s - coins[c]];
        }
    }
    printf("%d\n", ways[4]);
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 4 || none
C) 2 || none
D) 3 || correct
EXPLANATION: The ways to make 4 are 1+1+1+1, 1+1+2 and 2+2; handling one coin type at a time avoids counting reorderings twice.
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
    vector<int> dp(5, 0);
    dp[0] = 1;
    for (int i = 1; i < 5; i++) {
        dp[i] = dp[i - 1] + i;
    }
    cout << dp[4] << endl;
    return 0;
}
```
OPTIONS:
A) 10 || wrong_initial_value
B) 11 || correct
C) 7 || off_by_one
D) 15 || none
EXPLANATION: The values go 1, 2, 4, 7, 11: each adds its index to the entry before.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
w[i] counts the ways to climb i steps taking 1 or 2 at a time. What does this program print?
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<long long> w(6);
    w[0] = 1;
    w[1] = 1;
    for (int i = 2; i <= 5; i++) {
        w[i] = w[i - 1] + w[i - 2];
    }
    cout << w[5] << endl;
    return 0;
}
```
OPTIONS:
A) 5 || off_by_one
B) 13 || off_by_one
C) 8 || correct
D) 10 || none
EXPLANATION: The last move is either 1 step or 2, so w[i] = w[i - 1] + w[i - 2]: 1, 1, 2, 3, 5, 8.
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
    vector<int> v = {-1, 3, -2, 4, -5};
    int cur = v[0], best = v[0];
    for (int i = 1; i < (int) v.size(); i++) {
        cur = max(v[i], cur + v[i]);
        best = max(best, cur);
    }
    cout << best << endl;
    return 0;
}
```
OPTIONS:
A) 4 || none
B) 7 || none
C) -1 || wrong_initial_value
D) 5 || correct
EXPLANATION: cur is the best sum of a block ending here; the block 3, -2, 4 gives the largest total, 5.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
dp[i] is the length of the longest increasing run of values, not necessarily adjacent, that ends at index i. What does this program print?
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {3, 1, 4, 1, 5};
    int n = v.size();
    vector<int> dp(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (v[j] < v[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }
    cout << *max_element(dp.begin(), dp.end()) << endl;
    return 0;
}
```
OPTIONS:
A) 3 || correct
B) 5 || none
C) 2 || none
D) 4 || none
EXPLANATION: dp works out to 1, 1, 2, 1, 3; for example 3, 4, 5 is an increasing run of length 3.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
dp[i][j] is the cheapest path sum from the top-left corner to (i, j), moving only right or down. What does this program print?
```cpp
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int grid[2][2] = {{1, 3}, {2, 1}};
    int dp[2][2];
    dp[0][0] = grid[0][0];
    dp[0][1] = dp[0][0] + grid[0][1];
    dp[1][0] = dp[0][0] + grid[1][0];
    dp[1][1] = grid[1][1] + min(dp[0][1], dp[1][0]);
    cout << dp[1][1] << endl;
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 4 || correct
C) 7 || none
D) 3 || none
EXPLANATION: Reaching (1, 1) through (1, 0) costs 1 + 2 + 1 = 4, cheaper than through (0, 1), which costs 5.
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
    int weight[] = {1, 3, 4};
    int value[] = {15, 20, 30};
    int capacity = 4;
    vector<int> best(capacity + 1, 0);
    for (int k = 0; k < 3; k++) {
        for (int c = capacity; c >= weight[k]; c--) {
            best[c] = max(best[c], best[c - weight[k]] + value[k]);
        }
    }
    cout << best[capacity] << endl;
    return 0;
}
```
OPTIONS:
A) 30 || none
B) 65 || none
C) 50 || none
D) 35 || correct
EXPLANATION: This is the 0/1 knapsack: the items of weight 1 and 3 fit together for value 35, more than the single item of weight 4.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
dp = [0, 1]
for i in range(2, 7):
    dp.append(dp[-1] + dp[-2])
print(dp[6])
```
OPTIONS:
A) 13 || off_by_one
B) 5 || off_by_one
C) 6 || none
D) 8 || correct
EXPLANATION: The list grows 0, 1, 1, 2, 3, 5, 8, and index 6 holds 8.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
memo = {}

def f(n):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = f(n - 1) + f(n - 2)
    return memo[n]

print(f(10), len(memo))
```
OPTIONS:
A) 55 10 || none
B) 89 8 || off_by_one
C) 55 8 || correct
D) 34 8 || off_by_one
EXPLANATION: f(10) is 55, and only the values n = 3 to 10 are stored, since n <= 2 returns before storing.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
grid = [[1] * 3 for _ in range(3)]
for i in range(1, 3):
    for j in range(1, 3):
        grid[i][j] = grid[i - 1][j] + grid[i][j - 1]
print(grid[2][2])
```
OPTIONS:
A) 4 || none
B) 9 || none
C) 5 || none
D) 6 || correct
EXPLANATION: Each cell adds the cell above and the cell to the left, giving the rows 1 1 1, 1 2 3 and 1 3 6.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Which pair of properties makes a problem a good fit for dynamic programming?
OPTIONS:
A) The input is sorted and has no duplicates || none
B) The same smaller subproblems come up again and again, and the best answer can be built from the best answers to those subproblems || correct
C) The problem has exactly one possible answer || none
D) The input is small enough to try every possibility || none
EXPLANATION: These are overlapping subproblems and optimal substructure; DP solves each subproblem once and reuses the answer.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What does memoisation do in a recursive solution?
OPTIONS:
A) It writes each result to the screen || none
B) It removes the base case so the recursion is faster || missing_base_case
C) It stores each subproblem's result the first time it is computed, so later calls reuse it instead of recomputing || correct
D) It sorts the input before the recursion starts || none
EXPLANATION: Remembering results turns an exponential number of repeated calls into one computation per subproblem.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Coins of value 1, 3 and 4 are available. A greedy method always takes the largest coin that still fits. Why does it fail to find the fewest coins for the amount 6?
OPTIONS:
A) It takes 4 + 1 + 1, three coins, but 3 + 3 needs only two || correct
B) It cannot make 6 at all || none
C) It takes six 1-coins || none
D) It does not fail; greedy is always optimal for coins || none
EXPLANATION: Taking the biggest coin first is not always best, so DP tries every last coin and keeps the cheapest result.
=== END ===

=== DEBUG ===
PROBLEM: dsa-max-subarray
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    current = best = values[0]
    for x in values[1:]:
        current = max(x, current + x)
        best = max(best, current)
    print(best)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    current = best = 0
    for x in values:
        current = max(x, current + x)
        best = max(best, current)
    print(best)
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-max-subarray
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
        int a[500];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int current = a[0], best = a[0];
        for (int i = 1; i < n; i++) {
            if (current + a[i] > a[i]) {
                current = current + a[i];
            } else {
                current = a[i];
            }
            if (current > best) {
                best = current;
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
        int a[500];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int current = a[0], best = a[0];
        for (int i = 2; i < n; i++) {
            if (current + a[i] > a[i]) {
                current = current + a[i];
            } else {
                current = a[i];
            }
            if (current > best) {
                best = current;
            }
        }
        printf("%d\n", best);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-climb-stairs
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    ways = [0] * (n + 1)
    ways[0] = 1
    ways[1] = 1
    for i in range(2, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    print(ways[n])
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    ways = [0] * (n + 1)
    ways[0] = 0
    ways[1] = 1
    for i in range(2, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    print(ways[n])
```
=== END ===

=== DEBUG ===
PROBLEM: aita-climb-stairs
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
        long long ways[50] = {0};
        ways[0] = 1;
        ways[1] = 1;
        for (int i = 2; i <= n; i++) {
            ways[i] = ways[i - 1] + ways[i - 2];
        }
        printf("%lld\n", ways[n]);
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
        long long ways[50] = {0};
        ways[0] = 1;
        ways[1] = 1;
        for (int i = 2; i < n; i++) {
            ways[i] = ways[i - 1] + ways[i - 2];
        }
        printf("%lld\n", ways[n]);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-climb-stairs
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
        long long a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            long long c = a + b;
            a = b;
            b = c;
        }
        cout << b << endl;
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
        long long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long long c = a + b;
            a = b;
            b = c;
        }
        cout << b << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-min-coins
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    best = [0] + [n + 1] * n
    for amount in range(1, n + 1):
        for coin in (1, 3, 4):
            if coin <= amount:
                best[amount] = min(best[amount], best[amount - coin] + 1)
    print(best[n])
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    best = [0] * (n + 1)
    for amount in range(1, n + 1):
        for coin in (1, 3, 4):
            if coin <= amount:
                best[amount] = min(best[amount], best[amount - coin] + 1)
    print(best[n])
```
=== END ===

=== DEBUG ===
PROBLEM: aita-min-coins
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int coins[3] = {1, 3, 4};
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int best[1001];
        best[0] = 0;
        for (int amount = 1; amount <= n; amount++) {
            best[amount] = n + 1;
            for (int k = 0; k < 3; k++) {
                if (amount - coins[k] >= 0 && best[amount - coins[k]] + 1 < best[amount]) {
                    best[amount] = best[amount - coins[k]] + 1;
                }
            }
        }
        printf("%d\n", best[n]);
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>

int main(void) {
    int coins[3] = {1, 3, 4};
    int t;
    scanf("%d", &t);
    while (t--) {
        int n;
        scanf("%d", &n);
        int best[1001];
        best[0] = 0;
        for (int amount = 1; amount <= n; amount++) {
            best[amount] = n + 1;
            for (int k = 0; k < 3; k++) {
                if (amount - coins[k] > 0 && best[amount - coins[k]] + 1 < best[amount]) {
                    best[amount] = best[amount - coins[k]] + 1;
                }
            }
        }
        printf("%d\n", best[n]);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-min-coins
LANGUAGE: cpp
BUG: wrong_loop_bound
CORRECT:
```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int coins[3] = {1, 3, 4};
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> best(n + 1, n + 1);
        best[0] = 0;
        for (int amount = 1; amount <= n; amount++) {
            for (int k = 0; k < 3; k++) {
                if (coins[k] <= amount) {
                    best[amount] = min(best[amount], best[amount - coins[k]] + 1);
                }
            }
        }
        cout << best[n] << endl;
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
    int coins[3] = {1, 3, 4};
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> best(n + 1, n + 1);
        best[0] = 0;
        for (int amount = 1; amount <= n; amount++) {
            for (int k = 0; k < 2; k++) {
                if (coins[k] <= amount) {
                    best[amount] = min(best[amount], best[amount - coins[k]] + 1);
                }
            }
        }
        cout << best[n] << endl;
    }
    return 0;
}
```
=== END ===
