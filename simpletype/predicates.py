from simpletype.exceptions import *


class Predicate:

    def __init__(self, p):
        self.p = p

    def __and__(self, other):
        return Predicate(lambda x: self.p(x) and other.p(x))

    def __or__(self, other):
        return Predicate(lambda x: self.p(x) or other.p(x))

    def __call__(self, arg):
        if not self.p(arg):
            raise ValuePredicateError(arg)
        return arg

    def inverted(self):
        return self.__class__(lambda x: not self.p(x))

    def __iter__(self):
        return [PredicateIterator(self)].__iter__()


class TypePredicate(Predicate):

    def __init__(self, base_type):
        super().__init__(
            lambda x: type(x) is base_type
        )
        self.t = base_type


class CollectionTypePredicate(TypePredicate):

    def __init__(self, col_t, elem_type_predicates=()):
        super().__init__(
            col_t
        )
        self.elem_type_predicates = elem_type_predicates

    def __call__(self, col):
        self.check_col_type(col)
        self.check_col_elements_type(col)
        return col

    def check_col_elements_type(self, col):
        try:
            self.element_check(col)
        except ValueTypeError as e:
            raise ElementTypeError(
                e.value,
                col
            )

    def element_check(self, col):
        for predicate in self.elem_type_predicates:
            for el in col:
                predicate(el)

    def check_col_type(self, col):
        super().__call__(col)

    def check_col_len(self, col):
        required_len = len(self.elem_type_predicates)
        actual_len = len(col)

        if 0 < required_len != actual_len:
            raise CollectionLengthError(col, required_len, actual_len)

    def __getitem__(self, elem_type_predicate):
        return CollectionTypePredicate(
            self.t,
            (elem_type_predicate,)
        )


class TupleTypePredicate(CollectionTypePredicate):

    def __init__(self, elem_type_predicates=()):
        super().__init__(
            tuple,
            elem_type_predicates
        )

    def __getitem__(self, *elem_type_predicates):
        return TupleTypePredicate(
            elem_type_predicates[0]
            if type(elem_type_predicates[0]) is tuple
            else elem_type_predicates
        )

    def __call__(self, col):
        self.check_col_type(col)
        self.check_col_len(col)
        self.check_col_elements_type(col)
        return col

    def element_check(self, col):
        for i in range(len(self.elem_type_predicates)):
            self.elem_type_predicates[i](col[i])


class DictTypePredicate(CollectionTypePredicate):

    def __init__(self, kv_type_predicates=()):
        super().__init__(
            dict,
            kv_type_predicates
        )

    def __call__(self, col):
        return super().__call__(col)

    def element_check(self, col):
        if self.elem_type_predicates:
            for k, v in col.items():
                self.elem_type_predicates[0](k)
                self.elem_type_predicates[1](v)

    def __getitem__(self, *predicates):
        if len(predicates[0]) != 2:
            raise KeyValueCollectionTypingError()
        return DictTypePredicate(
            predicates[0]
        )





class PredicateIterator:

    def __init__(self, predicate):
        self.predicate = predicate


def primitive_type_list(*types):
    return [TypePredicate(t) for t in types]


def collection_type_list(*types):
    return [CollectionTypePredicate(t) for t in types]
