from simpletype.utils import str_limit, type_name_ref


class ValueTypeError(TypeError):

    def __init__(self, value, err_msg):
        super().__init__(
            err_msg
        )
        self.value = value


class ValuePredicateError(ValueTypeError):

    def __init__(self, value):
        super().__init__(
            value,
            "{}<{}>".format(
                str_limit(value),
                type_name_ref(value),
            )
        )


class ElementTypeError(ValueTypeError):

    def __init__(self, value, col):
        super().__init__(
            value,
            "col: {}{}; elem: {} <{}>".format(
                type_name_ref(col),
                col,
                value,
                type_name_ref(value)
            )
        )
        self.col = col


class IndexedElementTypeError(ElementTypeError):

    def __init__(self, value, col, predicates, elem_index):
        super().__init__(
            value,
            super().args[0] + " index=" + self.elem_index
        )
        self.elem_index = elem_index


class CollectionLengthError(ValueTypeError):

    def __init__(self, col, expected_len, actual_len):
        super().__init__(
            col,
            "{}{}: expected {} elements, got {} ".format(
                type_name_ref(col),
                col,
                expected_len,
                actual_len
            )
        )
        self.expected_len = expected_len
        self.actual_len = actual_len


class KeyValueCollectionTypingError(ValueTypeError):

    def __init__(self):
        super().__init__(
            [],
            "Dict[K, V]{} — Dictionary accepts either two type specifiers or none"
        )


class ReturnTypeError(ValuePredicateError):

    def __init__(self, func, value):
        super().__init__(
            "function '{}': {}{}".format(
                func.__name__,
                type(value).__class__.__name__,
                value
            )
        )


class ArgumentTypeError(ValuePredicateError):

    def __init__(self, func, index, value):
        super().__init__(
            "function '{}', arg_{}: value='{}', base_type={}".format(
                func.__name__,
                index + 1,
                value,
                type(value)
            )
        )
