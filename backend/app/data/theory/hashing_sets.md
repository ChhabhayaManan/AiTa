# Theory bank: hashing_sets

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: How does a counting array such as `int count[1001]` act as a very simple hash table, and what are its limits?
MODEL ANSWER: The value itself is used as the index, so `count[v]++` records an occurrence of v and `count[v]` reads it back, each in constant time. This only works when the values are small non-negative integers: the array needs one slot for every possible value up to the maximum, so huge ranges do not fit in memory, and negative values must first be shifted by an offset.
KEY POINTS:
- the value is used directly as the array index
- updates and lookups take constant time
- it needs a slot for every possible value, so it only suits small non-negative ranges (shift negatives)
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Why is checking "have I seen this value before?" with a hash table faster than comparing with every earlier element?
MODEL ANSWER: Comparing each element with all earlier ones takes about n²/2 comparisons. A hash table, or a seen-array for small values, answers "was this value inserted?" in about constant time, because the value leads straight to its slot. Over n elements that is about n steps in total instead of n².
KEY POINTS:
- comparing with all earlier elements takes about n squared comparisons
- a hash table or seen-array answers membership in about constant time
- the whole pass becomes about linear
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: What is a collision in a hash table, why can collisions not be avoided, and how does linear probing deal with them?
MODEL ANSWER: A collision happens when two different keys hash to the same slot. They are unavoidable because there are far more possible keys than slots, so some keys must share a slot. With linear probing, if the slot is occupied by a different key, the table tries the next slot, and the next, until it finds the key or an empty slot. Lookups follow the same sequence, so they find keys that were moved along.
KEY POINTS:
- a collision is two different keys mapping to the same slot
- it is unavoidable because there are more possible keys than slots
- linear probing checks the following slots until it finds the key or an empty slot, and lookups follow the same path
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why can `slot = x % SIZE` produce an invalid array index in C, and how do you fix it?
MODEL ANSWER: In C the result of `%` takes the sign of the left operand, so for a negative `x` the remainder is negative, for example `-7 % 10` is `-7`. Using it as an index reads outside the array. Normalising with `((x % SIZE) + SIZE) % SIZE`, or casting to an unsigned type first, always gives an index between 0 and SIZE - 1.
KEY POINTS:
- in C, % with a negative left operand gives a negative result
- a negative slot is an out-of-bounds index
- normalise with ((x % SIZE) + SIZE) % SIZE to get 0..SIZE-1
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: What is the load factor of a hash table, and why does performance degrade as an open-addressing table fills up?
MODEL ANSWER: The load factor is the number of stored keys divided by the number of slots. As it grows, occupied slots form long runs (clusters), so linear probing has to step through many slots to find a key or an empty place. Near full, operations approach O(n). Keeping the load factor low, for example sizing the table at least twice the number of keys, keeps the probe sequences short and operations close to constant time.
KEY POINTS:
- load factor is the number of keys divided by the number of slots
- a fuller table forms clusters, making probe sequences longer
- operations degrade toward O(n), so keep the load factor low by making the table larger
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: In a linear-probing hash table, why can you not delete a key by simply marking its slot as empty?
MODEL ANSWER: A lookup stops when it reaches an empty slot, assuming the key is not present. Other keys may have been placed after the deleted one because of collisions. If the deleted slot becomes empty, lookups for those later keys stop early and wrongly report them as missing. Instead the slot is marked with a special "deleted" tombstone that lookups skip over and insertions may reuse.
KEY POINTS:
- lookups stop at the first empty slot
- keys inserted later in the probe sequence would become unreachable
- use a tombstone marker that lookups skip but inserts can reuse
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What is the difference between `std::set` and `std::unordered_set`, and how do you choose between them?
MODEL ANSWER: `std::unordered_set` is a hash table: insert, erase and lookup take constant time on average, but it keeps no order. `std::set` is a balanced binary search tree: operations take O(log n), and it keeps its elements in sorted order, supporting things like `lower_bound`. Use unordered_set when you only need membership tests, and set when you need sorted order or nearest-value queries.
KEY POINTS:
- unordered_set is a hash table with average O(1) operations and no order
- set is a balanced tree with O(log n) operations that keeps elements sorted
- choose set when order or ordered queries are needed, otherwise unordered_set
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Why does `if (m[key] > 0)` change the size of an `unordered_map`, and how should membership be tested?
MODEL ANSWER: `operator[]` inserts the key with a default value (0 for int) when it is missing, then returns a reference to it. So merely testing a missing key adds it to the map, growing it and possibly affecting later loops over the map. To check without inserting, use `m.count(key)`, `m.find(key) != m.end()`, or `m.contains(key)` in C++20.
KEY POINTS:
- operator[] inserts a default value for a missing key
- testing with [] silently grows the map
- use count, find, or contains to check membership without inserting
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: How does `std::unordered_map` handle two keys that hash to the same bucket?
MODEL ANSWER: The hash function maps each key to a bucket. Keys that land in the same bucket collide, and the standard implementation keeps them together in that bucket (separate chaining). A lookup hashes the key to find its bucket and then compares the key with each element in that bucket using `==`. As long as keys are spread evenly and buckets stay short, operations take constant time on average.
KEY POINTS:
- the hash picks a bucket, and colliding keys share the bucket (chaining)
- lookup searches the bucket comparing keys with ==
- with an even spread, operations are constant time on average
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why should a program not depend on the order in which it iterates over an `unordered_set`?
MODEL ANSWER: Elements are stored by bucket, according to their hashes, not by insertion order or value. The order you see can change when the table grows and rehashes, and it can differ between compilers and library versions. If output order matters, iterate over the original input, sort the elements, or use `std::set`.
KEY POINTS:
- elements are arranged by hash bucket, not by insertion or value order
- the order can change after rehashing or between implementations
- iterate the input, sort, or use set when order matters
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: `unordered_map` operations are O(1) on average. When can they become O(n), and how can this be guarded against?
MODEL ANSWER: If many keys hash to the same bucket, that bucket becomes a long chain and each operation has to scan it, so operations degrade to O(n) and the whole program toward O(n²). This can happen by accident with a poor hash, or deliberately, since the default integer hash is predictable and inputs can be crafted to collide. Using a custom hash with a random seed (for example based on splitmix64) or a `std::map` with guaranteed O(log n) avoids it; `reserve` reduces rehashing costs.
KEY POINTS:
- when many keys collide in one bucket, operations degrade to O(n)
- predictable default hashes allow crafted inputs that collide
- a randomised custom hash or an ordered map with guaranteed O(log n) avoids the worst case
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: Why does `unordered_set<pair<int,int>> seen;` fail to compile, and what are your options?
MODEL ANSWER: An unordered container needs a hash function for its key type, and the standard library does not provide `std::hash` for `pair`. You can supply your own hash functor that combines the hashes of both members, encode the pair into one integer such as `(long long)a * BIG + b` and store that instead, or use `std::set<pair<int,int>>`, which needs only `<`, which pairs already have.
KEY POINTS:
- unordered containers need a std::hash for the key type
- std::hash is not defined for pair
- provide a custom hash, encode the pair as a single integer, or use set
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: Why is `x in some_set` much faster than `x in some_list` for large collections?
MODEL ANSWER: A list has no way to find x except comparing it with the elements one by one, which takes O(n). A set is a hash table: it computes the hash of x, which leads directly to where x would be stored, so the check takes about constant time on average. Inside a loop over many queries the difference is enormous.
KEY POINTS:
- membership in a list checks elements one by one, O(n)
- a set uses the hash to jump to where the item would be
- set membership is about O(1) on average
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: What happens with `d[key]` when the key is missing from a dict, and what are the ways to avoid the error when counting?
MODEL ANSWER: Reading `d[key]` for a missing key raises a KeyError. When counting, you can use `d.get(key, 0) + 1`, which returns a default instead of raising, use `collections.defaultdict(int)`, which creates missing keys with 0 automatically, or use `collections.Counter`, which counts a whole sequence at once.
KEY POINTS:
- reading a missing key with d[key] raises KeyError
- d.get(key, default) returns a default instead
- defaultdict or Counter handle missing keys automatically when counting
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why can a list not be used as a dictionary key or set element, while a tuple can?
MODEL ANSWER: Dict keys and set elements must be hashable: their hash must stay the same for as long as they are stored, because it decides where they live in the table. A list is mutable, so its contents and hash could change after insertion and it could no longer be found; Python therefore refuses with a TypeError. A tuple of immutable values cannot change, so it is hashable and can be used as a key.
KEY POINTS:
- keys must be hashable, with a hash that never changes
- lists are mutable, so they are unhashable and raise TypeError
- tuples of immutable values are hashable and can be keys
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: What order do you get when you loop over a set, and over a dict, in Python?
MODEL ANSWER: A set has no meaningful order: elements come out in an order determined by their hashes and the table layout, not insertion order or sorted order, and it can look random. A dict, since Python 3.7, keeps insertion order, so keys come out in the order they were first added, which is still not sorted order. When sorted output is required, use `sorted(...)`.
KEY POINTS:
- set iteration order depends on hashing and is not insertion or sorted order
- dicts preserve insertion order (since Python 3.7)
- use sorted() when sorted output is needed
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why must two objects that are equal (`==`) also have the same hash, and what does `{1: "a", 1.0: "b"}` evaluate to?
MODEL ANSWER: A dict lookup first uses the hash to find the slot and then confirms the match with `==`. If two equal objects had different hashes, a lookup with one would go to the wrong slot and fail to find the other, breaking the dictionary. Python guarantees that equal numbers hash the same, and since `1 == 1.0`, they are the same key: the dict becomes `{1: "b"}`, keeping the first key object with the later value.
KEY POINTS:
- lookups use the hash to find the slot, then == to confirm the key
- equal objects with different hashes would not be found
- 1 and 1.0 are equal with equal hashes, so they are the same key
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: Why does deleting keys from a dict inside `for k in d:` raise an error, and how do you remove entries safely?
MODEL ANSWER: Adding or removing keys while iterating changes the table that the iterator is walking through, so Python raises `RuntimeError: dictionary changed size during iteration` rather than skip or repeat keys. To remove entries safely, iterate over a snapshot of the keys, `for k in list(d):`, or build a new dict with a comprehension that keeps only the wanted items.
KEY POINTS:
- changing a dict's size during iteration invalidates the iteration
- Python raises RuntimeError: dictionary changed size during iteration
- iterate over list(d) or build a new dict with a comprehension
=== END ===
