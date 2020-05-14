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
            raise ValueTypeError(arg)
        return arg

    def inverted(self):
        return Predicate(lambda x: not self.p(x))

    def __iter__(self):
        return [PredicateIterator(self)].__iter__()


class TypePredicate(Predicate):

    def __init__(self, base_type):
        super().__init__(
            lambda x: type(x) is base_type
        )
        self.t = base_type


class CollectionTypePredicate(TypePredicate):

    def __init__(self, col_t, *elem_type_predicates):
        super().__init__(
            col_t
        )
        self.elem_type_predicates = elem_type_predicates

    def __call__(self, col):
        super().__call__(col)
        for el, predicate in zip(col, self.elem_type_predicates):
            predicate(el)

    def __getitem__(self, elem_type_predicate):
        return CollectionTypePredicate(
            self.t,
            elem_type_predicate
        )


class TupleTypePredicate(CollectionTypePredicate):

    def __init__(self, *elem_type_predicates):
        super().__init__(
            tuple,
            *elem_type_predicates
        )

    def __getitem__(self, *elem_type_predicates):
        return TupleTypePredicate(
            *elem_type_predicates[0]
        )


class PredicateIterator:

    def __init__(self, predicate):
        self.predicate = predicate


def primitive_type_list(*types):
    return [TypePredicate(t) for t in types]


def collection_type_list(*types):
    return [CollectionTypePredicate(t) for t in types]
