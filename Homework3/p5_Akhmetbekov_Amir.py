import turtle
from testif import testif



# Part a - Recursive Leaf


def draw_leaf_straight(level: int, length: float) -> None:
    """
    Recursively draw a straight-stem leaf.

    Parameters:
        level: Recursion level.
        length: Length of the current stem.
    """
    if level <= 0 or length <= 2:
        return

    start_position = turtle.position()
    start_heading = turtle.heading()

    # First part of the stem
    turtle.forward(length * 0.35)

    # Left branch
    turtle.left(40)
    draw_leaf_straight(
        level - 1,
        length * 0.55
    )

    turtle.setheading(start_heading)

    # Continue farther up the main stem
    turtle.forward(length * 0.25)

    # Right branch
    turtle.right(40)
    draw_leaf_straight(
        level - 1,
        length * 0.55
    )

    turtle.setheading(start_heading)

    # Finish the main stem
    turtle.forward(length * 0.40)

    # Return without drawing
    turtle.penup()
    turtle.goto(start_position)
    turtle.setheading(start_heading)
    turtle.pendown()


def draw_leaf_curved(level: int, length: float) -> None:
    """
    Recursively draw a curved leaf for the extra-credit part.

    Parameters:
        level: Recursion level.
        length: Length of the current curved stem.
    """
    if level <= 0 or length <= 1:
        return

    start_position = turtle.position()
    start_heading = turtle.heading()

    branch_length = length * 0.58
    segments = 5

    for segment in range(segments):
        turtle.forward(length / segments)
        turtle.left(4)

        # Create branches partway up the curved stem.
        if segment == 1:
            branch_heading = turtle.heading()

            turtle.left(38)
            draw_leaf_curved(
                level - 1,
                branch_length
            )

            turtle.setheading(branch_heading)

            turtle.right(38)
            draw_leaf_curved(
                level - 1,
                branch_length
            )

            turtle.setheading(branch_heading)

    # Return without drawing another line.
    turtle.penup()
    turtle.goto(start_position)
    turtle.setheading(start_heading)
    turtle.pendown()


def setup_leaf_window(title: str) -> None:
    """Prepare the turtle window for drawing a vertical leaf."""
    turtle.reset()
    turtle.title(title)

    turtle.speed(0)
    turtle.delay(0)
    turtle.tracer(False)

    turtle.hideturtle()
    turtle.pensize(1)

    turtle.penup()
    turtle.goto(0, -250)

    # Turtle starts facing East. Turn it left 90 degrees.
    turtle.setheading(90)

    turtle.pendown()


def show_straight_leaf() -> None:
    """Draw the required straight leaf using draw_leaf_straight(6, 120)."""
    setup_leaf_window(
        "Recursive Straight Leaf"
    )

    draw_leaf_straight(6, 120)

    turtle.update()
    turtle.done()


def show_curved_leaf() -> None:
    """Draw the extra-credit curved leaf using draw_leaf_curved(6, 120)."""
    setup_leaf_window(
        "Recursive Curved Leaf"
    )

    draw_leaf_curved(6, 120)

    turtle.update()
    turtle.done()



# Part b - Base X Conversion


DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def strB(n: int, base: int = 10) -> str:
    """
    Recursively convert a non-negative integer to another base.

    Parameters:
        n: Non-negative integer to convert.
        base: Integer base from 2 through 26.

    Returns:
        String representation of n in the requested base.

    Raises:
        TypeError: If n or base is not an integer.
        ValueError: If n is negative or base is outside 2 through 26.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if not isinstance(base, int):
        raise TypeError("base must be an integer")

    if n < 0:
        raise ValueError(
            "n must be non-negative"
        )

    if base < 2 or base > 26:
        raise ValueError(
            "base must be between 2 and 26"
        )

    # Recursive base case.
    if n < base:
        return DIGITS[n]

    # Recursive step.
    return (
        strB(n // base, base)
        + DIGITS[n % base]
    )


def test_strB() -> None:
    """Run four unit tests for the recursive strB function."""

    testif(
        strB(42, 2) == "101010",
        "strB base 2",
        "42 converted correctly",
        "42 conversion failed"
    )

    testif(
        strB(255, 16) == "FF",
        "strB base 16",
        "255 converted correctly",
        "255 conversion failed"
    )

    testif(
        strB(625, 25) == "100",
        "strB base 25",
        "625 converted correctly",
        "625 conversion failed"
    )

    testif(
        strB(35, 26) == "19",
        "strB base 26",
        "35 converted correctly",
        "35 conversion failed"
    )



# Part c - Memoized Binomial Coefficient


_cnk_memo: dict[tuple[int, int], int] = {}


def Cnk_m(n: int, k: int) -> int:
    """
    Recursively calculate the binomial coefficient n-choose-k
    using memoization.

    Parameters:
        n: Non-negative integer.
        k: Integer from 0 through n.

    Returns:
        The binomial coefficient C(n, k).

    Raises:
        TypeError: If n or k is not an integer.
        ValueError: If n or k is outside the valid range.
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError(
            "n and k must be integers"
        )

    if n < 0:
        raise ValueError(
            "n cannot be negative"
        )

    if k < 0 or k > n:
        raise ValueError(
            "k must be between 0 and n"
        )

    key = (n, k)

    if key in _cnk_memo:
        return _cnk_memo[key]

    # Base cases:
    # C(n, 0) = C(n, n) = 1
    if k == 0 or k == n:
        _cnk_memo[key] = 1
        return 1

    # Recursive formula:
    # C(n,k) = C(n-1,k-1) + C(n-1,k)
    result = (
        Cnk_m(n - 1, k - 1)
        + Cnk_m(n - 1, k)
    )

    _cnk_memo[key] = result

    return result


