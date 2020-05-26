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

    def __init__(self, ret_p=Any, *params_p):
        super().__init__(type(
            lambda: None
        ))
        # print(f'({",".join(str(i.t) for i in params_p)}) -> ({ret_p})')
        self.ret_p = ret_p
        self.params_p = params_p

    def __call__(self, f):
        super().__call__(f)

        def wrapper(*args):
            return self.ret_p(
                f(
                    *Tuple[self.params_p](
                        args
                    )
                )
            )

        return wrapper

    def taking(self, *predicates):
        return FunctionPredicate(
            self.ret_p,
            *predicates
        )

    def returning(self, predicate):
        return FunctionPredicate(
            predicate,
            *self.params_p
        )

    def __getitem__(self, predicates):
        return FunctionPredicate(
            predicates[-1],
            *predicates[:-1]
        )


Function = FunctionPredicate()


def takes(*predicates):
    def wrap(func):
        return Function.taking(*predicates)(
            func
        ) if type(func) is functional else Function.taking(
            *predicates
        ).returning(
            func.ret_p
        )
    return wrap


def returns(predicate):
    def wrap(func):
        return Function.returning(
            predicate
        )(func)

    return wrap


@takes(Int, Int, Int)
@returns(Int)
def sum(a, b):
    return a + b

print(sum(1, 1))




