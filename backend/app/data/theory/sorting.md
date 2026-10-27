# Theory bank: sorting

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Explain how insertion sort works, and why it is fast on an array that is already almost sorted.
MODEL ANSWER: Insertion sort keeps a sorted part at the front of the array. It takes the next element and shifts larger elements of the sorted part one place right until it finds where the new element belongs, then places it there. On an almost sorted array each element only moves a few places, so the total work is close to n. On a reversed array every element moves all the way, giving about n² steps.
KEY POINTS:
- it grows a sorted prefix by inserting one element at a time
- larger elements are shifted right to make room for the new element
- on nearly sorted data each element moves only a little, so it runs in close to linear time (worst case n squared)
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Why is an n² sorting algorithm such as bubble sort too slow for 100000 numbers, while an n log n sort is fine?
MODEL ANSWER: For n = 100000, n² is 10^10 basic steps, and a program performs roughly 10^8 simple operations per second, so bubble sort would take on the order of 100 seconds. n log n is about 100000 × 17 ≈ 1.7 million steps, which finishes in a fraction of a second.
KEY POINTS:
- n squared for 100000 is 10^10 operations
- that is far beyond the roughly 10^8 operations per second available
- n log n is under 2 million operations, which is fast
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: A `qsort` comparator is written as `return a - b;`. Why can this sort incorrectly, and what is a safe alternative?
MODEL ANSWER: The comparator only needs to return a negative, zero or positive number. But `a - b` can overflow when the values are far apart, for example a large positive minus a large negative number; the result wraps and gets the wrong sign, so qsort puts the elements in the wrong order (and signed overflow is undefined behaviour). `return (a > b) - (a < b);` returns -1, 0 or 1 without any risk of overflow.
KEY POINTS:
- the comparator must return negative, zero, or positive
- a - b can overflow for values far apart, giving the wrong sign
- (a > b) - (a < b) is safe because it never overflows
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why does a `qsort` comparator take `const void *` parameters and cast them, and what does qsort's size argument tell it?
MODEL ANSWER: qsort is generic: it can sort arrays of any type, so it does not know the element type. It passes the comparator pointers to two elements as `const void *`, and the comparator must cast them back to the real type, such as `const int *`, and dereference them to compare values. The size argument tells qsort how many bytes each element occupies, so it can find and swap elements.
KEY POINTS:
- qsort is generic and does not know the element type
- the comparator receives void pointers to elements and must cast and dereference them
- the size argument gives the size in bytes of one element
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: What does it mean for a sort to be stable, when does it matter, and how can you get stable results from `qsort`?
MODEL ANSWER: A sort is stable if elements that compare equal keep their original relative order. It matters when records are sorted by one field and ties should follow the input order, or when sorting by several keys in passes. qsort is not guaranteed to be stable, so equal elements can be reordered. Adding a tie-breaker to the comparator, such as the original index of each record, makes the order fully defined.
KEY POINTS:
- a stable sort keeps equal elements in their original relative order
- it matters when ties must follow input order or when sorting in several passes
- qsort is not guaranteed stable, so add a tie-breaker such as the original index
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Why does sorting first make it possible to find duplicates in an array in O(n log n) instead of O(n²)?
MODEL ANSWER: Without sorting, finding duplicates means comparing every pair of elements, which is about n² / 2 comparisons. After sorting, equal values are next to each other, so one pass comparing each element with its neighbour finds every duplicate in O(n). The total cost is dominated by the sort, O(n log n).
KEY POINTS:
- without sorting you must compare all pairs, about n squared
- after sorting, equal values are adjacent
- one pass over neighbours finds them, so the total is O(n log n)
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What does `sort(v.begin(), v.end());` do, how do you sort in decreasing order, and how fast is it?
MODEL ANSWER: It sorts the elements in the range from `begin()` up to (not including) `end()` in place, in increasing order using `<`. Passing a comparator such as `greater<int>()` as a third argument sorts in decreasing order. std::sort runs in O(n log n) time.
KEY POINTS:
- it sorts the range [begin, end) in place in increasing order
- passing greater<int>() sorts in decreasing order
- it runs in O(n log n)
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Why would a hand-written bubble sort fail the time limit on 10^5 elements while `std::sort` passes?
MODEL ANSWER: Bubble sort performs about n² comparisons and swaps, which is 10^10 for n = 10^5, far more than the roughly 10^8 simple operations a program can do in a second. std::sort uses an O(n log n) algorithm, about 1.7 million operations here, which runs almost instantly.
KEY POINTS:
- bubble sort is O(n squared), about 10^10 steps for 10^5 elements
- that greatly exceeds the roughly 10^8 operations per second available
- std::sort is O(n log n), only a few million steps
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why is `[](int a, int b) { return a <= b; }` an invalid comparator for `std::sort`?
MODEL ANSWER: std::sort requires a strict weak ordering: the comparator must return true only when the first argument must come strictly before the second, and must return false for equal elements. With `<=`, comparing an element with an equal one (or itself) returns true, which breaks this rule. The result is undefined behaviour: the sort may produce a wrong order or even read outside the array and crash. Use `<` instead.
KEY POINTS:
- the comparator must define a strict weak ordering
- it must return false when the two elements are equal
- <= violates this and causes undefined behaviour, such as wrong order or a crash
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: How does sorting a `vector<pair<int,int>>` order its elements, and how would you sort people by score descending and then by name ascending?
MODEL ANSWER: Pairs are compared lexicographically: first by `first`, and only when the firsts are equal, by `second`. So the default sort orders by the first value and breaks ties with the second. For a custom order, pass a lambda that compares the primary key first and the secondary key only for ties: `if (a.score != b.score) return a.score > b.score; return a.name < b.name;`.
KEY POINTS:
- pairs compare by first, then by second on ties
- a custom comparator can compare the primary key first
- ties are broken by comparing the secondary key
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: What is the difference between `std::sort` and `std::stable_sort`, and when would you choose `stable_sort`?
MODEL ANSWER: `std::sort` does not guarantee that equal elements keep their original order, because it uses introsort, which moves elements around freely. `std::stable_sort` does guarantee it; it is typically a merge sort and may use extra memory. Choose stable_sort when ties must stay in input order, or when sorting in several passes, sorting by the less important key first and then by the more important one.
KEY POINTS:
- std::sort is not stable, so equal elements may be reordered
- stable_sort keeps equal elements in their original order, possibly using extra memory
- use it when ties must follow input order or for multi-pass sorting
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Plain quicksort can take O(n²) time. Why is `std::sort` still guaranteed to be O(n log n)?
MODEL ANSWER: Quicksort's worst case happens when the pivots repeatedly split the range very unevenly, for example always choosing the first element of an already sorted array, giving n levels of work. std::sort uses introsort: it starts as quicksort but watches the recursion depth, and when the depth exceeds about 2 log n it switches to heapsort, which is always O(n log n). It also uses insertion sort for small pieces. This guarantees O(n log n) in the worst case.
KEY POINTS:
- quicksort degrades to O(n squared) with consistently bad pivots
- std::sort uses introsort, switching to heapsort when recursion gets too deep
- this gives an O(n log n) worst-case guarantee
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: What is the difference between `sorted(nums)` and `nums.sort()`, and why is `nums = nums.sort()` a bug?
MODEL ANSWER: `sorted(nums)` returns a new sorted list and leaves `nums` unchanged; it works on any iterable. `nums.sort()` sorts the list itself in place and returns `None`. So `nums = nums.sort()` sorts the list and then replaces the variable with `None`, losing the list.
KEY POINTS:
- sorted() returns a new list and leaves the original unchanged
- list.sort() sorts in place and returns None
- assigning the result of sort() stores None
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Why should you use Python's built-in sort instead of writing bubble sort for 10^5 numbers?
MODEL ANSWER: Bubble sort takes about n² steps, 10^10 for 10^5 elements, which is far too slow, and especially slow in pure Python. The built-in sort (Timsort) runs in O(n log n) and is implemented in C, so it sorts 10^5 numbers in a small fraction of a second.
KEY POINTS:
- bubble sort is O(n squared), about 10^10 steps here
- the built-in sort is O(n log n)
- the built-in sort is implemented in C, making it much faster than Python loops
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: How does `key=` work in sorting, and how does `key=lambda p: (-p.score, p.name)` sort by score descending and name ascending?
MODEL ANSWER: The key function is called once on each element, and the elements are then ordered by those key values. Tuples compare element by element, so a tuple key sorts by its first item and uses the following items only to break ties. Negating the score reverses the order of that one numeric field, while the name is still compared in normal ascending order.
KEY POINTS:
- the key function computes a value for each element, and elements are sorted by those values
- tuple keys compare field by field, so later fields break ties
- negating a numeric field reverses only that field's order
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why does `sorted(["10", "9", "100"])` give `['10', '100', '9']`, and how do you sort them as numbers?
MODEL ANSWER: The values are strings, and strings are compared character by character: "1" comes before "9", so both "10" and "100" come before "9", and "10" comes before "100" because it is a prefix. To sort numerically, convert them, either beforehand with `int` or by passing `key=int` to sorted.
KEY POINTS:
- strings are compared character by character, not by numeric value
- "10" and "100" start with "1", which is less than "9"
- convert to int or use key=int to sort numerically
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Python's sort is stable. Explain what that means and how it lets you sort by two keys in two passes.
MODEL ANSWER: Stable means that elements with equal keys keep the relative order they had before the sort. To sort by department and, within each department, by name, first sort by name (the secondary key), then sort by department (the primary key). The second sort orders by department, and because it is stable, people in the same department keep the name order from the first sort.
KEY POINTS:
- stable sorting keeps elements with equal keys in their original order
- sort by the secondary key first, then by the primary key
- stability preserves the secondary order within equal primary keys
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why does Python 3 use a `key` function for sorting instead of a two-argument comparison function, and what do you do if you really need a comparison?
MODEL ANSWER: A key function is called once per element, n calls in total, and then the sort compares the resulting keys quickly. A comparison function would be called for every comparison, about n log n Python calls, which is much slower. Python 3 removed the `cmp` parameter for this reason; when a pairwise comparison is genuinely needed, `functools.cmp_to_key` wraps it into a key.
KEY POINTS:
- a key function is called once per element
- a comparison function would be called on every comparison, about n log n times
- Python 3 removed cmp; functools.cmp_to_key converts a comparison into a key
=== END ===
