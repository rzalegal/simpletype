# Simpletype

## One more type checker?

Existing solutions for type checking in python projects sometimes may seem 
too complicated for just-in-time use.

### Main reasons for that:

+ Method signature verbosity
+ A need to modify method contents
+ Huge amount of built-ins

Usually type constraints are placed within method or function signature:
```python
def send_funds(sender_addr: string, reciever_addr: string, float: amount) -> List:
    ...
```

This code string seems **verbose** and nearly breaks PEP on maximum code line length.
We decided to literally move that whole type checking upside:

```python
@takes(String, String, Float)
@returns(List)
def send_funds(sender_addr, receiver_addr, amount):
    ...
```

Stretching a piece of code not horizontally but vertically and removing typing **off method signature**
clarifies the code in much more _pythonic_ way.
The idea of splitting _argument_ and _return_ parts into separate annotations follows the same target.

When using third-party library one always agrees somebody else's personal naming conventions,
same to the new "types" one needs to remember.

Our types a predicate-based:

```python
# e.g. some primitives

Number = Int | Float

Even = Int & Predicate(lambda x: x % 2 == 0)

Odd = Even.inverted()
```

So you easily can perform your own ones:
```python
Unit = Predicate(lambda x: len(str(x)) == 1)

Digit = Int & Unit

Char = String & Unit
```

By the way, you may also substitute too long but often used type definitions by 
your own to reduce code verbosity even more:

```python
# before
@takes(List[List[List[Int]]])
@returns(List[List[List[Int]]])
def wrap_coordinates(coord_lst):
    ...
```
```python
# after
IntArray3 = List[List[List[Int]]]

@takes(IntArray3)
@returns(IntArray3)
def wrap_coordinates(coord_lst):
    ...

```

## Install
Just run standard pip command to install **simpletype** module:
`pip install simpletype`

## General use

### Decorating functions

As you may have already seen, checking the types requires using just one 
of two decorators 
```python
@takes(...)
@returns(...)
```
or both of them.

Any of built-in types can be passed into the **takes** annotation in any
quantity, any depth of nesting with vararg support:
```python
@takes(Function, *Int)
def map_all_ints(f, *args):
    return [f(i) for i in args]
```
When providing your functions with type constraints you can use _simpletype builtins_,
define your own ones or just use predicate-style typing right-in-place.

For example, we have to implement **join** function to concatenate vararg input whether it may consist of strings or 
integers with separator defined as first string argument. You can define something like `StringInt` as your own type, 
but the better one is to use predicative manner:
```python
@takes(String, *(Int | String)) 
def join(*args):
    return args[0].join(str(i) for i in args)
```
That will work fine on args despite the separator wasn't explicitly included into signature.

Same principle works good for params list version:
```python
@takes(String, List[Int | String])
def join(sep, list_to_join):
    return sep.join(str(i) for i in list_to_join)
```
It does literally say "Me, join function, accept string firstly, and list of strings and maybe integers then."

The **returns** decorator on the other hand is able to handle only a single value, 
because functions in Python themselves can return only a single value.

So it supports the same features to **takes** but in quantity of one and except varargs.

```python
# takes(List[Any])
@returns(List[String])
def convert_to_strings(some_list):
    return [str(i) for i in some_list]
```
Special return case is when function does not return anything. You may check this
by declaring the one returning _Nothing_ built-in type, but there's special **void** decorator
that will make it clearer:
```python
# returning Nothing
@takes(*Number)
@returns(Nothing)
def print_numbers(*nums):
    print(nums)
```

```python
# Declaring as void
@takes(*Number)
@void
def print_numbers(*nums):
    print(nums)
```

### Variable type checking

Library allows to check not only the function parameters and return value, but variable type.

```python
a = Int(5) # a = 5

b = List[Number]([1, 2, 3.0]) # b = [1, 2, 3.0]

c = String(4.0) # an exception will be raised
``` 

### What exceptions are actually raised

