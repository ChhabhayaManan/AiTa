# Hashing & Sets

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int count[5] = {0};
    int data[] = {1, 3, 1, 4, 1};
    for (int i = 0; i < 5; i++) {
        count[data[i]]++;
    }
    printf("%d %d\n", count[1], count[2]);
    return 0;
}
```
OPTIONS:
A) 3 0 || correct
B) 1 3 || none
C) 3 1 || none
D) 2 0 || off_by_one
EXPLANATION: Each value is used as an index into count; 1 appears three times and 2 never appears.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "abca";
    int seen[26] = {0};
    int dup = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        if (seen[s[i] - 'a']) {
            dup = 1;
        }
        seen[s[i] - 'a'] = 1;
    }
    printf("%d\n", dup);
    return 0;
}
```
OPTIONS:
A) 0 || none
B) 1 || correct
C) 2 || none
D) 4 || none
EXPLANATION: seen marks every letter met so far; the second a finds its mark already set, so dup becomes 1.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    int seen[10] = {0};
    int vals[] = {2, 5, 2, 7, 5};
    int distinct = 0;
    for (int i = 0; i < 5; i++) {
        if (!seen[vals[i]]) {
            seen[vals[i]] = 1;
            distinct++;
        }
    }
    printf("%d\n", distinct);
    return 0;
}
```
OPTIONS:
A) 5 || none
B) 2 || none
C) 3 || correct
D) 4 || none
EXPLANATION: Only the first time a value is seen does it count, so 2, 5 and 7 give three distinct values.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    printf("%d %d\n", 17 % 10, 27 % 10);
    return 0;
}
```
OPTIONS:
A) 1 2 || none
B) 17 27 || none
C) 7 2 || none
D) 7 7 || correct
EXPLANATION: Both keys leave remainder 7, so a table that uses key % 10 as the slot would put them in the same slot: a collision.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "banana";
    int c[26] = {0};
    for (int i = 0; s[i] != '\0'; i++) {
        c[s[i] - 'a']++;
    }
    int best = 0;
    for (int k = 1; k < 26; k++) {
        if (c[k] > c[best]) {
            best = k;
        }
    }
    printf("%c %d\n", 'a' + best, c[best]);
    return 0;
}
```
OPTIONS:
A) n 2 || none
B) a 3 || correct
C) b 1 || none
D) a 2 || none
EXPLANATION: The counts are a: 3, b: 1, n: 2, so the most frequent letter is a.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    const char *w = "cab";
    int h = 0;
    for (int i = 0; w[i] != '\0'; i++) {
        h = (h * 31 + w[i]) % 7;
    }
    printf("%d\n", h);
    return 0;
}
```
OPTIONS:
A) 0 || none
B) 3 || none
C) 6 || correct
D) 294 || none
EXPLANATION: With 'c' = 99, 'a' = 97 and 'b' = 98, h goes 99 % 7 = 1, then (31 + 97) % 7 = 2, then (62 + 98) % 7 = 6.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {3, 1, 3, 2};
    cout << s.size() << endl;
    return 0;
}
```
OPTIONS:
A) 4 || none
B) 3 || correct
C) 2 || none
D) 1 || none
EXPLANATION: A set keeps each value only once, so the second 3 is ignored.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: easy
STEM:
What does this program print?
```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {5, 1, 4};
    for (int x : s) {
        cout << x << " ";
    }
    cout << endl;
    return 0;
}
```
OPTIONS:
A) 5 1 4 || none
B) 5 4 1 || none
C) 1 4 5 || correct
D) 4 1 5 || none
EXPLANATION: std::set keeps its elements sorted, so iterating it gives them in ascending order.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> m;
    m["b"] = 2;
    m["a"] = 1;
    m["b"] += 5;
    cout << m.size() << " " << m["b"] << endl;
    return 0;
}
```
OPTIONS:
A) 3 7 || none
B) 2 5 || none
C) 2 7 || correct
D) 3 5 || none
EXPLANATION: A map holds one value per key; "b" is updated in place, so there are two keys and m["b"] is 2 + 5.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <unordered_set>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {4, 2, 4, 9, 2};
    unordered_set<int> seen;
    int dups = 0;
    for (int x : v) {
        if (seen.count(x)) {
            dups++;
        } else {
            seen.insert(x);
        }
    }
    cout << dups << endl;
    return 0;
}
```
OPTIONS:
A) 3 || none
B) 1 || none
C) 0 || none
D) 2 || correct
EXPLANATION: The second 4 and the second 2 are already in the set, so two duplicates are counted.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<char, int> m;
    for (char c : string("hello")) {
        m[c]++;
    }
    int l = m['l'];
    int z = m['z'];
    cout << l << z << m.size() << endl;
    return 0;
}
```
OPTIONS:
A) 204 || none
B) 205 || correct
C) 104 || none
D) 2 4 || none
EXPLANATION: Reading m['z'] with [] inserts the missing key with value 0, so the map grows from 4 keys (h, e, l, o) to 5.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {10, 20, 30};
    s.insert(20);
    s.erase(10);
    cout << s.size() << *s.begin() << endl;
    return 0;
}
```
OPTIONS:
A) 320 || none
B) 210 || none
C) 310 || none
D) 220 || correct
EXPLANATION: Inserting 20 again changes nothing, erasing 10 leaves {20, 30}, and begin() is the smallest element, 20.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
s = {1, 2, 2, 3}
print(len(s))
```
OPTIONS:
A) 4 || none
B) 2 || none
C) 3 || correct
D) 1 || none
EXPLANATION: A set keeps each value once, so the duplicate 2 is dropped.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
d = {"a": 1}
d["b"] = 2
d["a"] += 10
print(d["a"], len(d))
```
OPTIONS:
A) 11 2 || correct
B) 11 3 || none
C) 1 2 || none
D) 10 2 || none
EXPLANATION: Assigning to an existing key replaces its value, so the dictionary still has two keys.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
counts = {}
for word in "the cat the hat".split():
    counts[word] = counts.get(word, 0) + 1
print(counts["the"], "dog" in counts)
```
OPTIONS:
A) 1 False || none
B) 2 None || none
C) 2 True || none
D) 2 False || correct
EXPLANATION: get returns 0 for a missing key, so "the" is counted twice; "dog" was never added.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Why is a hash table (a set, dictionary or map) good for checking whether a value has been seen before?
OPTIONS:
A) It keeps its values sorted, so the check is always alphabetical || none
B) It jumps straight to where the value would be stored, instead of comparing it with every stored value || correct
C) It never uses any memory || none
D) It can only hold numbers, which are fast to compare || none
EXPLANATION: The hash of a value tells the table which slot to look in, so a lookup takes about the same time however many values are stored.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A set holds the values 3, 7 and 9. The value 7 is added again. How many values does the set hold now?
OPTIONS:
A) 4 || none
B) 3 || correct
C) 2 || none
D) 1 || none
EXPLANATION: A set holds each value at most once, so adding 7 again changes nothing.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
Two different keys are sent to the same slot of a hash table. What is this called?
OPTIONS:
A) An overflow || none
B) A duplicate key || none
C) A collision || correct
D) A base case || none
EXPLANATION: A collision is normal; the table handles it, for example by keeping a small list in that slot.
=== END ===

