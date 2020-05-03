from pytypes.predicates import *
from pytypes.exceptions import *


def takes(*predicates):
    def wrapper(func):
        def wrap(*args):
            for i in range(len(args)):

                try:
                    predicates[i](args[i])
                except TypeError as e:
                    raise arg_type_exception(func, i, str(e))

            return func(*args)

        return wrap

    return wrapper


def returns(predicate):
    def wrapper(func):
        def wrap(*args):

            ret_val = func(*args)

            try:
                predicate(ret_val)
            except TypeError as e:
                raise return_type_exception(func, str(e))

            return ret_val
        return wrap
    return wrapper

