# Theory bank: loops

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: How many times does `for (i = 0; i <= n; i++)` run, and why is that often a bug when looping over an array of size `n`?
MODEL ANSWER: It runs n + 1 times, for i = 0, 1, ..., n. An array of size n only has valid indexes 0 to n - 1, so the last repetition accesses `a[n]`, one element past the end, which is undefined behaviour. The usual form is `i < n`.
KEY POINTS:
- the loop runs n + 1 times (0 through n)
- an array of size n has valid indexes 0 to n - 1, so a[n] is out of bounds
- use i < n to run exactly n times
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: What is the difference between `break` and `continue` inside a loop?
MODEL ANSWER: `break` ends the loop immediately and execution continues after the loop. `continue` skips only the rest of the current repetition and moves on to the next one; in a `for` loop the update step (such as `i++`) still runs. Both affect only the innermost loop they are in.
KEY POINTS:
- break exits the loop entirely
- continue skips the rest of the current iteration and goes to the next one
- both apply only to the innermost enclosing loop
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: How does a `do { ... } while (cond);` loop differ from a `while (cond) { ... }` loop, and when is the do-while form the natural choice?
MODEL ANSWER: A while loop checks its condition before every repetition, so its body can run zero times. A do-while loop checks the condition after the body, so the body always runs at least once. That makes do-while natural when an action must happen before it can be checked, such as reading input and repeating until the value is valid.
KEY POINTS:
- while checks the condition before the body and may run zero times
- do-while checks after the body, so it always runs at least once
- it suits cases like reading input until it is valid
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: What happens with `for (i = 0; i < n; i++); { sum += a[i]; }` (note the semicolon after the loop header)?
MODEL ANSWER: The semicolon is an empty statement, and it becomes the loop's body. The loop therefore runs n times doing nothing, leaving `i` equal to n. The block in braces is not part of the loop; it runs once afterwards, using `a[n]`, which is out of bounds.
KEY POINTS:
- the semicolon is an empty statement that becomes the loop body
- the loop runs without doing any work
- the following block runs only once, after the loop, with i at its final value
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Why does `for (unsigned int i = n - 1; i >= 0; i--)` never terminate?
MODEL ANSWER: An unsigned integer can never be negative, so `i >= 0` is always true. When `i` is 0 and is decremented, it wraps around to the largest unsigned value instead of becoming -1, and the loop carries on (also reading far out of range). Use a signed `int` for a countdown, or a pattern such as `for (i = n; i-- > 0; )`.
KEY POINTS:
- unsigned values are never negative, so i >= 0 is always true
- decrementing 0 wraps around to the maximum unsigned value
- use a signed counter or a pattern like i-- > 0
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Two nested loops each run up to `n`. Why does this become too slow for n = 100000?
MODEL ANSWER: The inner loop runs completely for every repetition of the outer loop, so the total work is about n × n operations. For n = 100000 that is 10^10 operations, while a typical judge executes roughly 10^8 simple operations per second, so it would take on the order of 100 seconds. A faster approach is needed, for example sorting or hashing, which brings the work near n log n or n.
KEY POINTS:
- the inner loop runs fully for each outer iteration, giving about n × n operations
- 10^10 operations is far beyond the roughly 10^8 per second a program can do
- a better algorithm (such as sorting or hashing) is needed
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What is the difference between `for (int x : v)` and `for (int &x : v)` when the loop body changes `x`?
MODEL ANSWER: In `for (int x : v)` each `x` is a copy of an element, so changing it does not affect the vector. In `for (int &x : v)` each `x` is a reference to the element itself, so changes are made in the vector. For large elements you only read, `const auto &x` avoids copying them.
KEY POINTS:
- int x is a copy of each element, so changes do not affect the vector
- int &x is a reference, so changes modify the vector's elements
- const auto & avoids copies when only reading
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Why does `while (cin >> x)` stop when the input runs out?
MODEL ANSWER: The expression `cin >> x` returns the stream itself. When a stream is used as a condition it converts to true if the last operation succeeded and to false if it failed. At the end of input (or on invalid input) the extraction fails, the stream becomes false, and the loop ends.
KEY POINTS:
- cin >> x returns the stream
- the stream converts to false when an extraction fails
- reaching end of input makes the extraction fail, ending the loop
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Inside two nested loops, a `break` in the inner loop does not stop the outer loop. Why, and how can you leave both loops at once?
MODEL ANSWER: `break` only exits the innermost loop that contains it; the outer loop then continues with its next repetition. To leave both, you can set a flag and check it in the outer loop's condition, or put the loops in a function and `return` from it when done (a `goto` to a label after the loops also works but is rarely used).
KEY POINTS:
- break exits only the innermost enclosing loop
- the outer loop keeps running
- use a flag, or move the loops into a function and return
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why is it dangerous to call `v.push_back(...)` inside `for (int x : v)`?
MODEL ANSWER: A range-based for loop works with iterators to the vector's storage. `push_back` may need more space, in which case the vector allocates a new block and moves its elements there. The iterators the loop is using then point to freed memory, which is undefined behaviour. Use an index loop with a fixed bound, or collect the new elements in a separate vector.
KEY POINTS:
- the range-based loop uses iterators into the vector
- push_back can reallocate the vector's storage
- the loop's iterators become invalid, causing undefined behaviour
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: What goes wrong with `for (size_t i = v.size() - 1; i >= 0; i--)`, especially when `v` is empty?
MODEL ANSWER: `size_t` is unsigned, so `i >= 0` is always true and the loop never stops; decrementing 0 wraps around to a huge number. When `v` is empty it is even worse: `v.size() - 1` itself wraps to the maximum value, so the very first access is far out of range. Use a signed int, or count down with `for (size_t i = v.size(); i-- > 0; )`.
KEY POINTS:
- size_t is unsigned, so i >= 0 is always true
- decrementing 0 wraps to a huge value instead of -1
- for an empty vector, v.size() - 1 already wraps to a huge index
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: A solution compares every pair of elements with two nested loops. Why is that too slow for 10^5 elements, and what is the general way out?
MODEL ANSWER: Checking all pairs takes about n × n / 2 steps, roughly 5 × 10^9 for n = 10^5, while about 10^8 simple operations run per second. The program would need tens of seconds. The way out is a different algorithm, for example sorting first so that related elements are adjacent, or using a hash set for lookups, reducing the work to around n log n or n.
KEY POINTS:
- comparing all pairs is on the order of n squared operations
- that is billions of operations for n = 10^5, far over a time limit
- use a better algorithm such as sorting or hashing
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Which numbers does `range(1, n)` produce, and how do you loop from 1 to n inclusive?
MODEL ANSWER: `range(a, b)` starts at `a` and stops before `b`; the end value is never included. So `range(1, n)` gives 1 up to n - 1. To include n, write `range(1, n + 1)`. Likewise `range(n)` gives exactly n values, 0 to n - 1.
KEY POINTS:
- range excludes its end value
- range(1, n) gives 1 to n - 1
- use range(1, n + 1) to include n
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Why is `for x in items:` usually better than `for i in range(len(items)):`, and how do you get the index when you need it?
MODEL ANSWER: `for x in items` gives you each element directly, so there is no index arithmetic to get wrong and the code is shorter and clearer. When you also need the position, `enumerate(items)` yields pairs of index and value, as in `for i, x in enumerate(items):`.
KEY POINTS:
- for x in items iterates over the values directly
- it avoids index arithmetic and off-by-one mistakes
- enumerate gives (index, value) pairs when the index is needed
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why does `for x in nums: if x % 2 == 0: nums.remove(x)` fail to remove all even numbers from `[2, 4, 6, 7]`?
MODEL ANSWER: The for loop walks the list by position. Removing an element shifts every later element one place to the left, so the element that moves into the current position is skipped when the loop advances. Here 4 slides into the place of 2 and is never checked. Loop over a copy (`nums[:]`) or build a new list, such as `[x for x in nums if x % 2]`.
KEY POINTS:
- the loop advances through the list by position
- removing an element shifts the following elements left
- the element that shifts into the current position gets skipped; iterate over a copy or build a new list
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: What does the `else` block of a Python `for` loop do, and when is it useful?
MODEL ANSWER: The `else` block runs when the loop finishes normally, having gone through all its items, and is skipped if the loop was left with `break`. It is useful for searches: break when the item is found, and put the "not found" handling in the `else`, without needing a separate flag variable.
KEY POINTS:
- the else runs when the loop completes without break
- it does not run if the loop exits through break
- it replaces a found/not-found flag in search loops
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Inside `for i in range(10):`, the body sets `i = i + 5`. Why does this not make the loop skip ahead?
MODEL ANSWER: The for loop takes its next value from the range object on every repetition, independently of what the body did to `i`. Assigning to `i` only changes the local name until the next repetition, when it is overwritten with the next value from the range. To control the index yourself, use a `while` loop.
KEY POINTS:
- the next value comes from the range iterator each iteration
- assigning to i only changes the name until the next iteration
- use a while loop to control the index manually
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why can building a long result with `s += piece` inside a loop be slow, and what is the standard alternative?
MODEL ANSWER: Strings are immutable, so `s += piece` creates a new string and copies all the existing characters into it each time. Over many repetitions the total copying grows roughly with the square of the final length. Collecting the pieces in a list and calling `"".join(pieces)` once at the end copies each character only once.
KEY POINTS:
- strings are immutable, so each += builds a new string
- copying the old contents each time can make the total work quadratic
- append pieces to a list and join them once at the end
=== END ===
