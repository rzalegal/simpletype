from unittest import TestCase
from simpletype.builtins import *
from simpletype.utils.utils import type_filtered_list


class TestPrimitiveBuiltins(TestCase):

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

    # testing not typed library-collections matching python ones
    def test_collections(self):
        for col_t, predicate in TestCollectionBuiltins.type_dict.items():
            predicate(
                col_t(TestPrimitiveBuiltins.values)
            )

    # testing typed iterable library-collections (List & Set) on each primitive
    def test_typed_linears(self):
        for primitive, predicate in TestPrimitiveBuiltins.type_dict.items():
            for col_type in (list, set):
                TestCollectionBuiltins.type_dict[col_type][predicate](col_type(
                    type_filtered_list(
                        TestPrimitiveBuiltins.values,
                        primitive
                    )
                ))

    # testing a typed tuple that contains a single element on each primitive
    def test_single_elem_tuple(self):
        for primitive, predicate in TestPrimitiveBuiltins.type_dict.items():
            Tuple[predicate](
                tuple(
                    [
                        type_filtered_list(
                            TestPrimitiveBuiltins.values,
                            primitive
                        )[0]
                    ]
                )
            )

    # testing a typed tuple of two elements on all pairs of primitives
    def test_two_elems_tuple(self):
        for primitive1, predicate1 in TestPrimitiveBuiltins.type_dict.items():
            for primitive2, predicate2 in TestPrimitiveBuiltins.type_dict.items():
                Tuple[predicate1, predicate2](
                    tuple(
                        [
                            type_filtered_list(
                                TestPrimitiveBuiltins.values,
                                primitive1
                            )[0],
                            type_filtered_list(
                                TestPrimitiveBuiltins.values,
                                primitive2
                            )[0]
                        ]
                    )
                )
