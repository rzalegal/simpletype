class ValueTypeError(TypeError):

    def __init__(self, value):
        super().__init__("Predicate mismatch for value='{}', base_type={}".format(
            value,
            type(value)
        ))
        self.value = value


class ReturnTypeError(ValueTypeError):

    def __init__(self, func, value):
        super().__init__(
            "function '{}': value={}, base_type={}".format(
                func.__name__,
                value,
                type(value)
            )
        )


class ArgumentTypeError(ValueTypeError):

    def __init__(self, func, index, value):
        super().__init__(
            "function '{}', arg_{}: value='{}', base_type={}".format(
                func.__name__,
                index + 1,
                value,
                type(value)
            )
        )



