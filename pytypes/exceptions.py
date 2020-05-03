def arg_type_exception(func, index, base_text=""):
    return TypeError("{}Function '{}', arg_{}".format(
        str(base_text) + ". ",
        func.__name__,
        index + 1
    ))
