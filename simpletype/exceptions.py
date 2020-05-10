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