Because of Python not being a compiled programming language we don`t have _compile time errors_, 
having only _runtime_ ones.

When typed function is being called and some parameter or (and) return value does not match the types declared,
a TypeError-base exception will be raised.

Depending on what exactly went wrong, this is to be either _ArgumentTypeError_ or _ReturnTypeError_ or _ValueTypeError_, carrying some
information about typed function (method) and wrong type argument or value:

#### ArgumentTypeError
+ Invoked function (method) name
+ Argument index
+ Argument value
+ Argument base type

Exception is raised on function argument type mismatch:

```python
@takes(*Number)
def build_reversed_int(*args):
    s = ''
    for i in args:
        s += str(i)
    return s[::-1]

build_reversed_int(1, 2, 3) # result: 321
build_reversed_int(1, 2, 's') # ArgumentTypeException
```

Normally, an accident string argument passing wouldn't have much effect on code execution — explicit casting to string 
works properly both on integers and strings — so the fact of returning an absolutely incorrect result would 
remain unnoticed.

However, being marked as type-safe function that takes only numbers it would raise error immediately:

    simpletype.exceptions.ArgumentTypeError: function 'build_reversed_int', arg_3: value='s', base_type=<class 'str'>


#### ReturnTypeError
+ Invoked function (method) name
+ Argument value
+ Argument base type

Exception is raised on function return value type mismatch:

```python

@returns(Set[String])
def str_collection(*args):
    return [str(i) for i in args]

@returns(Int)
def divide(a, b):
    return a / b 
```

Both of these functions will cause a ReturnTypeError, although the first one is to show up the function was built
incorrectly, but the second helps to find an incorrectly predicted return type.  

#### ValueTypeError
+ Value
+ Value base type

Basic exception type is raised on value type mismatch and is a cause for other two exceptions. 

It is raised alone only when variable is declared:

```python
a = Float(1)
```
    simpletype.exceptions.ValueTypeError: Predicate mismatch for value='1', base_type=<class 'int'>

## Type system

### Primitive types

1) **Int** — integer value in common sense: ```1, 20, 300```
2) **Float** — float value in common sense: ```3.0, 4.2, 5.9```
3) **String** — string value in common sense: ```'hello', 'world'```
4) **Bool** — boolean value in common sense: ```true, false```
5) **Number** — either an integer or float value: ```4, 1.0```
6) **Even** — an even integer value: ```2, -4, 6```
7) **Odd** — an odd integer value: ```3, 9, -17```
8) **Unit** — a unit-length value: ```3, 's', 'B', 1```
9) **Char** — a unit-length string value: ```'a', 'b', 'c', ... 'z'```
10) **Digit** — a unit-length integer value: ```0, 1, 2, 3, ... 9``` 
11) **Any** — represents a value of any type
12) **Nothing** — represents python builtin _None_ value
 
As it was already mentioned before, types are **predicate-based** in _simpletype_. This means you can combine library
types or introduce your own conditionals just passing a predicate-function 
(function that returns boolean value) to Predicate class instance.

Predicate class also has a helper-method _"inverted"_ to apply logical _NOT_ on basic predicate function, which may be
useful sometimes.

```python
# Defining negative integer type
NegativeInt = Int & Predicate(lambda x: x < 0)

# Defining naturals type
Natural = NegativeInt.inverted()

# Defining prime number type
def is_prime(n):
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True and n != 1

Prime = Int & Predicate(is_prime) 

```

### Collection types

1) **List**, **List[T]** — a list in common sense & list of elements with type T: ```[1, 2, 's']```
2) **Tuple**, **Tuple[T1, T2, ..., Tn]** — a tuple in common sense & tuple with typed values: ```(10, 20, 'ff')```
3) **Set**, **Set[T]** — a set in common sense & set of elements with type T: ```{1, 2, 's'}```
4) **Collection**, **Collection[T]** — list, tuple or set in common sense or typed collection

Collection types support their elements predicative-typing on any depth level:

```python

@takes(List[List[Int | Float]])
@returns(List | Nothing)
def longest_int_sublist(lst):
    max_len = -1
    sublist = None
    for l in lst:
        length = len(l)
        if length > max_len:
            max_len = length
            sublist = l
    return sublist 

longest_int_sublist([[1, 2.0, 3], [], [1, 3]]) # result: [1, 2.0, 3]
longest_int_sublist([[1, 2, 3], [], [1, '3']]) # ArgumentTypeError
```

This typed function accepts only a list of lists of integers or floats, and returns a list or None.
