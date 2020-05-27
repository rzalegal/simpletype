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

functional = type(lambda: 1)


class FunctionPredicate(TypePredicate):

    def __init__(self, f, ret_p, params_p):
        super().__init__(functional)
        self.f = f
        self.ret_p = ret_p
        self.params_p = params_p

    def __call__(self, *args):
        return self.ret_p(
            self.f(
                *Tuple[self.params_p](
                    args
                )
            )
        )


def takes(*predicates):
    def wrapper(func):

        if type(func) is FunctionPredicate:
            return FunctionPredicate(
                func.f,
                func.ret_p,
                predicates
            )

        return FunctionPredicate(
            func,
            Any,
            predicates
        )

    return wrapper


def returns(predicate):
    def wrapper(func):

        if type(func) is FunctionPredicate:
            return FunctionPredicate(
                func.f,
                predicate,
                func.params_p,
            )

        return FunctionPredicate(
            func,
            predicate,
            ()
        )

    return wrapper


@returns(Int)
@takes(Int, Int)
def sum(a, b):
    return a + b


