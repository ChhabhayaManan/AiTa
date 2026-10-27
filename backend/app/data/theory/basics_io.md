# Theory bank: basics_io

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Why does `scanf("%d", &x)` need the `&` before `x`, while `scanf("%s", name)` for a `char name[20]` does not?
MODEL ANSWER: C passes arguments by value, so if scanf received the value of `x` it could only change its own copy. Passing `&x` gives scanf the address of `x`, and it stores the number through that address. An array name already converts to a pointer to its first element, so `name` is already an address and needs no `&`.
KEY POINTS:
- scanf has to store the value through an address (a pointer) to the variable
- C passes arguments by value, so without the address scanf cannot change the caller's variable
- an array name already converts to the address of its first element
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: What does `7 / 2` evaluate to in C, why, and how would you get `3.5` instead?
MODEL ANSWER: It evaluates to 3. Both operands are `int`, so C performs integer division and throws away the fractional part (it truncates toward zero). To get 3.5, at least one operand must be a floating-point value, for example `7.0 / 2` or `(double)a / b`.
KEY POINTS:
- both operands are int, so integer division is performed
- the fractional part is discarded, giving 3
- making one operand a double (a cast or 7.0) gives 3.5
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why is it a problem to print a `double` with `%d`, or to read a `long long` with `%d`? Explain what printf and scanf rely on.
MODEL ANSWER: printf and scanf take a variable number of arguments and the compiler does not convert them to match the format string. The functions trust the format code to know the type and size of each argument. If the code does not match, they read or write the wrong number of bytes, which is undefined behaviour: garbage output, wrong values, or memory being overwritten. Each type needs its own code, such as `%lld` for long long and `%lf` for reading a double.
KEY POINTS:
- printf/scanf use the format string to know the type and size of each argument
- there is no automatic type checking or conversion against the format
- a mismatch is undefined behaviour: wrong values, garbage, or memory corruption
- each type has its own specifier (for example %lld for long long, %lf for scanf of double)
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Two `int` variables each hold 100000. Why can `long long r = a * b;` still give a wrong answer, and how do you fix it?
MODEL ANSWER: The multiplication is done in `int` because both operands are `int`; the result is converted to long long only after it is computed. 100000 × 100000 = 10^10, which is larger than the int maximum of about 2.1 × 10^9, so it overflows first. Signed overflow is undefined behaviour and often wraps to a negative number. Converting one operand first, as in `(long long)a * b`, makes the multiplication happen in 64 bits.
KEY POINTS:
- the multiplication is evaluated in int before the assignment to long long
- 10^10 exceeds the int range of about 2.1 billion, so it overflows
- signed integer overflow is undefined behaviour (often a wrong or negative value)
- cast an operand to long long before multiplying
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: What does `scanf` return, and how can a program use that return value?
MODEL ANSWER: scanf returns the number of input items it successfully converted and stored. If the input ends before any conversion it returns EOF. A program can therefore loop with `while (scanf("%d", &x) == 1)` to read until the input runs out, or check the return value to detect input that does not match the format. When a conversion fails, the variable is left unchanged and the offending characters stay in the input stream.
KEY POINTS:
- it returns the number of items successfully converted and assigned
- it returns EOF when input ends before the first conversion
- the return value lets you read until end of input or detect invalid input
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: After `scanf("%d", &n);`, a following `scanf("%c", &c);` stores a newline in `c` instead of the next letter. Why, and how do you fix it?
MODEL ANSWER: `%d` reads the digits and stops before the newline that the user typed, so the `'\n'` remains in the input buffer. Unlike `%d` and `%s`, `%c` does not skip whitespace, so it reads that leftover newline immediately. Writing a space before the conversion, `scanf(" %c", &c)`, tells scanf to skip any whitespace first.
KEY POINTS:
- %d leaves the trailing newline in the input buffer
- %c does not skip whitespace, so it reads the leftover newline
- a space before %c (" %c") skips whitespace before reading the character
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: `scanf` needs format codes like `%d`, but `cin >> x` does not. How does `cin` know how to read the value?
MODEL ANSWER: `operator>>` is overloaded separately for each type. The compiler picks the version that matches the static type of the variable, so an `int` is parsed as a whole number and a `string` as a word. Because the choice is made from the type, there is no format code that can be mismatched, and the variable is taken by reference, so no `&` is needed.
KEY POINTS:
- operator>> is overloaded for each type
- the compiler chooses the reading code from the variable's type
- the variable is passed by reference, so no address or format code is needed
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What is the difference between ending a line with `"\n"` and with `endl`, and which should you prefer in a loop that prints 100000 lines?
MODEL ANSWER: Both write a newline character. `endl` additionally flushes the output buffer, forcing the text to be written out immediately. Flushing is slow, so doing it on every one of 100000 lines can make the program much slower. In large loops `"\n"` is preferred; the buffer is flushed automatically at the end.
KEY POINTS:
- both end the line with a newline
- endl also flushes the output buffer
- flushing on every line is slow, so prefer "\n" in big loops
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: After `cin >> n;`, a call to `getline(cin, line);` returns an empty string. Explain why and how to fix it.
MODEL ANSWER: `cin >> n` reads the number and stops before the newline, leaving `'\n'` in the stream. `getline` reads characters up to the next newline, so it immediately finds that leftover newline and returns an empty line. Discarding the rest of the line first with `cin.ignore()` (or `cin >> ws`) before calling getline fixes it.
KEY POINTS:
- >> stops before the newline and leaves it in the input stream
- getline reads up to the next newline, so it returns the empty remainder
- call cin.ignore() (or use cin >> ws) before getline
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: With `int a = 100000, b = 100000;`, why can `long long r = a * b;` be wrong, and what is the fix?
MODEL ANSWER: The type of the multiplication depends on its operands, not on the variable it is assigned to. Both are `int`, so `a * b` is computed in int, where 10^10 does not fit, and overflows before being converted to long long. Signed overflow is undefined behaviour. Writing `(long long)a * b` or `1LL * a * b` makes the multiplication itself 64-bit.
KEY POINTS:
- the multiplication is performed in int because both operands are int
- the result overflows before it is converted to long long
- signed overflow is undefined behaviour
- convert an operand to long long before multiplying
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: What do `ios::sync_with_stdio(false);` and `cin.tie(nullptr);` do, and what restriction do they bring?
MODEL ANSWER: By default C++ streams are synchronised with C's stdio so that `cin`/`cout` and `scanf`/`printf` can be mixed safely, which costs speed. `sync_with_stdio(false)` turns this off and lets the streams use their own buffering, making input and output much faster. `cin.tie(nullptr)` stops `cout` from being flushed before every read from `cin`. The restriction is that you must no longer mix C and C++ I/O on the same stream, or output can appear out of order.
KEY POINTS:
- by default C++ streams are synchronised with C stdio, which is slow
- sync_with_stdio(false) removes the synchronisation and speeds up I/O
- cin.tie(nullptr) stops cout from being flushed before each cin read
- afterwards you must not mix cin/cout with scanf/printf
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: What happens when `cin >> x` (with `int x`) meets the input `abc`, and why do all later reads also fail?
MODEL ANSWER: The extraction fails, `cin` sets its failbit, and the stream then converts to false, which is why `while (cin >> x)` stops. While the failbit is set, every further extraction does nothing. The characters `abc` are also still in the stream, so even after `cin.clear()` resets the state, they must be skipped (for example with `cin.ignore`) before reading again.
KEY POINTS:
- the failed extraction sets the stream's failbit and the stream evaluates to false
- later reads do nothing until the error state is cleared with clear()
- the invalid characters stay in the stream and must be discarded
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Why must you write `int(input())` to read a number, instead of just `input()`?
MODEL ANSWER: `input()` always returns a string, even when the user types digits. Using that string in arithmetic either joins text (`"3" + "8"` is `"38"`) or raises a TypeError when mixed with numbers. `int()` converts the text into an integer, and raises a ValueError if the text is not a valid number.
KEY POINTS:
- input() always returns a string
- string + string concatenates instead of adding, and string + int raises TypeError
- int() converts the text into an integer
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Explain the difference between `/`, `//` and `%` in Python, including what `-7 // 2` gives.
MODEL ANSWER: `/` is true division and always returns a float, so even `6 / 2` is `3.0`. `//` is floor division: it rounds the quotient down toward negative infinity, so `7 // 2` is 3 and `-7 // 2` is -4. `%` gives the remainder that matches `//`, so `a == (a // b) * b + a % b`, and its sign follows the divisor.
KEY POINTS:
- / always returns a float
- // is floor division, rounding down toward negative infinity (-7 // 2 is -4)
- % is the remainder consistent with //
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: The input line is `3 8`. Why does `n = int(input())` crash, and how do you read the two numbers correctly?
MODEL ANSWER: `input()` returns the whole line, `"3 8"`, including the space. `int()` cannot parse a string with two numbers in it and raises a ValueError. The line has to be split into separate pieces first and each piece converted, as in `a, b = map(int, input().split())`.
KEY POINTS:
- input() returns the whole line as one string
- int() cannot convert "3 8" and raises ValueError
- split the line into tokens and convert each with map(int, ...)
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Python's `int` never overflows. How is that possible, and why do problems still ask for answers modulo 1 000 000 007?
MODEL ANSWER: Python integers have arbitrary precision: they are stored in as many digits of memory as they need, so there is no fixed 32- or 64-bit limit. The cost is that arithmetic on very large numbers gets slower as the numbers grow, and they use more memory. Taking the modulo at each step keeps the numbers small, so the program stays fast, and it gives the same answer the problem expects in every language.
KEY POINTS:
- Python ints have arbitrary precision and grow as needed
- there is no fixed 32/64-bit limit, so no overflow
- operations on huge numbers become slower and use more memory, so keeping values small with a modulo still matters
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why is reading 100000 lines with `input()` slow, and why is `sys.stdin.read().split()` faster?
MODEL ANSWER: Every call to `input()` has fixed overhead: a Python function call, prompt handling, and stripping the newline, repeated 100000 times. `sys.stdin.read()` reads the whole input in one call, and `split()` breaks it into tokens in fast C code, so the per-line overhead disappears. The tokens are still strings and must be converted with `int()`.
KEY POINTS:
- input() has per-call overhead that adds up over many lines
- sys.stdin.read() reads all input in one call and split() tokenises it quickly
- the resulting tokens are strings that still need converting
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: A program prints 100000 answers with one `print` call each and is too slow. Why, and what is a better approach?
MODEL ANSWER: Every `print` call has overhead: it converts its arguments, writes to the output stream, and may flush. Repeating that 100000 times dominates the running time. Collecting the answers as strings in a list and printing `"\n".join(answers)` once does a single write, which is much faster.
KEY POINTS:
- each print call has its own overhead for conversion and writing
- many small writes are much slower than one large write
- collect results in a list and output them once with "\n".join
=== END ===
