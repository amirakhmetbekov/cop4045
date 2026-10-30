# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 17:05:12 2026

@author: Amir
"""

from numbers import Real
from testif import testif


class NVector:
    """Represent an N-dimensional vector of real numbers."""

    def __init__(self, *args: object) -> None:
        """
        Create an NVector.

        If one argument is supplied, it must be a sequence of real numbers.
        A new list is created from that sequence.

        If two or more arguments are supplied, the arguments themselves
        become the elements of the vector.

        Raises:
            TypeError: If no arguments are supplied, if a single argument
            is not a sequence, or if an element is not a real number.
        """
        if len(args) == 0:
            raise TypeError("NVector requires at least one argument")

        if len(args) == 1:
            # This intentionally creates a NEW list.
            # If args[0] is a scalar, list() raises TypeError.
            self._elements = list(args[0])
        else:
            self._elements = list(args)

        for value in self._elements:
            if not isinstance(value, Real):
                raise TypeError("All vector elements must be real numbers")

    def __len__(self) -> int:
        """Return the number of elements in this vector."""
        return len(self._elements)

    def __getitem__(self, index: int) -> Real:
        """
        Return the element at index.

        Negative indexes work the same way as normal Python lists.

        Raises:
            IndexError: If index is outside the vector.
        """
        return self._elements[index]

    def __setitem__(self, index: int, value: Real) -> None:
        """
        Assign value to the element at index.

        Negative indexes work the same way as normal Python lists.

        Raises:
            IndexError: If index is outside the vector.
            TypeError: If value is not a real number.
        """
        if not isinstance(value, Real):
            raise TypeError("Vector elements must be real numbers")

        self._elements[index] = value

    def __str__(self) -> str:
        """Return a readable string representation of this NVector."""
        return f"NVector({self._elements})"

    def __eq__(self, other: object) -> bool:
        """
        Return True when other is an NVector with identical elements.

        Return False for objects that are not NVector objects.
        """
        if not isinstance(other, NVector):
            return False

        return self._elements == other._elements

    def __ne__(self, other: object) -> bool:
        """Return True when this NVector is not equal to other."""
        return not self == other

    def __add__(self, other: object) -> object:
        """
        Add another NVector element-by-element or add a real number
        to every element.

        Raises:
            ValueError: If two NVectors have different dimensions.
            TypeError: For unsupported operands.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same dimension")

            return NVector([
                self[i] + other[i]
                for i in range(len(self))
            ])

        if isinstance(other, Real):
            return NVector([
                value + other
                for value in self._elements
            ])

        return NotImplemented

    def __radd__(self, other: object) -> object:
        """Implement reflected addition such as 10 + NVector(...)."""
        return self + other

    def __mul__(self, other: object) -> object:
        """
        Multiply by another NVector using the dot product, or multiply
        every vector element by a real number.

        Raises:
            ValueError: If two NVectors have different dimensions.
            TypeError: For unsupported operands.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same dimension")

            total = 0

            for i in range(len(self)):
                total += self[i] * other[i]

            return total

        if isinstance(other, Real):
            return NVector([
                value * other
                for value in self._elements
            ])

        return NotImplemented

    def __rmul__(self, other: object) -> object:
        """Implement reflected multiplication such as 10 * NVector(...)."""
        return self * other

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """
        Return a new NVector of dimension n containing only zeros.

        Raises:
            TypeError: If n is not an integer.
            ValueError: If n is negative.
        """
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")

        if n < 0:
            raise ValueError("Dimension cannot be negative")

        return cls([0] * n)


def main() -> None:
    """Test the required NVector operations using the testif function."""

    student_id = input("Enter your FAU student ID: ")
    print("\nFAU Student ID:", student_id)
    print("Testing NVector")
    print("-" * 50)

    # a) Constructor using a list
    original = [3, 0, 1, -1]
    v1 = NVector(original)

    testif(
        v1 == NVector(3, 0, 1, -1),
        "constructor with sequence",
        "vector created correctly",
        "vector was not created correctly"
    )

    # Verify that the constructor made a NEW list
    original[0] = 100

    testif(
        v1[0] == 3,
        "constructor creates new list",
        "original list and vector are independent",
        "vector shares the original list"
    )

    # a) Constructor using a tuple
    v_tuple = NVector((3, 0, 1, -1))

    testif(
        v_tuple == NVector(3, 0, 1, -1),
        "constructor with tuple",
        "tuple constructor works",
        "tuple constructor failed"
    )

    # b) Constructor using multiple arguments
    v2 = NVector(3, 0, 1, -1)

    testif(
        v2 == NVector([3, 0, 1, -1]),
        "constructor with multiple arguments",
        "multiple argument constructor works",
        "multiple argument constructor failed"
    )

    # c) __len__
    testif(
        len(v2) == 4,
        "__len__",
        "length is 4",
        "incorrect vector length"
    )

    # d) __getitem__
    testif(
        v2[1] == 0,
        "__getitem__",
        "index 1 contains 0",
        "incorrect value at index 1"
    )

    # d) Negative indexing
    testif(
        v2[-2] == 1,
        "negative indexing",
        "negative index works",
        "negative index failed"
    )

    # e) __setitem__
    v3 = NVector(1, 2, 3, 4)
    v3[3] = 10

    testif(
        v3[3] == 10,
        "__setitem__",
        "indexed assignment works",
        "indexed assignment failed"
    )

    # f) __str__
    testif(
        str(v2) == "NVector([3, 0, 1, -1])",
        "__str__",
        "string representation works",
        "string representation failed"
    )

    # g) __eq__
    testif(
        NVector(1, 2, 3) == NVector(1, 2, 3),
        "__eq__",
        "equal vectors compare equal",
        "equal vectors do not compare equal"
    )

    # g) __eq__ with another type
    testif(
        (NVector(1, 2, 3) == [1, 2, 3]) is False,
        "__eq__ different type",
        "non-NVector comparison returns False",
        "non-NVector comparison failed"
    )

    # g) __ne__
    testif(
        NVector(1, 2, 3) != NVector(1, 2, 4),
        "__ne__",
        "different vectors compare unequal",
        "different vectors incorrectly compare equal"
    )

    # h) Vector addition
    addition = (
        NVector(3, 0, 1, -1)
        + NVector(1, 2, 3, 4)
    )

    testif(
        addition == NVector(4, 2, 4, 3),
        "__add__ vector addition",
        "element-wise addition works",
        "element-wise addition failed"
    )

    # h) Vector + number
    addition_number = NVector(3, 0, 1, -1) + 10

    testif(
        addition_number == NVector(13, 10, 11, 9),
        "__add__ scalar",
        "vector plus scalar works",
        "vector plus scalar failed"
    )

    # h) Number + vector
    reflected_addition = 10 + NVector(3, 0, 1, -1)

    testif(
        reflected_addition == NVector(13, 10, 11, 9),
        "__radd__",
        "reflected addition works",
        "reflected addition failed"
    )

    # i) Dot product
    dot_product = (
        NVector(3, 0, 1, -1)
        * NVector(1, 2, 3, 4)
    )

    testif(
        dot_product == 2,
        "__mul__ dot product",
        "dot product equals 2",
        "dot product is incorrect"
    )

    # i) Vector * number
    multiplication = NVector(1, 2, 3) * 10

    testif(
        multiplication == NVector(10, 20, 30),
        "__mul__ scalar",
        "scalar multiplication works",
        "scalar multiplication failed"
    )

    # i) Number * vector
    reflected_multiplication = 10 * NVector(1, 2, 3)

    testif(
        reflected_multiplication == NVector(10, 20, 30),
        "__rmul__",
        "reflected multiplication works",
        "reflected multiplication failed"
    )

    # j) zeros
    zero_vector = NVector.zeros(4)

    testif(
        zero_vector == NVector(0, 0, 0, 0),
        "zeros",
        "zero vector created correctly",
        "zero vector creation failed"
    )

    # Standard IndexError from __getitem__
    try:
        value = v2[100]

        testif(
            False,
            "__getitem__ IndexError",
            "",
            "invalid index did not raise IndexError"
        )

    except IndexError:
        testif(
            True,
            "__getitem__ IndexError",
            "invalid index raises IndexError",
            ""
        )

    # Standard IndexError from __setitem__
    try:
        v2[100] = 5

        testif(
            False,
            "__setitem__ IndexError",
            "",
            "invalid index did not raise IndexError"
        )

    except IndexError:
        testif(
            True,
            "__setitem__ IndexError",
            "invalid index raises IndexError",
            ""
        )

    # Different dimensions for addition
    try:
        result = NVector(1, 2) + NVector(1, 2, 3)

        testif(
            False,
            "addition dimension error",
            "",
            "different dimensions did not raise ValueError"
        )

    except ValueError:
        testif(
            True,
            "addition dimension error",
            "different dimensions raise ValueError",
            ""
        )

    # Different dimensions for dot product
    try:
        result = NVector(1, 2) * NVector(1, 2, 3)

        testif(
            False,
            "multiplication dimension error",
            "",
            "different dimensions did not raise ValueError"
        )

    except ValueError:
        testif(
            True,
            "multiplication dimension error",
            "different dimensions raise ValueError",
            ""
        )

    print("-" * 50)
    print("NVector testing finished.")


if __name__ == "__main__":
    main()