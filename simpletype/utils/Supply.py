from random import randint, random, choice
from string import ascii_letters


class Supply:
    __max_val = 10
    __size = 5

    @staticmethod
    def of_size(size):
        Supply.__size = size
        return Supply

    @staticmethod
    def with_max(max_val):
        Supply.__max_val = max_val
        return Supply

    @staticmethod
    def int_value():
        return randint(0, Supply.__max_val)

    @staticmethod
    def float_value():
        return random() * Supply.__max_val

    @staticmethod
    def char_value():
        return choice(ascii_letters)

    @staticmethod
    def string_value():
        return "".join(
            [
                Supply.char_value() for i in range(Supply.__size)
            ]
        )

    @staticmethod
    def bool_value():
        return choice([True, False])

    __primitive_type_methods = {

        int: int_value.__get__(object),
        float: float_value.__get__(object),
        str: string_value.__get__(object),
        bool: bool_value.__get__(object),
        list: list,
        set: set,
        tuple: tuple,
        dict: dict
    }

    @staticmethod
    def value_of_type(primitive_type):
        return Supply.__primitive_type_methods[primitive_type]()

    @staticmethod
    def collection(col_type, key_primitive_type=int, value_primitive_type=None):
        if col_type == dict:
            return {
                Supply.value_of_type(key_primitive_type):
                    Supply.value_of_type(
                        value_primitive_type
                        if value_primitive_type
                        else key_primitive_type
                    )
                for i in range(Supply.__size)
            }

        return col_type(
            [
                Supply.value_of_type(key_primitive_type)
                for i in range(Supply.__size)
            ]
        )

    @staticmethod
    def nested_collection(col_type, *element_types):
        if len(element_types) == 1:
            return Supply.collection(col_type, element_types[0])

        return col_type(
            [
                Supply.nested_collection(element_types[0], *element_types[1:])
                for i in range(Supply.__size)
            ]
        )

