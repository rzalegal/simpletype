class ArgumentTypeError(TypeError):

    def __init__(self, func, index):
        super().__init__(
            "function '{}', arg_{}".format(
                func.__name__,
                index + 1
            )
        )


class ReturnTypeError(TypeError):

    def __init__(self, func):
        super().__init__(
            "function '{}'".format(
                func.__name__
            )
        )


class ValueTypeError(TypeError):

    def __init__(self, value):
        super().__init__("Predicate mismatch for value='{}', base_type={}".format(
            value,
            type(value)
        ))

