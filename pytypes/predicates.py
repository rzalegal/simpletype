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

    def name_reference(self):
        return "expected {}".format(self.name) if self.name else ""

    def exception_text(self):
        return "predicate condition mismatch"

    def with_name(self, name):
        return Predicate(
            self.p,
            name
        )


class TypePredicate(Predicate):

    def __init__(self, t):
        super().__init__(
            lambda x: type(x) is t
        )

    def exception_text(self):
        return "Type mismatch" + self.name_reference()


def is_prime(n):
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True and n != 1


def type_predicates(*types):
    return [TypePredicate(t) for t in types]



