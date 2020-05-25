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

Tuple = TupleTypePredicate()

Dict = DictTypePredicate()

Collection = List | Set | Tuple

Singleton = Collection & Len(1)

# Function types


class FunctionPredicate(TypePredicate):

    def __init__(self, ret_p=Any, *params_p):
        super().__init__(type(
            lambda: None
        ))

        self.ret_p = ret_p
        self.params_p = Tuple[params_p]

    def __call__(self, f):
        def wrapper(*args):
            return self.ret_p(
                f(
                    *self.params_p(
                        args
                    )
                )
            )
        return wrapper


sum = FunctionPredicate(Int, Int, Int)(lambda x, y: x + y)

print(sum(3,4))