=== DEBUG ===
PROBLEM: dsa-two-sum
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    answer = "-1"
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] + values[j] == target:
                answer = f"{i} {j}"
                break
        if answer != "-1":
            break
    print(answer)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    target = int(input())
    answer = "-1"
    for i in range(n):
        for j in range(i + 1, n - 1):
            if values[i] + values[j] == target:
                answer = f"{i} {j}"
                break
        if answer != "-1":
            break
    print(answer)
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-two-sum
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, target;
        int a[200];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int found_i = -1, found_j = -1;
        for (int i = 0; i < n && found_i == -1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (a[i] + a[j] == target) {
                    found_i = i;
                    found_j = j;
                    break;
                }
            }
        }
        if (found_i == -1) {
            printf("-1\n");
        } else {
            printf("%d %d\n", found_i, found_j);
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
        int n, target;
        int a[200];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        scanf("%d", &target);
        int found_i = -1, found_j = -1;
        for (int i = 0; i < n && found_i == -1; i++) {
            for (int j = i; j < n; j++) {
                if (a[i] + a[j] == target) {
                    found_i = i;
                    found_j = j;
                    break;
                }
            }
        }
        if (found_i == -1) {
            printf("-1\n");
        } else {
            printf("%d %d\n", found_i, found_j);
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-two-sum
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
        int target;
        cin >> target;
        int a = -1, b = -1;
        for (int i = 0; i < n && a == -1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (v[i] + v[j] == target) {
                    a = i;
                    b = j;
                    break;
                }
            }
        }
        if (a == -1) {
            cout << -1 << endl;
        } else {
            cout << a << " " << b << endl;
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
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        int target;
        cin >> target;
        int a = 0, b = -1;
        for (int i = 0; i < n && a == -1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (v[i] + v[j] == target) {
                    a = i;
                    b = j;
                    break;
                }
            }
        }
        if (a == -1) {
            cout << -1 << endl;
        } else {
            cout << a << " " << b << endl;
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-anagram
LANGUAGE: python
BUG: wrong_loop_bound
CORRECT:
```python
t = int(input())
for _ in range(t):
    a = input()
    b = input()
    counts = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        counts[ch] = counts.get(ch, 0) - 1
    same = True
    for value in counts.values():
        if value != 0:
            same = False
    print("YES" if same else "NO")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    a = input()
    b = input()
    same = True
    for ch in a:
        if a.count(ch) != b.count(ch):
            same = False
    print("YES" if same else "NO")
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-anagram
LANGUAGE: c
BUG: uninitialised_variable
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[400], b[400];
    int t;
    fgets(a, sizeof a, stdin);
    sscanf(a, "%d", &t);
    while (t--) {
        fgets(a, sizeof a, stdin);
        fgets(b, sizeof b, stdin);
        a[strcspn(a, "\r\n")] = '\0';
        b[strcspn(b, "\r\n")] = '\0';
        int count[256] = {0};
        for (int i = 0; a[i] != '\0'; i++) {
            count[(unsigned char) a[i]]++;
        }
        for (int i = 0; b[i] != '\0'; i++) {
            count[(unsigned char) b[i]]--;
        }
        int same = 1;
        for (int c = 0; c < 256; c++) {
            if (count[c] != 0) {
                same = 0;
            }
        }
        printf("%s\n", same ? "YES" : "NO");
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[400], b[400];
    int count[256] = {0};
    int t;
    fgets(a, sizeof a, stdin);
    sscanf(a, "%d", &t);
    while (t--) {
        fgets(a, sizeof a, stdin);
        fgets(b, sizeof b, stdin);
        a[strcspn(a, "\r\n")] = '\0';
        b[strcspn(b, "\r\n")] = '\0';
        for (int i = 0; a[i] != '\0'; i++) {
            count[(unsigned char) a[i]]++;
        }
        for (int i = 0; b[i] != '\0'; i++) {
            count[(unsigned char) b[i]]--;
        }
        int same = 1;
        for (int c = 0; c < 256; c++) {
            if (count[c] != 0) {
                same = 0;
            }
        }
        printf("%s\n", same ? "YES" : "NO");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-anagram
LANGUAGE: cpp
BUG: wrong_comparison_operator
CORRECT:
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string a, b;
        getline(cin, a);
        getline(cin, b);
        map<char, int> counts;
        for (char c : a) {
            counts[c]++;
        }
        for (char c : b) {
            counts[c]--;
        }
        bool same = true;
        for (auto entry : counts) {
            if (entry.second != 0) {
                same = false;
            }
        }
        cout << (same ? "YES" : "NO") << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string a, b;
        getline(cin, a);
        getline(cin, b);
        map<char, int> counts;
        for (char c : a) {
            counts[c]++;
        }
        for (char c : b) {
            counts[c]--;
        }
        bool same = true;
        for (auto entry : counts) {
            if (entry.second > 0) {
                same = false;
            }
        }
        cout << (same ? "YES" : "NO") << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-count-characters
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[600];
        scanf("%s", s);
        int count[26] = {0};
        for (int i = 0; s[i] != '\0'; i++) {
            count[s[i] - 'a']++;
        }
        for (int c = 0; c < 26; c++) {
            if (count[c] > 0) {
                printf("%c %d\n", 'a' + c, count[c]);
            }
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
        char s[600];
        scanf("%s", s);
        int count[26] = {0};
        for (int i = 0; s[i] != '\0'; i++) {
            count[s[i] - 'a']++;
        }
        for (int c = 0; c < 25; c++) {
            if (count[c] > 0) {
                printf("%c %d\n", 'a' + c, count[c]);
            }
        }
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-count-characters
LANGUAGE: cpp
BUG: uninitialised_variable
CORRECT:
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        map<char, int> counts;
        for (char c : s) {
            counts[c]++;
        }
        for (auto entry : counts) {
            cout << entry.first << " " << entry.second << endl;
        }
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    map<char, int> counts;
    while (t--) {
        string s;
        cin >> s;
        for (char c : s) {
            counts[c]++;
        }
        for (auto entry : counts) {
            cout << entry.first << " " << entry.second << endl;
        }
    }
    return 0;
}
```
=== END ===

=== PROBLEM ===
ID: aita-first-repeat
DIFFICULTY: easy
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. Read them from left to right and print the first integer that you meet for the second time. If no integer appears twice, print -1.
CONSTRAINTS: 1 <= n <= 1000; each integer is between 1 and 1000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = [int(x) for x in data[pos + 1:pos + 1 + n]]
    pos += 1 + n
    seen = set()
    answer = -1
    for x in values:
        if x in seen:
            answer = x
            break
        seen.add(x)
    print(answer)
```
TESTS:
### input
5
3 1 4 1 3
### output
1
### input
1
7
### output
-1
### input
4
2 2 2 2
### output
2
### input
6
1 2 3 4 5 6
### output
-1
### input
6
1000 5 9 5 1000 9
### output
5
### input
4
8 3 8 3
### output
8
### input
3
1 1000 1000
### output
1000
=== END ===

=== PROBLEM ===
ID: aita-pair-sum-count
DIFFICULTY: medium
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. The third line contains an integer k. Print how many pairs of positions i < j there are whose two integers add up to exactly k.
CONSTRAINTS: 1 <= n <= 1000; each integer is between 0 and 1000; 0 <= k <= 2000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = [int(x) for x in data[pos + 1:pos + 1 + n]]
    k = int(data[pos + 1 + n])
    pos += 2 + n
    count = {}
    pairs = 0
    for x in values:
        pairs += count.get(k - x, 0)
        count[x] = count.get(x, 0) + 1
    print(pairs)
```
TESTS:
### input
5
1 5 3 3 4
6
### output
2
### input
1
4
8
### output
0
### input
4
2 2 2 2
4
### output
6
### input
3
0 0 1000
1000
### output
2
### input
3
1 2 3
100
### output
0
### input
6
1000 1000 0 999 1 500
2000
### output
1
### input
5
0 0 0 0 0
0
### output
10
### input
3
7 7 7
14
### output
3
=== END ===

=== PROBLEM ===
ID: aita-distinct-rank
DIFFICULTY: medium
STATEMENT: The first line contains an integer n. The second line contains n space-separated integers. For each integer, in the order given, print how many different values in the list are smaller than it. Print the n answers on one line, separated by single spaces.
CONSTRAINTS: 1 <= n <= 1000; each integer is between 1 and 1000.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
pos = 1
for _ in range(t):
    n = int(data[pos])
    values = [int(x) for x in data[pos + 1:pos + 1 + n]]
    pos += 1 + n
    rank = {}
    for i, v in enumerate(sorted(set(values))):
        rank[v] = i
    print(" ".join(str(rank[v]) for v in values))
```
TESTS:
### input
5
40 10 40 20 10
### output
2 0 2 1 0
### input
1
5
### output
0
### input
4
7 7 7 7
### output
0 0 0 0
### input
5
5 4 3 2 1
### output
4 3 2 1 0
### input
6
1000 1 500 1 1000 2
### output
3 0 2 0 3 1
### input
3
999 1000 998
### output
1 2 0
=== END ===

=== PROBLEM ===
ID: aita-balanced-days
DIFFICULTY: hard
STATEMENT: A single line contains a string made only of the letters R and D, one letter for each day: R means a rainy day and D means a dry day. Print the length of the longest run of consecutive days that has exactly as many rainy days as dry days. If there is no such run, print 0.
CONSTRAINTS: The string has between 1 and 100000 letters and contains no spaces.
REFERENCE:
```python
import sys

data = sys.stdin.read().split()
t = int(data[0])
for k in range(1, t + 1):
    s = data[k]
    first = {0: -1}
    balance = 0
    best = 0
    for i, ch in enumerate(s):
        balance += 1 if ch == "R" else -1
        if balance in first:
            best = max(best, i - first[balance])
        else:
            first[balance] = i
    print(best)
```
TESTS:
### input
RRRDRDD
### output
6
### input
R
### output
0
### input
RD
### output
2
### input
DDDD
### output
0
### input
RDRDRD
### output
6
### input
RRRRDRRR
### output
2
### input
RRRDDRRR
### output
4
### input
DDRDRRRD
### output
8
=== END ===

=== DEBUG ===
PROBLEM: dsa-count-characters
LANGUAGE: python
BUG: return_vs_print
CORRECT:
```python
def letter_report(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    lines = []
    for ch in sorted(counts):
        lines.append(f"{ch} {counts[ch]}")
    return "\n".join(lines)


t = int(input())
for _ in range(t):
    s = input().strip()
    print(letter_report(s))
```
BUGGY:
```python
def letter_report(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in sorted(counts):
        print(f"{ch} {counts[ch]}")


t = int(input())
for _ in range(t):
    s = input().strip()
    print(letter_report(s))
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-002
LANGUAGE: python
BUG: mutate_while_iterating
CORRECT:
```python
t = int(input())
for _ in range(t):
    first = set(map(int, input().split()))
    second = set(map(int, input().split()))
    common = set(first)
    for x in list(common):
        if x not in second:
            common.remove(x)
    print(" ".join(str(x) for x in sorted(common)))
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    first = set(map(int, input().split()))
    second = set(map(int, input().split()))
    common = set(first)
    for x in common:
        if x not in second:
            common.remove(x)
    print(" ".join(str(x) for x in sorted(common)))
```
=== END ===

=== DEBUG ===
PROBLEM: aita-first-repeat
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    seen = set()
    answer = -1
    for i in range(n):
        if values[i] in seen:
            answer = values[i]
            break
        seen.add(values[i])
    print(answer)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    n = int(input())
    values = list(map(int, input().split()))
    seen = set()
    answer = -1
    for i in range(1, n):
        if values[i] in seen:
            answer = values[i]
            break
        seen.add(values[i])
    print(answer)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-balanced-days
LANGUAGE: python
BUG: wrong_initial_value
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    first = {0: -1}
    balance = 0
    best = 0
    for i in range(len(s)):
        if s[i] == "R":
            balance += 1
        else:
            balance -= 1
        if balance in first:
            best = max(best, i - first[balance])
        else:
            first[balance] = i
    print(best)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    first = {}
    balance = 0
    best = 0
    for i in range(len(s)):
        if s[i] == "R":
            balance += 1
        else:
            balance -= 1
        if balance in first:
            best = max(best, i - first[balance])
        else:
            first[balance] = i
    print(best)
```
=== END ===

=== DEBUG ===
PROBLEM: aita-first-repeat
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
        int a[1000];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int count[1001] = {0};
        int answer = -1;
        for (int i = 0; i < n; i++) {
            count[a[i]]++;
            if (count[a[i]] >= 2) {
                answer = a[i];
                break;
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
        int n;
        int a[1000];
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
        }
        int count[1001] = {0};
        int answer = -1;
        for (int i = 0; i < n; i++) {
            count[a[i]]++;
            if (count[a[i]] > 2) {
                answer = a[i];
                break;
            }
        }
        printf("%d\n", answer);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-pair-sum-count
LANGUAGE: c
BUG: integer_division
CORRECT:
```c
#include <stdio.h>

int main(void) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int n, k;
        int count[1001] = {0};
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            count[x]++;
        }
        scanf("%d", &k);
        int pairs = 0;
        for (int v = 0; v <= 1000; v++) {
            int w = k - v;
            if (v < w && w <= 1000) {
                pairs += count[v] * count[w];
            }
        }
        if (k % 2 == 0) {
            int c = count[k / 2];
            pairs += c * (c - 1) / 2;
        }
        printf("%d\n", pairs);
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
        int count[1001] = {0};
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            int x;
            scanf("%d", &x);
            count[x]++;
        }
        scanf("%d", &k);
        int pairs = 0;
        for (int v = 0; v <= 1000; v++) {
            int w = k - v;
            if (v < w && w <= 1000) {
                pairs += count[v] * count[w];
            }
        }
        if (k % 2 == 0) {
            int c = count[k / 2];
            pairs += c / 2 * (c - 1);
        }
        printf("%d\n", pairs);
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-distinct-rank
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
        int a[1000];
        int present[1001] = {0};
        int smaller[1001] = {0};
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
            present[a[i]] = 1;
        }
        int distinct = 0;
        for (int v = 1; v <= 1000; v++) {
            smaller[v] = distinct;
            if (present[v]) {
                distinct++;
            }
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                printf(" ");
            }
            printf("%d", smaller[a[i]]);
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
        int a[1000];
        int present[1001] = {0};
        int smaller[1001] = {0};
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
            present[a[i]] = 1;
        }
        int distinct = 0;
        for (int v = 1; v < 1000; v++) {
            smaller[v] = distinct;
            if (present[v]) {
                distinct++;
            }
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                printf(" ");
            }
            printf("%d", smaller[a[i]]);
        }
        printf("\n");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-pair-sum-count
