# Theory bank: conditionals

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: A grading program checks `if (marks >= 50)` first and `else if (marks >= 90)` later, and nobody ever gets the top grade. Why does the order of conditions matter in an if / else if chain?
MODEL ANSWER: The conditions are tested from top to bottom, and only the first one that is true runs; the rest are skipped. Any mark of 90 or more is also at least 50, so the first, broader condition catches it and the `>= 90` branch is never reached. The strictest condition must come first.
KEY POINTS:
- conditions are checked from top to bottom
- only the first true branch runs and the rest are skipped
- a broader condition placed first catches cases meant for later branches, so the strictest goes first
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Why is `if (x = 5)` a bug in C even though it compiles?
MODEL ANSWER: `=` is assignment, not comparison. The expression stores 5 in `x` and its value is 5, which is non-zero, so the condition is always true. The original value of `x` is also lost. The comparison operator is `==`.
KEY POINTS:
- = assigns while == compares
- the assignment's value is 5, which is non-zero, so the condition is always true
- the variable x is overwritten
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why is `if (i < n && a[i] > 0)` safe while `if (a[i] > 0 && i < n)` can crash when `i == n`?
MODEL ANSWER: `&&` evaluates its left operand first and stops as soon as it is false, because the result is then known (short-circuit evaluation). In the first version, when `i < n` is false, `a[i]` is never read. In the second version `a[i]` is read first, even when `i` is out of range, which is undefined behaviour and can crash.
KEY POINTS:
- && evaluates left to right
- it stops when the left side is false (short-circuit)
- in the safe order the out-of-range a[i] is never accessed; reversed, it is read first, causing undefined behaviour
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: What happens in a `switch` when a `case` has no `break`, and when can that be useful?
MODEL ANSWER: Execution falls through: after the matching case's statements, it continues into the statements of the following case labels until it reaches a `break` or the end of the switch. This is a common bug when `break` is forgotten. It is useful when several cases share the same code, such as `case 'a': case 'e': case 'i': vowels++; break;`.
KEY POINTS:
- without break, execution continues into the following cases (fall-through)
- it continues until a break or the end of the switch
- it is useful to let several case labels share the same code
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Why can `if (0.1 + 0.2 == 0.3)` be false in C, and how should floating-point values be compared?
MODEL ANSWER: Doubles are stored in binary, and most decimal fractions such as 0.1 cannot be represented exactly. Each value is rounded, and the rounding errors mean that `0.1 + 0.2` is very slightly different from the stored `0.3`, so `==` fails. Floating-point values should be compared with a tolerance, for example `fabs(a - b) < 1e-9`.
KEY POINTS:
- binary floating point cannot represent most decimal fractions exactly
- rounding errors make mathematically equal results differ slightly
- compare with a small tolerance, such as fabs(a - b) < epsilon
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: In `if (a) if (b) x(); else y();`, which `if` does the `else` belong to, and how do you make the intent clear?
MODEL ANSWER: The `else` belongs to the nearest preceding `if` that has no else, so it pairs with `if (b)`. Indentation has no effect on how the compiler reads it, so code indented to suggest otherwise is misleading. Using braces around the inner `if` (or around each branch) makes the pairing explicit.
KEY POINTS:
- else binds to the nearest unmatched if (the inner one)
- indentation does not change how the compiler pairs them
- braces make the intended pairing explicit
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What does `if (n)` mean when `n` is an `int`, and what does `if (p)` mean when `p` is a pointer?
MODEL ANSWER: In a condition the value is converted to `bool`. For an integer, zero becomes false and any other value becomes true, so `if (n)` means `if (n != 0)`. For a pointer, a null pointer is false and any other pointer is true, so `if (p)` means `if (p != nullptr)`.
KEY POINTS:
- the value is converted to bool in a condition
- for integers, 0 is false and any non-zero value is true
- for pointers, nullptr is false and a non-null pointer is true
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Exactly one message must be printed for a temperature. Why use `else if` instead of a series of separate `if` statements?
MODEL ANSWER: Separate `if` statements are each checked independently, so when the conditions overlap, several of them can run and several messages are printed. With `else if`, once one condition is true its branch runs and all the remaining checks are skipped, so at most one branch runs. It also avoids evaluating conditions that are no longer needed.
KEY POINTS:
- separate ifs are each evaluated, so several can run
- else if skips the remaining branches after the first true one
- this guarantees at most one branch runs
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why does `cout << x > 0 ? "pos" : "neg";` not do what it seems, and how should the conditional operator be written inside a `cout` statement?
MODEL ANSWER: The conditional operator `?:` has a lower precedence than `<<` and `>`, so the expression is grouped as `((cout << x) > 0) ? ...`, which compares the stream itself with 0 instead of choosing a word to print, so it fails to compile in modern C++. The conditional expression must be wrapped in parentheses: `cout << (x > 0 ? "pos" : "neg");`. Both branches of `?:` must also have compatible types, because the whole expression yields a single value.
KEY POINTS:
- ?: has lower precedence than <<
- without parentheses, the stream insertion is grouped first
- wrap the conditional expression in parentheses inside cout
- both branches must have compatible types because ?: produces one value
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why is `if (!v.empty() && v.back() == x)` safe, but `if (v.back() == x && !v.empty())` is not?
MODEL ANSWER: `&&` evaluates the left side first and does not evaluate the right side when the left is false. In the first version, an empty vector makes `!v.empty()` false, so `v.back()` is never called. In the second version `back()` is called first, and calling it on an empty vector is undefined behaviour.
KEY POINTS:
- && evaluates left to right and stops when the left side is false
- the emptiness check protects the call to back()
- back() on an empty vector is undefined behaviour, so the order of the operands matters
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Why can you not `switch` on a `std::string` in C++, and what do you use instead?
MODEL ANSWER: `case` labels must be integral (or enumeration) constant expressions, known at compile time, because the compiler turns a switch into comparisons or a jump table over integer values. A `std::string` is an object, not an integral constant, so it cannot be a case label. You use an if / else if chain comparing strings with `==`, or a `map` / `unordered_map` from strings to values or actions.
KEY POINTS:
- case labels must be integral or enum compile-time constants
- the compiler implements switch with integer comparisons or a jump table
- for strings use an if/else-if chain or a map lookup
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Why should you avoid `if (a == b)` when `a` and `b` are `double` results of calculations?
MODEL ANSWER: Most decimal fractions cannot be stored exactly in binary floating point, so each operation introduces a tiny rounding error. Two calculations that are equal on paper can therefore differ in the last bits, making `==` false. Compare with a tolerance instead, for example `abs(a - b) < 1e-9`, choosing the tolerance to fit the size of the values.
KEY POINTS:
- floating-point values are rounded because most decimals have no exact binary form
- results equal on paper can differ slightly after calculation
- compare using a tolerance such as abs(a - b) < epsilon
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: How does Python know which lines belong to an `if` block, and what happens if the indentation is wrong?
MODEL ANSWER: Python uses indentation, not braces, to mark a block. The lines after the colon that are indented by the same amount belong to the `if`; the first line back at the outer level ends the block. Wrong indentation either raises an IndentationError or silently moves a line in or out of the block, changing what the program does.
KEY POINTS:
- Python uses indentation instead of braces to define blocks
- lines indented under the colon belong to the if
- wrong indentation causes an IndentationError or changes the program's logic
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: In an `if / elif / else` chain for grades, why must `marks >= 90` be tested before `marks >= 50`?
MODEL ANSWER: Python tests the conditions in order and runs only the first one that is true. A mark of 95 also satisfies `marks >= 50`, so if that test came first it would win, and the `>= 90` branch would never run. Putting the strictest condition first lets each branch catch only its own range.
KEY POINTS:
- conditions are checked in order from top to bottom
- only the first true branch runs
- a broader condition first would capture marks meant for the stricter branch
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: What does "truthy" and "falsy" mean in Python, and why can `if count:` be a bug when `count` may be 0?
MODEL ANSWER: In a condition every value is treated as true or false. `0`, `0.0`, `""`, empty lists and dicts, and `None` are falsy; almost everything else is truthy. `if count:` is therefore false both when `count` is missing (None) and when it is a valid 0. If 0 is a legitimate value, test explicitly, for example `if count is not None:`.
KEY POINTS:
- every value counts as true or false in a condition
- 0, empty strings and containers, and None are falsy
- if x: treats a valid 0 the same as a missing value, so test explicitly when 0 is allowed
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why is `if x == 1 or 2:` always true, and how should it be written?
MODEL ANSWER: Python groups it as `(x == 1) or 2`, not as "x equals 1 or 2". When `x == 1` is false, `or` evaluates to its right side, `2`, which is truthy, so the condition is always true. Write `if x == 1 or x == 2:` or, more simply, `if x in (1, 2):`.
KEY POINTS:
- it is parsed as (x == 1) or 2
- 2 is a truthy value, so the whole condition is always true
- write x == 1 or x == 2, or x in (1, 2)
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: What does `name = given or "guest"` store, and what does it show about how `and` and `or` work in Python?
MODEL ANSWER: `and` and `or` return one of their operands, not necessarily `True` or `False`. `or` returns its first truthy operand, or the last operand if none is truthy, so the line stores `given` when it is a non-empty string and `"guest"` otherwise. `and` returns its first falsy operand, or the last one. Both short-circuit, so the right side is not even evaluated when the left side decides the result.
KEY POINTS:
- and/or return one of their operands rather than a bool
- or returns the first truthy operand (otherwise the last); and returns the first falsy operand (otherwise the last)
- evaluation short-circuits, so the right side may never run
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: What is the difference between `==` and `is` in a condition, and when should `is` be used?
MODEL ANSWER: `==` compares values: it asks whether two objects are equal. `is` compares identity: it asks whether both names refer to the very same object. Small integers and some strings are cached by Python, so `is` sometimes appears to work for them by accident, but it is not reliable. `is` should be used only for identity checks such as `x is None`.
KEY POINTS:
- == tests equality of values
- is tests identity, whether both refer to the same object
- caching can make is seem to work by accident for small values, so use it only for checks like is None
=== END ===
