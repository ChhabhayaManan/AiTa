# Theory bank: stacks_queues

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: What is the difference between a stack and a queue? Give an everyday example of each.
MODEL ANSWER: A stack is last in, first out (LIFO): the item removed is always the one added most recently, like taking plates from the top of a pile or an undo history. A queue is first in, first out (FIFO): the item removed is the one that has waited longest, like people served in order in a line at a counter.
KEY POINTS:
- a stack is last in, first out: the most recent item is removed first
- a queue is first in, first out: the oldest item is removed first
- examples such as a pile of plates or undo (stack) and a waiting line (queue)
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: In an array-based stack with `int top` as the number of items, why must you check that the stack is not empty before popping?
MODEL ANSWER: Popping returns `stack[--top]`. If the stack is empty, `top` is 0, so this reads `stack[-1]`, outside the array, which is undefined behaviour, and `top` becomes negative, breaking every later operation. This error is called stack underflow. Checking `top > 0` first lets the program handle the empty case properly.
KEY POINTS:
- popping an empty stack reads outside the array (index -1)
- it is undefined behaviour and leaves top negative (stack underflow)
- check that top > 0 before popping
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: A balanced-bracket checker pushes opening brackets and pops on closing ones. Why must it also check that the stack is empty at the end?
MODEL ANSWER: For input such as `((`, no closing bracket ever arrives, so no mismatch is detected during the scan. The unclosed opening brackets are simply left on the stack. The string is balanced only if every opening bracket was matched, which means the stack must be empty once the whole string has been processed.
KEY POINTS:
- some unbalanced inputs never produce a mismatch during the scan
- unmatched opening brackets remain on the stack
- the string is balanced only if the stack is empty at the end
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: In a simple array queue with `head` and `tail` indexes, what problem appears when many items pass through, and how does a circular queue solve it?
MODEL ANSWER: Both indexes only ever move forward, so the slots before `head` are never reused. After enough enqueues `tail` reaches the end of the array even if the queue holds only a few items. A circular queue wraps the indexes around with `% capacity`, reusing freed slots at the front. It then needs a count of items, or one slot left empty, to tell a full queue from an empty one.
KEY POINTS:
- head and tail only move forward, so freed slots at the front are wasted
- tail reaches the end of the array even when the queue holds few items
- a circular queue wraps indexes with modulo capacity to reuse slots, tracking the count to distinguish full from empty
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: How is the function call stack an example of a stack data structure?
MODEL ANSWER: Each function call pushes a frame containing its return address, parameters and local variables. When a function returns, its frame is popped and execution continues in the caller, whose frame is now on top. The most recent call always finishes first, which is exactly the last-in-first-out rule. Because the stack has limited size, too many nested calls overflow it.
KEY POINTS:
- each call pushes a frame with its return address and local variables
- returning pops the frame and resumes the caller
- the most recent call finishes first (LIFO), and too deep nesting overflows the stack
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Why does breadth-first search with a queue find the shortest path in an unweighted grid, while using a stack instead would not guarantee it?
MODEL ANSWER: With a queue, cells are processed in the order they were discovered. The start is at distance 0, its neighbours at distance 1 are all processed before any cell at distance 2, and so on, level by level. So the first time a cell is reached, it is reached by a path with the fewest steps. A stack processes the most recently found cell first and dives deep along one route, so it can reach a cell first through a long path.
KEY POINTS:
- a queue processes cells in the order they were discovered
- all cells at distance d are processed before cells at distance d + 1
- the first time a cell is reached is by a shortest path; a stack goes deep and gives no such guarantee
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Why does `std::stack::pop()` return nothing, and how do you take the top item out?
MODEL ANSWER: `pop()` only removes the top element; it returns `void`. To get the value you first read it with `top()` and then call `pop()`. Keeping the two operations separate lets `top()` return a reference without copying and keeps the container safe if copying the element would throw an exception.
KEY POINTS:
- pop() removes the top element but returns void
- read the value with top() before calling pop()
- separating them avoids unnecessary copies and keeps the operation exception-safe
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What is the difference between LIFO and FIFO, and which of `std::stack` and `std::queue` follows each?
MODEL ANSWER: LIFO, last in first out, means the element removed is the one added most recently; `std::stack` follows it, with `push`, `top` and `pop`. FIFO, first in first out, means the oldest element is removed first; `std::queue` follows it, adding at the back with `push` and removing from the front with `front` and `pop`.
KEY POINTS:
- LIFO removes the most recently added element first
- FIFO removes the oldest element first
- std::stack is LIFO and std::queue is FIFO
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: `std::stack` and `std::queue` are called container adaptors. What does that mean, and what does `std::deque` offer that they do not?
MODEL ANSWER: An adaptor wraps an underlying container, by default a `deque`, and exposes only the operations that fit the abstraction: stack lets you work only at the top, queue only adds at the back and removes at the front. This expresses intent and prevents accidental misuse. A `deque` itself allows insertion and removal at both ends and indexing, so it is the choice when you need more than one kind of access, such as a sliding window.
KEY POINTS:
- an adaptor restricts an underlying container (deque by default) to certain operations
- stack and queue expose only top-based or front/back operations, preventing misuse
- deque allows adding and removing at both ends and random access
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: When checking brackets with a `stack<char>`, why is it not enough that every closing bracket matched the top?
MODEL ANSWER: Every closing bracket can match while some opening brackets are never closed, as in `(()`. Those leftover openers remain on the stack after the loop. The expression is balanced only when every opener has been matched, so the stack must also be empty once all characters are processed.
KEY POINTS:
- unclosed opening brackets do not cause a mismatch during the loop
- they remain on the stack at the end
- balanced means all closings matched and the stack is empty at the end
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Why is `std::priority_queue` not a first-in-first-out queue, and how do you make it return the smallest element first?
MODEL ANSWER: A priority_queue is a heap ordered by value, not by arrival time. `top()` always returns the largest element by default, regardless of when it was pushed, and `push` and `pop` take O(log n). To get the smallest first, declare it as `priority_queue<int, vector<int>, greater<int>>`, which reverses the comparison.
KEY POINTS:
- a priority_queue orders elements by priority (a heap), not by arrival order
- by default top() is the largest element; push and pop are O(log n)
- greater<int> as the comparator makes top() the smallest element
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Why does BFS on an unweighted grid, using `std::queue`, give shortest distances?
MODEL ANSWER: The queue releases cells in the order they were discovered. Starting from the source at distance 0, all cells at distance 1 are discovered and processed before any cell at distance 2, so the search expands in rings of increasing distance. When a cell is first discovered, its distance is therefore the minimum possible, and marking it visited at that moment keeps that shortest distance.
KEY POINTS:
- the queue processes cells in the order they were discovered
- the search expands level by level, by increasing distance
- the first discovery of a cell gives its shortest distance
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: How is a Python list used as a stack, and why are those operations fast?
MODEL ANSWER: The end of the list is the top of the stack: `append(x)` pushes, `pop()` removes and returns the last item, and `stack[-1]` peeks at the top. These operations work at the end of the underlying array, so no other elements are moved and they take constant (amortised) time.
KEY POINTS:
- append pushes and pop() removes from the end of the list
- stack[-1] reads the top item
- working at the end moves no other elements, so it is O(1)
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Explain LIFO and FIFO and say which one a stack and a queue follow.
MODEL ANSWER: LIFO, last in first out, means the most recently added item is taken out first; a stack works this way, like a pile of plates. FIFO, first in first out, means the item that has waited longest is taken out first; a queue works this way, like a line at a ticket counter.
KEY POINTS:
- LIFO takes out the most recent item first
- FIFO takes out the oldest item first
- a stack is LIFO and a queue is FIFO
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why is using `list.pop(0)` as a queue slow for large inputs, and why is `collections.deque` better?
MODEL ANSWER: A list stores its elements in one contiguous array, so removing the first element shifts every remaining element one place left, which takes O(n) time; doing that n times costs O(n²). A deque is designed for fast operations at both ends, so `append` and `popleft` take O(1) and the queue stays fast however long it gets.
KEY POINTS:
- a list is a contiguous array, so pop(0) shifts all other elements
- each pop(0) is O(n), giving O(n squared) for many operations
- deque supports O(1) append and popleft at both ends
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: A bracket checker never finds a mismatch for the input `"(()"`. Why must it still answer "not balanced", and how does it detect that?
MODEL ANSWER: Each closing bracket in `"(()"` correctly matches the top of the stack, so no mismatch happens during the scan. But one opening bracket is never closed and remains on the stack. The checker must test that the stack is empty after processing all characters; a non-empty stack means some brackets are unclosed.
KEY POINTS:
- no mismatch occurs during the scan for this input
- an unmatched opening bracket remains on the stack
- the stack must be empty at the end for the string to be balanced
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: How does `heapq` behave as a priority queue, and how do you get the largest item first?
MODEL ANSWER: `heapq` keeps a list arranged as a binary min-heap, so the smallest element is always at index 0. `heappush` and `heappop` take O(log n), and items come out in order of value, not in the order they were added. Python has no max-heap in heapq, so the usual trick is to push negated values and negate them again when popping.
KEY POINTS:
- heapq maintains a min-heap with the smallest item at index 0
- heappush and heappop are O(log n) and return items by value, not arrival order
- push negated values to simulate a max-heap
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why does breadth-first search with a `deque` give the shortest number of steps in an unweighted grid?
MODEL ANSWER: The deque hands out cells in the order they were discovered, so the search processes every cell at distance d before any cell at distance d + 1, spreading out level by level from the start. The first time a cell is discovered it is therefore through a shortest route, and marking it as visited then preserves that distance. A depth-first search would follow one path as far as possible and could reach a cell first by a longer route.
KEY POINTS:
- cells are processed in the order they were discovered
- the search expands in levels of increasing distance
- the first time a cell is reached is via a shortest path, unlike depth-first search
=== END ===
