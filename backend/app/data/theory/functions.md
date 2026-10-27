# Theory bank: functions

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: A function `void add_one(int x) { x = x + 1; }` is called as `add_one(n);`. Why is `n` unchanged afterwards?
MODEL ANSWER: C passes arguments by value: the value of `n` is copied into the parameter `x`, which is a separate local variable of the function. The function changes only that copy, and the copy disappears when the function returns, so `n` keeps its old value.
KEY POINTS:
- C passes arguments by value, copying them into the parameters
- the parameter is a separate local variable
- changes to the copy are lost when the function returns
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: easy
QUESTION: Why does a C program need a function prototype when `main` calls a function that is defined further down the file?
MODEL ANSWER: The compiler reads the file from top to bottom and must know a function's return type and parameter types at the point where it is called, so that it can check the call and convert the arguments. A prototype such as `int square(int x);` declares this before the call. Without it, modern C reports an error (older compilers assumed an implicit `int` function, which led to wrong conversions).
KEY POINTS:
- the compiler processes the file top to bottom
- it needs the return and parameter types before the call
- a prototype declares the signature ahead of the definition
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: How is passing a pointer to a variable as a parameter different from passing the variable's value directly, and why would you choose the pointer?
MODEL ANSWER: Passing the value copies it, so the function works on its own copy. Passing a pointer copies only the variable's address, so the function can reach the original variable in the caller's memory and change it through `*p`. This is how a function can modify the caller's variables or hand back several results (as scanf does). It also avoids copying large data such as a big struct, because only the address is copied.
KEY POINTS:
- the function receives the variable's address instead of a copy of its value
- it can modify the caller's variable directly by dereferencing the pointer
- it lets a function return several results through output parameters
- only the address is copied, which avoids copying large data
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: medium
QUESTION: Why is it wrong for a function to return the address of one of its local variables?
MODEL ANSWER: Local variables live in the function's stack frame, which is released when the function returns. The returned pointer then points to memory that no longer belongs to that variable and may be reused by the next call. Using it is undefined behaviour. Return the value itself, or use memory that outlives the call: a buffer provided by the caller, a static variable, or malloc.
KEY POINTS:
- local variables live in the stack frame that is destroyed on return
- the returned pointer dangles, pointing to memory that may be reused
- using it is undefined behaviour; return a value or use caller-provided, static, or heap memory
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: Why can a function `int total(int a[])` not find out how many elements the caller's array has, and what does that imply?
MODEL ANSWER: An array argument decays to a pointer to its first element, so the parameter `int a[]` is really `int *a`. Inside the function `sizeof a` is the size of a pointer, not of the array, and there is no stored length. The caller must pass the number of elements as a separate parameter. Because only the address is passed, changes the function makes to the elements are visible to the caller.
KEY POINTS:
- an array argument decays to a pointer to its first element
- sizeof inside the function gives the pointer size, not the array size
- the length must be passed as a separate parameter
- the function works on the caller's array, so changes are visible
=== END ===

=== THEORY ===
LANGUAGE: c
DIFFICULTY: hard
QUESTION: What is the difference between a global variable and a `static` local variable, and why are parameters and return values usually preferred over both?
MODEL ANSWER: A global variable is visible to, and can be changed by, every function in the file. A static local variable also lives for the whole program and keeps its value between calls, but it can only be used inside its own function. Both hide data flow: a function's result can depend on state that is not visible in its call. Passing data in through parameters and out through return values makes each function's inputs and outputs explicit and easier to test.
KEY POINTS:
- a global is visible to and modifiable by every function
- a static local keeps its value between calls but is visible only in its function
- parameters and return values make data flow explicit and functions easier to test
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: What is the difference between `void f(int x)` and `void f(int &x)` when `f` changes `x`?
MODEL ANSWER: In `f(int x)` the argument is copied into the parameter, so changing `x` affects only the copy and the caller's variable is unchanged. In `f(int &x)` the parameter is a reference, another name for the caller's variable, so changes are visible to the caller. A reference parameter also avoids making a copy.
KEY POINTS:
- passing by value copies the argument, so changes stay local
- a reference parameter is an alias for the caller's variable
- changes through the reference are visible to the caller
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: easy
QUESTION: Why are large inputs such as a `vector<int>` or a `string` often passed as `const vector<int> &v`?
MODEL ANSWER: Passing by value copies the entire container, which costs time and memory proportional to its size on every call. Passing by reference avoids the copy. Adding `const` promises, and makes the compiler enforce, that the function will not modify the caller's data. A const reference can also bind to temporary values.
KEY POINTS:
- passing by value copies the whole container
- a reference avoids the copy
- const prevents the function from modifying the argument
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Both pointers and references let a function modify the caller's variable. How do they differ?
MODEL ANSWER: A reference must be bound to an existing object when it is created, cannot be null, and cannot be changed to refer to something else; it is used with ordinary syntax. A pointer holds an address, can be null, can be pointed somewhere else, and needs explicit `&` at the call and `*` to access the value. References are therefore simpler and safer for parameters, while pointers are needed when "no object" is a valid option.
KEY POINTS:
- a reference must be bound at creation and cannot be null or reseated
- a pointer can be null and can be changed to point elsewhere
- pointers need explicit & and * while references use normal syntax
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: medium
QUESTION: Why is `int& biggest() { int best = 0; /* ... */ return best; }` a bug?
MODEL ANSWER: The function returns a reference to `best`, a local variable that is destroyed when the function returns. The caller receives a dangling reference to storage that no longer holds a valid object, and using it is undefined behaviour. Return by value instead; this is cheap, since compilers avoid the copy where possible (return value optimisation or move).
KEY POINTS:
- the local variable is destroyed when the function returns
- the returned reference dangles
- using it is undefined behaviour, so return by value instead
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: How does the compiler choose between overloaded functions, and why can two functions not differ only in their return type?
MODEL ANSWER: The choice is made at compile time from the number and types of the arguments at the call: the compiler picks the overload whose parameters match best, and reports an error if the call is ambiguous. The return type is not part of this matching, because a call like `f(3);` gives no information about which return type is wanted. So two functions with the same parameters and different return types would be indistinguishable and are not allowed.
KEY POINTS:
- overloads are chosen at compile time from the number and types of the arguments
- the return type is not used in overload resolution
- ambiguous calls are compile errors
=== END ===

