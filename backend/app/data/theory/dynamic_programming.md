# Theory bank: dynamic_programming

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: What is the "state" in a dynamic programming solution? Explain using the problem of counting ways to climb n stairs taking 1 or 2 steps at a time.
MODEL ANSWER: The state is the set of parameters that identifies one subproblem, together with a precise meaning for its value. For the stairs problem, `dp[i]` means "the number of ways to reach step i". Once the state is clear, the transition follows: the last move came from step i - 1 or i - 2, so `dp[i] = dp[i-1] + dp[i-2]`, and the answer is `dp[n]`.
KEY POINTS:
- the state identifies a subproblem and what its value means
- here dp[i] is the number of ways to reach step i
- a clear state gives the transition dp[i] = dp[i-1] + dp[i-2] and the answer dp[n]
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: What is the difference between top-down (memoisation) and bottom-up dynamic programming?
MODEL ANSWER: Top-down keeps the natural recursive function but stores each result in a table the first time it is computed, returning the stored value on later calls. Bottom-up fills the table with a loop, starting from the base cases and moving to larger states, so every state needed is already computed. Both compute each state once and give the same result; bottom-up avoids deep recursion and the risk of stack overflow.
KEY POINTS:
- top-down uses recursion and stores results the first time they are computed
- bottom-up fills a table iteratively from the base cases upward
- both compute each state once; bottom-up avoids deep recursion
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: A DP counts paths and asks for the answer modulo 1000000007. Why should the modulo be applied at every step rather than only at the end, and why use `long long`?
MODEL ANSWER: The counts grow exponentially and quickly exceed even a 64-bit integer, and overflowed values are wrong forever after. Modular arithmetic allows reducing at every step, because `(a + b) mod m = ((a mod m) + (b mod m)) mod m`, so the final result is the same. Reducing keeps every stored value below m, about 10^9, so the sum of two values fits safely in a `long long` (and products of two values fit too).
KEY POINTS:
- the counts grow very fast and overflow if not reduced
- (a + b) mod m can be computed from the reduced values, so reducing each step gives the correct result
- values stay below m, so sums and products fit in long long
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why does the order in which a DP table is filled matter?
MODEL ANSWER: Each state is computed from other states, so those states must already hold their final values when it is computed. If `dp[i]` depends on `dp[i-1]` and `dp[i-2]`, the loop must go from small i to large i. Filling in the wrong order reads entries that are still uninitialised or zero, and the results are wrong.
KEY POINTS:
- each state depends on other states
- those dependencies must be computed first (for example increasing i)
- the wrong order reads uncomputed values and gives wrong results
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: In the 0/1 knapsack with a one-dimensional array `dp[w]`, why must the capacity loop run from high to low for each item?
MODEL ANSWER: The update is `dp[w] = max(dp[w], dp[w - weight] + value)`, where `dp[w - weight]` should mean the best value using only the previous items. Going from low to high capacities, `dp[w - weight]` may already have been updated for the current item, so the item would be counted more than once, which solves the unbounded knapsack instead. Going from high to low, `dp[w - weight]` is still the value from before this item, so each item is used at most once.
KEY POINTS:
- the update reads dp[w - weight], which should come from the previous items only
- iterating upward lets the current item be reused, giving the unbounded knapsack
- iterating downward ensures each item is used at most once
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: With coins {1, 3, 4} and amount 6, why does the greedy method (always take the largest coin that fits) fail, and how does dynamic programming find the optimum?
MODEL ANSWER: Greedy takes 4, then 1 and 1, using 3 coins, but 3 + 3 uses only 2 coins. Greedy commits to the locally best choice without checking how it affects what is left. DP computes the best answer for every amount from 0 up to 6, with `dp[a] = 1 + min(dp[a - c])` over all coins c that fit, so it considers every possible last coin and builds on the optimal answers for smaller amounts.
KEY POINTS:
- greedy gives 4 + 1 + 1 (3 coins) while the optimum is 3 + 3 (2 coins)
- greedy commits to a local choice without considering the remainder
- DP tries every last coin using optimal answers for smaller amounts: dp[a] = 1 + min dp[a - c]
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: For counting paths from the top-left to cell (r, c) of a grid moving only right or down, define the DP state, transition and base cases.
MODEL ANSWER: The state `dp[r][c]` is the number of paths that reach cell (r, c). A path arrives either from the cell above or from the cell to the left, so `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. The base cases are the starting cell with 1 path, and the first row and first column, where there is only one way to arrive (blocked cells have 0).
KEY POINTS:
- dp[r][c] is the number of paths reaching cell (r, c)
- the transition adds the paths from above and from the left
- the base cases are the start cell (1) and the first row and column
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What two properties must a problem have for dynamic programming to apply?
MODEL ANSWER: First, overlapping subproblems: solving the problem leads to the same smaller subproblems many times, so storing their answers saves repeated work. Second, optimal substructure: an optimal answer to the problem can be built from optimal answers to its subproblems. When both hold, each subproblem can be solved once, stored and reused.
KEY POINTS:
- overlapping subproblems: the same smaller problems recur many times
- optimal substructure: the best solution is built from best solutions of subproblems
- then each subproblem is solved once and reused
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: In a memoised function, why is the memo table often filled with -1 at the start rather than 0?
MODEL ANSWER: The memo needs a value that means "not computed yet". If 0 can also be a real answer for some state, a table initialised with 0 cannot tell a computed 0 from a missing entry, so those states are recomputed every time and the speed-up can be lost entirely. A value that can never be a valid answer, such as -1, or a separate visited array, marks uncomputed states reliably.
KEY POINTS:
- the memo needs a marker meaning not yet computed
- if 0 is a valid answer, it cannot be distinguished from an empty entry and states are recomputed
- use an impossible value such as -1 or a separate visited array
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why must a counting DP apply `% MOD` at every step instead of once at the end?
MODEL ANSWER: The true counts grow exponentially, so they overflow a 64-bit `long long` after a few dozen steps, and once a value has overflowed it is wrong. Addition and multiplication are compatible with the modulo, so reducing the intermediate values gives the same final answer as reducing the exact count. Keeping every value below MOD also guarantees that adding two values never overflows.
KEY POINTS:
- the counts grow exponentially and overflow long long
- modular arithmetic allows reducing intermediate values without changing the result
- keeping values below MOD prevents overflow when combining them
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: In the 0/1 knapsack using a single `vector<long long> dp(W + 1)`, why must the inner loop go from W down to the item's weight?
MODEL ANSWER: The transition `dp[w] = max(dp[w], dp[w - wt] + val)` should combine the current item with the best value from the previous items only. If w increases, `dp[w - wt]` may already include the current item, so the same item can be taken several times, which is the unbounded knapsack. Iterating w downward reads `dp[w - wt]` before it is changed for the current item, so each item is used at most once.
KEY POINTS:
- dp[w - wt] must refer to the state before the current item was considered
- increasing w lets an item be counted multiple times
- decreasing w keeps each item used at most once
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: How can a DP whose row `i` depends only on row `i - 1` be rewritten to use much less memory, and what is lost?
MODEL ANSWER: Instead of the full n × W table, only two rows are kept, the previous one and the current one, swapping them after each step (or even a single row with the right loop order). Memory drops from O(n × W) to O(W), while the time stays the same. What is lost is the full history: you can no longer trace back which choices produced the optimum unless you store that information separately.
KEY POINTS:
- keep only the previous and current rows instead of the whole table
- memory falls from O(n × W) to O(W) with the same time
- the full table is gone, so reconstructing the chosen items needs extra storage
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: What does `dp[i]` represent in the stairs problem (1 or 2 steps at a time), and how is it computed?
MODEL ANSWER: `dp[i]` is the number of distinct ways to reach step i. Any way to reach step i ends with a single step from i - 1 or a double step from i - 2, so `dp[i] = dp[i-1] + dp[i-2]`. The base cases are `dp[0] = 1` and `dp[1] = 1`, and the answer is `dp[n]`.
KEY POINTS:
- dp[i] is the number of ways to reach step i
- the last move came from i - 1 or i - 2, so dp[i] = dp[i-1] + dp[i-2]
- base cases dp[0] = 1 and dp[1] = 1
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Compare a memoised recursive solution using `lru_cache` with a bottom-up loop that fills a list.
MODEL ANSWER: With `lru_cache`, you keep the recursive function and Python stores each result, so each state is computed only once when it is first needed. A bottom-up loop fills a list from the base cases upward, computing every state in order. Both take the same time; the memoised version is often quicker to write, while the loop avoids recursion overhead and the recursion limit.
KEY POINTS:
- lru_cache keeps the recursion and stores each result the first time
- bottom-up fills a table from the base cases in order
- both compute each state once; the loop avoids recursion overhead and the recursion limit
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: A memoised `ways(n)` with `@lru_cache` works for n = 500 but raises RecursionError for n = 100000. Why, and what is the fix?
MODEL ANSWER: Memoisation stops repeated work but not deep recursion: the first call `ways(100000)` still calls `ways(99999)`, and so on, nesting about 100000 calls before reaching the base case. That exceeds Python's recursion limit of about 1000 and raises RecursionError. Filling the table bottom-up with a loop computes the same states without any nesting.
KEY POINTS:
- memoisation removes repeated work but still recurses to depth n
- the depth exceeds Python's recursion limit of about 1000
- a bottom-up loop computes the same states without recursion
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why is `dp = [[0] * cols] * rows` a dangerous way to create a 2D DP table, and how should it be built?
MODEL ANSWER: The outer `* rows` repeats a reference to the same inner list, so all the rows are the same object. Updating `dp[r][c]` therefore changes that column in every row, silently corrupting the DP. A list comprehension, `[[0] * cols for _ in range(rows)]`, creates a separate list for each row.
KEY POINTS:
- multiplying the outer list repeats references to one inner list
- all rows are the same object, so an update affects every row
- build the table with a list comprehension to get independent rows
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: For the 0/1 knapsack with a one-dimensional list `dp`, why must the capacity loop be `for w in range(W, wt - 1, -1)` rather than increasing?
MODEL ANSWER: The update `dp[w] = max(dp[w], dp[w - wt] + val)` must use the best value without the current item. If w increases, `dp[w - wt]` may already have been updated with this item in the same pass, so the item can be added again and again, which models the unbounded knapsack. Iterating downward reads `dp[w - wt]` before it changes in this pass, so each item is taken at most once.
KEY POINTS:
- dp[w - wt] must be the value before the current item is used
- an increasing loop allows the same item to be added repeatedly
- a decreasing loop ensures each item is used at most once
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Coins are {1, 3, 4} and the amount is 6. Why does always taking the largest coin give the wrong minimum number of coins, and how does DP avoid the mistake?
MODEL ANSWER: The greedy choice takes 4 and then needs 1 + 1, three coins, while 3 + 3 needs only two. Greedy commits to the best-looking choice now without checking whether the remaining amount can be made efficiently. DP computes the minimum for every amount from 0 to 6, trying every coin as the last coin, `dp[a] = 1 + min(dp[a - c])`, so it always builds on the true optimum of each smaller amount.
KEY POINTS:
- greedy gives 4 + 1 + 1 (3 coins) but 3 + 3 (2 coins) is optimal
- greedy does not consider how a choice affects the remaining amount
- DP tries every coin as the last one using optimal smaller results: dp[a] = 1 + min dp[a - c]
=== END ===
