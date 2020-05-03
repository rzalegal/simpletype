from pytypes.types import *
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
