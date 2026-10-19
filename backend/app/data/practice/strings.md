# Strings

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "hello";
    printf("%c%c\n", s[0], s[4]);
    return 0;
}
```
OPTIONS:
A) hl || off_by_one
B) ho || correct
C) he || none
D) h0 || none
EXPLANATION: s[0] is the first character h and s[4] is the fifth character o.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: easy
STEM:
What does this program print?
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    printf("%d\n", (int) strlen("code"));
    return 0;
}
```
OPTIONS:
A) 5 || off_by_one
B) 3 || off_by_one
C) 4 || correct
D) 0 || none
EXPLANATION: strlen counts the characters before the terminating '\0', so "code" has length 4.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[10] = "cat";
    printf("%d\n", (int) sizeof(s));
    return 0;
}
```
OPTIONS:
A) 3 || none
B) 4 || off_by_one
C) 8 || none
D) 10 || correct
EXPLANATION: sizeof gives the size of the whole array, 10 chars, no matter how long the text stored in it is.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>

int main(void) {
    char s[] = "abc";
    s[1] = 'X';
    printf("%s\n", s);
    return 0;
}
```
OPTIONS:
A) aXc || correct
B) Xbc || off_by_one
C) abX || none
D) abc || none
EXPLANATION: s is a char array, so its characters can be changed; index 1 is the middle character.
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: medium
STEM:
What does this program print?
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[] = "apple";
    char b[] = "apply";
    printf("%d\n", strcmp(a, b) < 0);
    return 0;
}
```
OPTIONS:
A) 0 || none
B) -1 || none
C) 1 || correct
D) 5 || none
EXPLANATION: strcmp compares character by character; at the first difference 'e' comes before 'y', so the result is negative and the comparison < 0 is true (1).
=== END ===

=== QUESTION ===
LANGUAGE: c
DIFFICULTY: hard
STEM:
What does this program print?
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "hello";
    s[2] = '\0';
    printf("%s %d\n", s, (int) strlen(s));
    return 0;
}
```
OPTIONS:
A) hello 5 || none
B) helo 4 || none
C) hel 3 || off_by_one
D) he 2 || correct
EXPLANATION: A C string ends at the first '\0', so after s[2] = '\0' only "he" is seen.
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
    cout << s.length() << " " << s[1] << endl;
    return 0;
}
```
OPTIONS:
A) 5 h || off_by_one
B) 5 e || correct
C) 6 e || off_by_one
D) 4 e || none
EXPLANATION: length() is the number of characters, 5, and s[1] is the second character.
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
    string a = "good";
    string b = "bye";
    cout << a + " " + b << endl;
    return 0;
}
```
OPTIONS:
A) goodbye || none
B) good + bye || none
C) good bye || correct
D) bye good || none
EXPLANATION: + joins strings in order, including the " " in the middle.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "banana";
    cout << s.find("an") << endl;
    return 0;
}
```
OPTIONS:
A) 1 || correct
B) 2 || off_by_one
C) 3 || none
D) 0 || none
EXPLANATION: find returns the index where the first match starts; "an" first appears at index 1.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "programming";
    cout << s.substr(3, 4) << endl;
    return 0;
}
```
OPTIONS:
A) gra || none
B) ogra || off_by_one
C) gram || correct
D) gramm || none
EXPLANATION: substr(3, 4) starts at index 3 and takes 4 characters: g, r, a, m.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: medium
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "abc";
    s += 'd';
    s[0] = 'z';
    cout << s << endl;
    return 0;
}
```
OPTIONS:
A) zbc || none
B) zbcd || correct
C) abcd || none
D) zabcd || none
EXPLANATION: += adds d to the end, and s[0] = 'z' replaces the first character.
=== END ===

=== QUESTION ===
LANGUAGE: cpp
DIFFICULTY: hard
STEM:
What does this program print?
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "level";
    int count = 0;
    for (char c : s) {
        if (c == 'e') {
            count++;
        }
    }
    cout << count << s.back() << endl;
    return 0;
}
```
OPTIONS:
A) 1l || none
B) 2e || none
C) 2l || correct
D) 3l || none
EXPLANATION: "level" contains two e characters, and back() is its last character, l.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: easy
STEM:
What does this program print?
```python
s = "Python"
print(s[0], s[-1], len(s))
```
OPTIONS:
A) P n 6 || correct
B) P o 6 || off_by_one
C) P n 5 || off_by_one
D) y n 6 || off_by_one
EXPLANATION: s[0] is the first character, s[-1] the last, and the word has six characters.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: medium
STEM:
What does this program print?
```python
s = "hello"
s.upper()
print(s)
```
OPTIONS:
A) HELLO || none
B) Hello || none
C) None || none
D) hello || correct
EXPLANATION: Strings cannot be changed in place; upper() returns a new string, and here that result is thrown away.
=== END ===