=== THEORY ===
LANGUAGE: cpp
DIFFICULTY: hard
QUESTION: A recursive function takes `vector<int> v` by value and is called about n times on a vector of n elements. Why can that make the solution too slow?
MODEL ANSWER: Each call copies all n elements of the vector into the new parameter. With about n calls, the total copying is about n × n element copies, even if the algorithm itself only needs linear work, and memory use grows too. Passing the vector by reference (`const vector<int> &v`, or a non-const reference if it must change) shares one vector across all the calls.
KEY POINTS:
- passing by value copies the entire vector on every call
- n calls each copying n elements gives about n squared work
- pass by (const) reference so all calls share one vector
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: What is the difference between a function that `return`s a value and one that `print`s it?
MODEL ANSWER: `return` hands the value back to the caller, which can store it, use it in a calculation, or pass it on. `print` only shows text on the screen; the caller gets nothing back. A function without a `return` statement returns `None`, so `x = f()` would store `None`.
KEY POINTS:
- return gives the value back to the caller to use
- print only displays text and does not give a value back
- a function with no return returns None
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: easy
QUESTION: A function assigns `total = 0` and fills it in. Why is `total` not available after the function returns?
MODEL ANSWER: Names assigned inside a function are local to that call: they are created when the function runs and disappear when it returns. They are not visible outside it, and a variable with the same name outside the function is a different variable. To use the result, return it and assign it at the call site.
KEY POINTS:
- names assigned inside a function are local
- local variables disappear when the function returns
- a same-named variable outside is a different variable, so return the value
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why does a function that does `items.append(1)` change the caller's list, while a function that does `n = n + 1` does not change the caller's number?
MODEL ANSWER: Python passes a reference to the same object, sometimes called call by sharing. A list is mutable, so `append` changes that one shared object and the caller sees the change. An int is immutable, so `n = n + 1` creates a new int object and rebinds only the local name `n`, leaving the caller's object untouched. Rebinding a list parameter with `items = [...]` would not affect the caller either.
KEY POINTS:
- the parameter refers to the same object as the caller's argument
- mutating a mutable object like a list is visible to the caller
- assigning a new value to the parameter only rebinds the local name; ints are immutable
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: medium
QUESTION: Why does `def add(x, bucket=[]): bucket.append(x); return bucket` return a growing list across separate calls?
MODEL ANSWER: Default values are evaluated once, when the `def` statement runs, not on each call. Every call that uses the default therefore shares the same list object, so items appended in one call are still there in the next. The usual fix is `bucket=None` and creating a new list inside the function when it is None.
KEY POINTS:
- default argument values are evaluated once, at definition time
- all calls share the same default list object
- use None as the default and create the list inside the function
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: With `count = 0` at the top of a file, why does a function containing `count += 1` raise UnboundLocalError?
MODEL ANSWER: If a name is assigned anywhere inside a function, Python treats it as local for the whole function. `count += 1` both reads and assigns `count`, so it refers to a local `count` that has not been given a value yet, which raises UnboundLocalError. Declaring `global count` changes that, but it is cleaner to pass the value in and return the new value.
KEY POINTS:
- any assignment to a name inside a function makes it local throughout the function
- count += 1 reads the local before it has a value, raising UnboundLocalError
- use a global declaration, or better, pass and return the value
=== END ===

=== THEORY ===
LANGUAGE: python
DIFFICULTY: hard
QUESTION: In `sorted(words, key=len)`, why is `len` written without brackets, and what does this show about functions in Python?
MODEL ANSWER: Functions are objects in Python: they can be stored in variables and passed to other functions like any other value. `key=len` passes the function itself, and `sorted` calls it on each element to get the value to compare. Writing `len()` would call it immediately (and fail, since it needs an argument) instead of passing it.
KEY POINTS:
- functions are first-class objects that can be passed as arguments
- sorted calls the key function on each element
- writing len() would call the function instead of passing it
=== END ===