LANGUAGE: cpp
BUG: uninitialised_variable
CORRECT:
```cpp
#include <iostream>
#include <map>
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
        int k;
        cin >> k;
        map<int, int> count;
        int pairs = 0;
        for (int x : v) {
            pairs += count[k - x];
            count[x]++;
        }
        cout << pairs << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <map>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    map<int, int> count;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int i = 0; i < n; i++) {
            cin >> v[i];
        }
        int k;
        cin >> k;
        int pairs = 0;
        for (int x : v) {
            pairs += count[k - x];
            count[x]++;
        }
        cout << pairs << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-distinct-rank
LANGUAGE: cpp
BUG: wrong_initial_value
CORRECT:
```cpp
#include <iostream>
#include <map>
#include <set>
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
        set<int> values(v.begin(), v.end());
        map<int, int> rank;
        int r = 0;
        for (int x : values) {
            rank[x] = r;
            r++;
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                cout << " ";
            }
            cout << rank[v[i]];
        }
        cout << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <map>
#include <set>
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
        set<int> values(v.begin(), v.end());
        map<int, int> rank;
        int r = 1;
        for (int x : values) {
            rank[x] = r;
            r++;
        }
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                cout << " ";
            }
            cout << rank[v[i]];
        }
        cout << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: aita-balanced-days
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        map<int, int> first;
        first[0] = -1;
        int balance = 0;
        int best = 0;
        for (int i = 0; i < (int) s.size(); i++) {
            if (s[i] == 'R') {
                balance++;
            } else {
                balance--;
            }
            if (first.count(balance)) {
                best = max(best, i - first[balance]);
            } else {
                first[balance] = i;
            }
        }
        cout << best << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        map<int, int> first;
        first[0] = -1;
        int balance = 0;
        int best = 0;
        for (int i = 0; i < (int) s.size(); i++) {
            if (s[i] == 'R') {
                balance++;
            } else {
                balance--;
            }
            if (first.count(balance)) {
                best = max(best, i - first[balance] + 1);
            } else {
                first[balance] = i;
            }
        }
        cout << best << endl;
    }
    return 0;
}
```
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
s = set()
for x in [4, 1, 4, 2, 1]:
    s.add(x)
print(sorted(s))
```
OPTIONS:
A) [4, 1, 4, 2, 1] || none
B) [4, 1, 2] || none
C) [1, 2, 4] || correct
D) [1, 1, 2, 4, 4] || none
EXPLANATION: Adding a value that is already in a set does nothing, and sorted gives the three values left in ascending order.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(len(a & b), len(a | b), len(a - b))
```
OPTIONS:
A) 2 7 2 || none
B) 2 5 2 || correct
C) 2 5 3 || none
D) 5 2 2 || none
EXPLANATION: The common values are 3 and 4, the union holds 1 to 5 once each, and only 1 and 2 are in a but not in b.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
first = {}
last = {}
for i, ch in enumerate("abcab"):
    if ch not in first:
        first[ch] = i
    last[ch] = i
print(first["a"], last["a"], last["c"] - first["c"])
```
OPTIONS:
A) 1 4 0 || off_by_one
B) 0 3 0 || correct
C) 0 0 0 || none
D) 3 3 0 || none
EXPLANATION: enumerate counts from 0, first keeps only the earliest position of each letter while last is overwritten every time, so a is at 0 and 3 and c appears only at 2.
=== END ===
