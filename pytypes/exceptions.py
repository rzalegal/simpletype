def arg_type_exception(func, index=0, base_text=""):
    return TypeError("{}Function '{}', arg_{}".format(
        str(base_text) + ". ",
        func.__name__,
        index + 1
    ))


def return_type_exception(func, base_text=""):
    return TypeError("{} (Function '{}' return value)".format(
        str(base_text),
        func.__name__
    ))
