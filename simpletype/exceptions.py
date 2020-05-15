from simpletype.utils import str_limit, type_name_ref


class __ValueTypeError(TypeError):

    def __init__(self, value):
        super().__init__(
            self.error_msg()
        )
        self.value = value

    def error_msg(self):
        return ""

    def value_type_ref(self):
        return type_name_ref(self.value)


class ValuePredicateError(__ValueTypeError):

    def __init__(self, value):
        super().__init__(
            value
        )

    def error_msg(self):
        return "'{}({})'".format(
            self.value_type_ref(),
            str_limit(self.value),
        )


class ElementTypeError(__ValueTypeError):

    def __init__(self, value, col, col_type_predicate):
        super().__init__(
            value
        )
        self.col = col
        self.col_type_predicate = col_type_predicate

    def error_msg(self):
        return "col='{}{}{}', elem='{}{}'".format(
            type_name_ref(self.col),
            "[" + type_name_ref(self.col_type_predicate) + "]" if self.col_type_predicate else "",
            self.col,
            self.value_type_ref(),
            self.value
        )


class IndexedElementTypeError(ElementTypeError):

    def __init__(self, value, col, col_type_predicate, elem_index):
        super().__init__(
            value,
            col,
            col_type_predicate
        )
        self.elem_index = elem_index

    def error_msg(self):
        return super().error_msg() + " index=" + self.elem_index


class CollectionLengthError(__ValueTypeError):

    def __init__(self, col, expected_len, actual_len):
        super().__init__(
            col
        )
        self.expected_len = expected_len
        self.actual_len = actual_len

    def error_msg(self):
        return "'{}{}': expected {} elements, got {} ".format(
            self.value_type_ref(),
            self.value,
            self.expected_len,
            self.actual_len
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
