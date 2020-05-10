from simpletype.predicates import *


def takes(*predicates):
    def wrapper(func):
        def wrap(*args):
            try:
                PredicateSequence(predicates)(args)
            except TypeError as e:
                raise TypeError(arg_type_exception(
                    func, e.args[0]
                ))

            return func(*args)

        return wrap

    return wrapper


def returns(predicate):
    def wrapper(func):
        def wrap(*args):
            try:
                ret_val = func(*args)
                predicate(ret_val)
            except TypeError as e:
                raise TypeError(return_type_exception(
                    func
                ))

            return ret_val

        return wrap

    return wrapper

