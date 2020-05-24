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

    def __init__(self, f):
        super().__init__(type(lambda : None))
        self.f = f

    def __call__(self, *args):
        super().__call__(self.f)
        return self.f(*args)




class FunctionTaking(FunctionPredicate):

    def __init__(self, f, param_predicates):
        super().__init__(f)
        self.param_predicates = param_predicates

    def __call__(self, *args):
        Tuple[self.param_predicates](
            args
        )
        return super().__call__(*args)


class FunctionReturning(FunctionPredicate):

    def __init__(self, f, return_predicate):
        super().__init__(f)
        self.return_predicate = return_predicate

    def __call__(self, *args):
        return self.return_predicate(
            super().__call__(
                *args
            )
        )


def Takes(*predicates):
    def wrapper(func):
        return FunctionTaking(
            func,
            predicates
        )
    return wrapper


def Returns(predicate):
    def wrapper(func):
        return FunctionReturning(
            func,
            predicate
        )
    return wrapper




