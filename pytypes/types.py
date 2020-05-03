from pytypes.constraints import *

# Basic types

Int, Float, String, Bool = type_predicates(int, float, str, bool)

Number = (Int | Float)

Unit = Predicate(lambda x: len(str(x)) == 1)

Digit = Int & Unit

Char = String & Unit

Nothing = Predicate(lambda x: x is None)

Any = Predicate(lambda x: True)

void = returns(Nothing)

# Custom types


def is_prime(n):
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True and n != 1


Prime = Int & Predicate(is_prime)






