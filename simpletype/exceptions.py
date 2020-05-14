class SequenceLengthError(Exception):
    pass


def arg_type_exception(func, index=0):
    return TypeError("Argument type mismatch: function '{}', arg_{}".format(
        func.__name__,
        index + 1
    ))


def return_type_exception(func):
    return TypeError("Return value type mismatch: function '{}'".format(
        func.__name__
    ))


def collection_elem_type_exception(func, index=0, base_text=""):
    return TypeError("{} within collection. (Function='{}', elem_index={})".format(
        str(base_text),
        func.__name__,
        index
    ))


class ValueTypeError(TypeError):

    def __init__(self, value):
        super().__init__("For value={}".format(
            value
        ))


class ArgumentTypeError(TypeError):

    def __init__(self, func, index, value):
        super().__init__("Function '{}', arg_{}, value={}".format(
            func.__name__,
            index + 1,
            value
        ))


class ReturnValueError(TypeError):

    def __init__(self, func, value):
        super().__init__("Function '{}', value={}".format(
            func.__name__,
            value
        ))