=== QUESTION ===
LANGUAGE: python
DIFFICULTY: hard
STEM:
What does this program print?
```python
print("-".join("abc"[::-1]))
```
OPTIONS:
A) a-b-c || none
B) c-b-a || correct
C) cba || none
D) -c-b-a- || none
EXPLANATION: [::-1] reverses the string to "cba", and join puts "-" between its characters.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
A program compares the strings Apple and apple character by character, exactly as given. Are they equal?
OPTIONS:
A) Yes, because they spell the same word || none
B) Yes, because comparing strings ignores upper and lower case || none
C) No, because an uppercase letter and its lowercase form are different characters || correct
D) It depends on how long the strings are || none
EXPLANATION: 'A' and 'a' have different character codes, so an exact comparison treats them as different.
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: easy
STEM:
What does it mean to concatenate two strings?
OPTIONS:
A) Join them, one after the other, into one longer string || correct
B) Compare them to see which comes first alphabetically || none
C) Find where the second string appears inside the first || none
D) Swap their contents || none
EXPLANATION: Concatenating "ab" and "cd" gives "abcd".
=== END ===

=== QUESTION ===
LANGUAGE: any
DIFFICULTY: medium
STEM:
A program must count the vowels in a sentence. Which approach works?
OPTIONS:
A) Compare the whole sentence once with the text "aeiou" || none
B) Look at each character in turn and add 1 to a counter whenever it is a vowel || correct
C) Divide the length of the sentence by 5 || none
D) Count only the first and last characters || none
EXPLANATION: Counting means visiting every character once with a loop and keeping a running total.
=== END ===

=== DEBUG ===
PROBLEM: dsa-reverse-string
LANGUAGE: python
BUG: off_by_one
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input()
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result += s[i]
    print(result)
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = input()
    result = ""
    for i in range(len(s) - 1, 0, -1):
        result += s[i]
    print(result)
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-reverse-string
LANGUAGE: c
BUG: wrong_comparison_operator
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int len = strlen(line);
        for (int i = len - 1; i >= 0; i--) {
            putchar(line[i]);
        }
        putchar('\n');
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int len = strlen(line);
        for (int i = len - 1; i > 0; i--) {
            putchar(line[i]);
        }
        putchar('\n');
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-palindrome
LANGUAGE: python
BUG: index_out_of_range
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input()
    is_palindrome = True
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - 1 - i]:
            is_palindrome = False
            break
    print("YES" if is_palindrome else "NO")
```
BUGGY:
```python
t = int(input())
for _ in range(t):
    s = input()
    is_palindrome = True
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - i]:
            is_palindrome = False
            break
    print("YES" if is_palindrome else "NO")
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-palindrome
LANGUAGE: c
BUG: uninitialised_variable
CORRECT:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int len = strlen(line);
        int is_palindrome = 1;
        for (int i = 0; i < len / 2; i++) {
            if (line[i] != line[len - 1 - i]) {
                is_palindrome = 0;
                break;
            }
        }
        printf("%s\n", is_palindrome ? "YES" : "NO");
    }
    return 0;
}
```
BUGGY:
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    int is_palindrome = 1;
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int len = strlen(line);
        for (int i = 0; i < len / 2; i++) {
            if (line[i] != line[len - 1 - i]) {
                is_palindrome = 0;
                break;
            }
        }
        printf("%s\n", is_palindrome ? "YES" : "NO");
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: dsa-palindrome
LANGUAGE: cpp
BUG: off_by_one
CORRECT:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string s;
        getline(cin, s);
        int n = s.size();
        bool palindrome = true;
        for (int i = 0; i < n / 2; i++) {
            if (s[i] != s[n - 1 - i]) {
                palindrome = false;
                break;
            }
        }
        cout << (palindrome ? "YES" : "NO") << endl;
    }
    return 0;
}
```
BUGGY:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        string s;
        getline(cin, s);
        int n = s.size();
        bool palindrome = true;
        for (int i = 0; i < n / 2; i++) {
            if (s[i] != s[n - i]) {
                palindrome = false;
                break;
            }
        }
        cout << (palindrome ? "YES" : "NO") << endl;
    }
    return 0;
}
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-231
LANGUAGE: python
BUG: uninitialised_variable
CORRECT:
```python
t = int(input())
for _ in range(t):
    s = input()
    count = 0
    for ch in s:
        if ch in "aeiouAEIOU":
            count += 1
    print(count)
```
BUGGY:
```python
t = int(input())
count = 0
for _ in range(t):
    s = input()
    for ch in s:
        if ch in "aeiouAEIOU":
            count += 1
    print(count)
```
=== END ===

=== DEBUG ===
PROBLEM: mbpp-231
LANGUAGE: c
BUG: off_by_one
CORRECT:
```c
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int count = 0;
        for (int i = 0; line[i] != '\0'; i++) {
            char c = tolower((unsigned char) line[i]);
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
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
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[600];
    int t;
    fgets(line, sizeof line, stdin);
    sscanf(line, "%d", &t);
    while (t--) {
        fgets(line, sizeof line, stdin);
        line[strcspn(line, "\r\n")] = '\0';
        int count = 0;
        for (int i = 1; line[i] != '\0'; i++) {
            char c = tolower((unsigned char) line[i]);
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                count++;
            }
        }
        printf("%d\n", count);
    }
    return 0;
}
```
=== END ===