def test_Cnk_m() -> None:
    """Run four unit tests for Cnk_m."""

    testif(
        Cnk_m(5, 2) == 10,
        "Cnk_m C(5,2)",
        "result is 10",
        "incorrect result"
    )

    testif(
        Cnk_m(10, 0) == 1,
        "Cnk_m base case k=0",
        "result is 1",
        "base case failed"
    )

    testif(
        Cnk_m(10, 10) == 1,
        "Cnk_m base case k=n",
        "result is 1",
        "base case failed"
    )

    testif(
        Cnk_m(12, 4) == 495,
        "Cnk_m C(12,4)",
        "result is 495",
        "incorrect result"
    )


def run_Cnk() -> None:
    """Display several interesting memoized binomial coefficients."""

    print("C(20, 10) =", Cnk_m(20, 10))
    print("C(30, 15) =", Cnk_m(30, 15))
    print("C(40, 20) =", Cnk_m(40, 20))
    print("C(50, 25) =", Cnk_m(50, 25))



# Part d - Making Pairs


def make_pairs(
    seq1: list,
    seq2: list
) -> list[tuple]:
    """
    Recursively pair corresponding elements from two lists.

    The function stops when the end of either list is reached.

    Parameters:
        seq1: First list.
        seq2: Second list.

    Returns:
        A list of tuples containing corresponding elements.
    """
    # Base case.
    if len(seq1) == 0 or len(seq2) == 0:
        return []

    # Recursive step.
    return (
        [(seq1[0], seq2[0])]
        + make_pairs(
            seq1[1:],
            seq2[1:]
        )
    )


def test_make_pairs() -> None:
    """Run five unit tests for make_pairs."""

    testif(
        make_pairs(
            [1, 2, 3],
            [4, 5, 6]
        )
        == [(1, 4), (2, 5), (3, 6)],
        "make_pairs equal lengths",
        "pairs created correctly",
        "incorrect pairs"
    )

    testif(
        make_pairs(
            [1, 2, 3],
            [4, 5]
        )
        == [(1, 4), (2, 5)],
        "make_pairs second list shorter",
        "stopped at shorter list",
        "incorrect result"
    )

    testif(
        make_pairs(
            [1, 2, 3],
            [4, 5, 6, 7, 8, 9]
        )
        == [(1, 4), (2, 5), (3, 6)],
        "make_pairs first list shorter",
        "stopped at shorter list",
        "incorrect result"
    )

    testif(
        make_pairs(
            [],
            [4, 5, 6]
        )
        == [],
        "make_pairs first list empty",
        "returned empty list",
        "empty-list case failed"
    )

    testif(
        make_pairs(
            [1, 2, 3],
            []
        )
        == [],
        "make_pairs second list empty",
        "returned empty list",
        "empty-list case failed"
    )



# Main


def main() -> None:
    """Run required console tests for Problem 5."""

    student_id = input(
        "Enter your FAU student ID: "
    )

    print(
        "\nFAU Student ID:",
        student_id
    )

    print("\nProblem 5 - Recursive Functions")
    print("-" * 60)

    print("\nPart b - strB unit tests:")
    test_strB()

    print("\nAdditional strB examples:")
    print(
        "strB(42, base=2) =",
        strB(42, 2)
    )
    print(
        "strB(255, base=16) =",
        strB(255, 16)
    )
    print(
        "strB(500, base=8) =",
        strB(500, 8)
    )
    print(
        "strB(35, base=26) =",
        strB(35, 26)
    )

    print("\nPart c - Cnk_m unit tests:")
    test_Cnk_m()

    print("\nPart d - make_pairs unit tests:")
    test_make_pairs()

    print("\nExample make_pairs result:")
    print(
        make_pairs(
            ["A", "B", "C"],
            [10, 20, 30, 40]
        )
    )

    print("\nAll console tests finished.")


if __name__ == "__main__":
    main()
