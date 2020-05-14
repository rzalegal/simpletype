# v0.1-alpha

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
More functionality will be 

## Install
Just run standard pip command to install **simpletype** module:
`pip install simpletype`

## General use

### Two decorators

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
# @returns(List) — return value check is optional — as you wish 
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
# returns(String) 
def join(*args):
    return args[0].join(str(i) for i in args)
```
That will work fine on args despite the separator wasn't explicitly included into signature.

Same principle works good for params list version:
```python
@takes(String, List[Int | String])
# returns(String)
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

### Type system
 
As it was already mentioned before, types are **predicate-based** in _simpletype_. This means you can combine library
types or introduce your own conditionals just passing a predicate-function 
(function that returns boolean value) to Predicate class instance.

Predicate class also has a helper-method _"inverted"_ to apply logical _NOT_ on basic predicate function, which may be
useful sometimes.

```python
# Defining negative integer type
NegativeInt = Int & Predicate(lambda x: x < 0)

# Defining naturals type
Natual = NegativeInt.inverted()

```


