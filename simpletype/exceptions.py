from types import TracebackType
from typing import Optional

from simpletype.utils import str_limit, type_name_ref


class ValueTypeError(TypeError):

    def __init__(self, value, err_msg):
        super().__init__(
            err_msg
        )
        self.value = value

    def value_type_ref(self):
        return type_name_ref(self.value)


class ValuePredicateError(ValueTypeError):

    def __init__(self, value):
        super().__init__(
            value,
            "'{}({})'".format(
                self.value_type_ref(),
                str_limit(self.value),
            )
        )


class ElementTypeError(ValueTypeError):

    def __init__(self, value, col, col_type_predicate):
        super().__init__(
            value,
            "col='{}{}{}', elem='{}{}'".format(
                type_name_ref(self.col),
                "[" + type_name_ref(self.col_type_predicate) + "]" if self.col_type_predicate else "",
                self.col,
                self.value_type_ref(),
                self.value
            )
        )
        self.col = col
        self.col_type_predicate = col_type_predicate


class IndexedElementTypeError(ElementTypeError):

    def __init__(self, value, col, col_type_predicate, elem_index):
        super().__init__(
            value,
            super().args[0] + " index=" + self.elem_index
        )
        self.elem_index = elem_index


class CollectionLengthError(ValueTypeError):

    def __init__(self, col, expected_len, actual_len):
        super().__init__(
            col,
            "'{}{}': expected {} elements, got {} ".format(
                self.value_type_ref(),
                self.value,
                self.expected_len,
                self.actual_len
            )
        )
        self.expected_len = expected_len
        self.actual_len = actual_len


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
