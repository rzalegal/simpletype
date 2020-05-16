from unittest import TestCase
from simpletype.builtins import *
from simpletype.utils import type_filtered_list, predicate_filtered_list


class TestPrimitiveBuiltins(TestCase):
    type_dict = {
        int: Int,
        float: Float,
        str: String,
        bool: Bool
    }

    values = [1, 2, -3, -1000, -8888,
              2.0, 8.1235, 13424634.820934,
              's', 'hello', "sdfsdfsdfsdf",
              True, False
              ]

    def test_primitives(self):
        for primitive, predicate in TestPrimitiveBuiltins.type_dict.items():
            for elem in type_filtered_list(TestPrimitiveBuiltins.values, primitive):
                predicate(elem)


class TestCollectionBuiltins(TestCase):
    type_dict = {
        list: List,
        tuple: Tuple,
        set: Set
    }

    def test_collections(self):
        for col_t, predicate in TestCollectionBuiltins.type_dict.items():
            predicate(
                col_t(TestPrimitiveBuiltins.values)
            )

    def test_typed_iterables(self):
        for primitive, predicate in TestPrimitiveBuiltins.type_dict.items():
            for col_type in (list, set):
                TestCollectionBuiltins.type_dict[col_type][predicate](col_type(
                    type_filtered_list(
                        TestPrimitiveBuiltins.values,
                        primitive
                    )
                ))
