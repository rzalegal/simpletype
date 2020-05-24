from unittest import TestCase
from simpletype.builtins import *
from simpletype.utils.utils import type_filtered_list
from simpletype.utils.Supply import Supply

primitive_predicates = {

    Int: int,
    Float: float,
    String: str,
    Bool: bool

}

linear_collection_predicates = {

    List: list,
    Set: set,

}


class TestPrimitiveBuiltins(TestCase):

    def test_builtin_types(self):
        for predicate, p_type in (
                *primitive_predicates.items(),
                *linear_collection_predicates.items(),
                {Dict : dict}
        ):
            predicate(
                Supply.value_of_type(
                    p_type
                )
            )


class TestTypedCollectionBuiltins(TestCase):

    def test_linears(self):
        for col_predicate, col_type in linear_collection_predicates.items():
            col_predicate(
                Supply.of_size(10).collection(col_type)
            )

    def test_typed_linears_except_tuple(self):
        for col_predicate, col_type in {List: list, Set: set}:
            for elem_predicate, elem_type in primitive_predicates.items():
                col_predicate[elem_predicate](
                    Supply.of_size(10).collection(col_type, elem_type)
                )





