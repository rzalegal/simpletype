from simpletype.constraints import *

# Basic types

Int, Float, String, Bool = primitive_type_list(int, float, str, bool)

Number = Int | Float

Even = Int & Predicate(lambda x: x % 2 == 0)

Odd = Even.inverted()

Len = lambda n: Predicate(lambda x: len(x) == n)

LenMax = lambda n: Predicate(lambda x: len(x) <= n)

LenMin = lambda n: Predicate(lambda x: len(x) >= n)

LenBound = lambda a, b: LenMin(a) & LenMax(b)

Unit = Predicate(lambda x: len(str(x)) == 1)

Digit = Int & Unit

Char = String & Unit

Nothing = Predicate(lambda x: x is None)

Any = Predicate(lambda x: True)

void = returns(Nothing)


# Collection types

List, Set = collection_type_list(list, set)

Collection = List | Set

Singleton = Collection & Len(1)

# Function types

Function = TypePredicate(type(lambda x: x))

Tuple = TupleTypePredicate()


@takes(*Number)
def build_reversed_int(*args):
    s = ''
    for i in args:
        s += str(i)
    return s[::-1]


build_reversed_int(1, 2, 's')
