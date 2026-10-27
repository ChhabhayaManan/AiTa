# Strings in Python

A string (`str`) is a sequence of characters. It knows its length, can be indexed and
sliced like a list, and comes with many useful methods.

## Basics

```python
name = "Asha"
print(len(name))     # 4
print(name[0])       # A
print(name[-1])      # a
print(name[1:3])     # sh
print(name + "!")    # Asha!
print("ab" * 3)      # ababab
```

## Strings are immutable

You **cannot** change a character in place: `name[0] = "U"` raises **TypeError**. Every
"change" makes a **new** string:

```python
name = "U" + name[1:]        # "Usha"
name = name.replace("U", "A")
```

To edit many characters, turn the string into a list, change the list, and join it back:

```python
chars = list(word)
chars[0] = chars[0].upper()
word = "".join(chars)
```

## Useful methods

| Code | Gives |
|---|---|
| `s.lower()`, `s.upper()` | a lowercase / uppercase copy |
| `s.strip()` | a copy without spaces at both ends |
| `s.split()` | a list of words |
| `" ".join(words)` | the words joined with spaces |
| `s.find("ab")` | index of the first match, or `-1` |
| `s.count("a")` | how many times it appears |
| `s.isdigit()`, `s.isalpha()` | is every character a digit / a letter? |
| `ord("a")`, `chr(97)` | character to code number, and back |

`ord(c) - ord("a")` gives a lowercase letter's position, 0 to 25.

## Building a long string

`s += piece` in a loop creates a new string every time and gets slow for long results.
Collect the pieces in a list and call `"".join(pieces)` once at the end.

## Comparing

`==` compares contents, and `<` compares alphabetically by character code, so uppercase
letters come before lowercase ones (`"Z" < "a"` is `True`).

## Worked example

Read a word and print how many vowels it has.

```python
word = input().strip()
count = 0
for ch in word:
    if ch in "aeiou":
        count += 1
print(count)
```

Input `programming` prints `3`. The shorter form is
`sum(1 for ch in word if ch in "aeiou")`.

## Common mistakes

- **Trying to assign `s[i] = ...`.** Build a new string or use a list.
- **Forgetting `strip()`**, so a trailing space or `\r` makes two equal-looking strings
  different.
- **`s.lower()` without saving the result**: it returns a new string and leaves `s` as it
  was.
- **`+=` in a long loop** instead of `join`.

## Remember

Strings index and slice like lists but cannot be changed: every method returns a new
string. Use `split` and `join` to move between text and lists of words.
