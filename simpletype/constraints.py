from simpletype.predicates import *


def takes(*predicates):
    def wrapper(func):
        def wrap(*args):
            try:
                exceptional_arg_index = 0

                for i in range(len(args)):

                    if predicates[i].__class__.__subclasscheck__(PredicateIterator):

                        for j in range(i, len(args)):
                            exceptional_arg_index = j
                            predicates[i].predicate(args[j])

                        return func(*args)

                    exceptional_arg_index = i
                    predicates[i](args[i])

            except ValuePredicateError as e:
                raise ArgumentTypeError(
                    func,
                    exceptional_arg_index,
                    e.value
                )

            return func(*args)

        return wrap

    return wrapper


def returns(predicate):
    def wrapper(func):
        def wrap(*args):
            try:
                ret_val = func(*args)
                predicate(ret_val)
            except ReturnTypeError as e:
                raise ReturnTypeError(
                    func,
                    e.value
                )

            return ret_val

        return wrap

    return wrapper
