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
