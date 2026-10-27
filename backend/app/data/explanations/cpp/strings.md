# Strings in C++

C++ has a real text type, `std::string`, from `<string>`. It knows its length, grows as
needed, and can be compared and joined with ordinary operators.

## Making and reading strings

```cpp
#include <string>

string name = "Asha";
cout << name.size() << "\n";   // 4
cout << name[0] << "\n";       // A: characters are indexed from 0

string word;
cin >> word;                   // one word, stops at a space
string line;
getline(cin, line);            // a whole line, spaces included
```

After `cin >> n`, the newline is still waiting, so a following `getline` returns an empty
line. Put `cin.ignore();` between them.

## What you can do with a string

| Code | Does |
|---|---|
| `s.size()` | number of characters |
| `s[i]` | the character at index `i` (a `char`) |
| `a + b`, `s += "x"`, `s.push_back('x')` | join |
| `a == b`, `a < b` | compare by content, alphabetically |
| `s.substr(i, len)` | the part starting at `i`, `len` characters long |
| `s.find("ab")` | index of the first match, or `string::npos` if none |
| `to_string(42)`, `stoi("42")` | number to text, text to number |

Strings are **mutable**: `s[0] = 'H';` changes the first character.

## Characters are small numbers

A `char` holds a character code, so you can compare and do arithmetic:
`c >= 'a' && c <= 'z'` checks for a lowercase letter, `c - 'a'` gives 0 to 25, and
`toupper(c)` from `<cctype>` makes it uppercase.

## Building a long string

`result += piece;` in a loop is fine. `result = result + piece;` makes a new copy each time
and gets slow for long strings.

## Worked example

Read a word and print how many vowels it has.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string w;
    cin >> w;
    int count = 0;
    for (char c : w) {
        if (string("aeiou").find(c) != string::npos) {
            count++;
        }
    }
    cout << count << "\n";
    return 0;
}
```

Input `programming` prints `3`.

## C strings still exist

A literal like `"hello"` is a C-style `const char` array ending in `'\0'`. Assigning it to a
`string` copies it, so you never have to manage the `'\0'` yourself. You only meet C strings
when a function asks for one; `s.c_str()` gives it.

## Common mistakes

- **`cin >>` then `getline`** without `cin.ignore()`.
- **Checking `find` against `-1`** instead of `string::npos`.
- **Indexing past the end**: `s[s.size()]` is not a real character.
- **`s.size() - 1` on an empty string** wraps around to a huge number.

## Remember

Use `std::string`: it knows its size, grows, and compares with `==` and `<`. Read words with
`cin >>` and lines with `getline`.
