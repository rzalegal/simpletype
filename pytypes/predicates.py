class Predicate:

    def __init__(self, p, name=""):
        self.p = p
        self.name = ""

    def __and__(self, other):
        return Predicate(lambda x: self.p(x) and other.p(x))

    def __or__(self, other):
        return Predicate(lambda x: self.p(x) or other.p(x))

    def __call__(self, *args):
        for arg in args:
            if not self.p(arg):
                raise TypeError("{} for value '{}'".format(
                    self.exception_text(),
                    arg
                ))

    def inverted(self):
        return Predicate(lambda x: not self.p(x), self.name)

    def for_all(self, args):
        if not self.p(args):
            raise TypeError("{} for value '{}'".format(
                self.exception_text(),
                args
            ))

    def name_reference(self):
        return "expected {}".format(self.name) if self.name else ""

    def exception_text(self):
        return "predicate condition mismatch"

    def with_name(self, name):
        return TypePredicate(
            self.p,
            name
        )


class TypePredicate(Predicate):

    def __init__(self, t, name=""):
        super().__init__(
            lambda x: type(x) is t,
            name
        )
        self.t = t

    def exception_text(self):
        return "Type mismatch" + self.name_reference()


class CollectionTypePredicate(TypePredicate):

    def __init__(self, col_t, elem_type_predicate=lambda x: True):
        super().__init__(
            col_t
        )
        self.elem_type_predicate = elem_type_predicate

    def __call__(self, *cols):

        for col in cols:
            self.for_all(col)
            for el in col:
                self.elem_type_predicate(el)

    def __getitem__(self, elem_type_predicate):
        return CollectionTypePredicate(
            self.t,
            elem_type_predicate
        )


def primitive_type_list(*types):
    return [TypePredicate(t) for t in types]


def collection_type_list(*types):
    return [CollectionTypePredicate(t) for t in types]
