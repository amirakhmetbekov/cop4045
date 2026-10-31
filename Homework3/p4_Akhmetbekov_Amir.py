# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 23:01:26 2026

@author: Amir
"""

import os
from testif import testif


def ed_read(
    filename: str,
    from_: int = 0,
    to: int = -1
) -> str:
    """
    Return part of a UTF-8 text file as a string.

    Parameters:
        filename: Name of the file to read.
        from_: Starting character index, inclusive.
        to: Ending character index, exclusive.
            If -1, read through the end of the file.

    Returns:
        The requested part of the file.

    Raises:
        IndexError: If from_ or to is outside the valid range.
        ValueError: If the requested range is invalid.
        FileNotFoundError/OSError: Passed to the caller.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    length = len(content)

    if from_ < 0 or from_ > length:
        raise IndexError("Starting position is outside the file")

    if to == -1:
        to = length
    elif to < 0 or to > length:
        raise IndexError("Ending position is outside the file")

    if to < from_:
        raise ValueError(
            "Ending position cannot be before starting position"
        )

    return content[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """
    Find every occurrence of search_str in a UTF-8 text file.

    Parameters:
        filename: Name of the file to search.
        search_str: Non-empty string to locate.

    Returns:
        A list containing the character index of every occurrence.
        Returns an empty list when the string is not found.

    Raises:
        ValueError: If search_str is empty.
        FileNotFoundError/OSError: Passed to the caller.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = []
    start = 0

    while True:
        position = content.find(search_str, start)

        if position == -1:
            break

        positions.append(position)

        # Move one character ahead so overlapping matches
        # can also be found.
        start = position + 1

    return positions


def ed_replace(
    filename: str,
    search_str: str,
    replace_with: str,
    occurrence: int = -1
) -> int:
    """
    Replace occurrences of a string in a UTF-8 text file.

    Parameters:
        filename: Name of the file to modify.
        search_str: Non-empty string to search for.
        replace_with: Replacement string.
        occurrence: -1 replaces all occurrences. A value >= 0
            replaces only that occurrence, where 0 means the first.

    Returns:
        Number of replacements made.

    Raises:
        ValueError: If search_str is empty or occurrence is less than -1.
        FileNotFoundError/OSError: Passed to the caller.

    The file is not rewritten when no replacement is made or when
    a precondition error occurs.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty")

    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or a non-negative integer")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if occurrence == -1:
        replacement_count = content.count(search_str)

        if replacement_count == 0:
            return 0

        new_content = content.replace(
            search_str,
            replace_with
        )

    else:
        positions = []
        start = 0

        while True:
            position = content.find(search_str, start)

            if position == -1:
                break

            positions.append(position)
            start = position + 1

        if occurrence >= len(positions):
            return 0

        position = positions[occurrence]

        new_content = (
            content[:position]
            + replace_with
            + content[position + len(search_str):]
        )

        replacement_count = 1

    # All validation and processing is finished before
    # the original file is opened for writing.
    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_content)

    return replacement_count


def ed_append(filename: str, string: str) -> int:
    """
    Append a string to a UTF-8 text file.

    If the file does not exist, it is created.

    Parameters:
        filename: Name of the file to modify or create.
        string: String to append.

    Returns:
        Number of characters written.

    Raises:
        FileNotFoundError/OSError: Passed to the caller.
    """
    with open(filename, "a", encoding="utf-8") as file:
        characters_written = file.write(string)

    return characters_written


def test_ed_find() -> None:
    """Test ed_find() using the Homework 3 testif() function."""
    filename = "test_ed_find.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    result1 = ed_find(filename, "345")

    testif(
        result1 == [3, 13],
        "ed_find finds multiple occurrences",
        "returned [3, 13]",
        "did not return expected positions"
    )

    result2 = ed_find(filename, "999")

    testif(
        result2 == [],
        "ed_find missing string",
        "returned empty list",
        "did not return empty list"
    )

    result3 = ed_find(filename, "012")

    testif(
        result3 == [0, 10],
        "ed_find beginning positions",
        "found both occurrences",
        "incorrect positions"
    )

    os.remove(filename)


def test_ed_replace() -> None:
    """Test ed_replace() using the Homework 3 testif() function."""
    filename = "test_ed_replace.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    replacements = ed_replace(
        filename,
        "345",
        "ABCDE",
        1
    )

    with open(filename, "r", encoding="utf-8") as file:
        result = file.read()

    testif(
        replacements == 1
        and result == "0123456789012ABCDE6789",
        "ed_replace one occurrence",
        "second occurrence replaced correctly",
        "specific replacement failed"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    replacements = ed_replace(
        filename,
        "345",
        "ABCDE"
    )

    with open(filename, "r", encoding="utf-8") as file:
        result = file.read()

    testif(
        replacements == 2
        and result == "012ABCDE6789012ABCDE6789",
        "ed_replace all occurrences",
        "all occurrences replaced correctly",
        "replace-all failed"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write("hello world")

    replacements = ed_replace(
        filename,
        "Python",
        "Java"
    )

    with open(filename, "r", encoding="utf-8") as file:
        result = file.read()

    testif(
        replacements == 0
        and result == "hello world",
        "ed_replace missing string",
        "file remained unchanged",
        "file changed unexpectedly"
    )

    os.remove(filename)


def main() -> None:
    """Demonstrate and test all text editor functions."""
    student_id = input("Enter your FAU student ID: ")

    print("\nFAU Student ID:", student_id)
    print("Non-Interactive Text Editor")
    print("-" * 60)

    filename = "file1.txt"

    # Start with a new demonstration file.
    if os.path.exists(filename):
        os.remove(filename)

    print("\nTesting ed_append:")

    written = ed_append(
        filename,
        "0123456789"
    )

    print("Characters written:", written)

    written = ed_append(
        filename,
        "0123456789"
    )

    print("Characters written:", written)
    print("Complete file:", ed_read(filename))

    print("\nTesting ed_read:")

    print(
        "ed_read(file, 3, 9):",
        ed_read(filename, 3, 9)
    )

    print(
        "ed_read(file, 3):",
        ed_read(filename, 3)
    )

    print("\nTesting ed_find:")

    result = ed_find(
        filename,
        "345"
    )

    print("Positions of '345':", result)

    result = ed_find(
        filename,
        "356"
    )

    print("Positions of '356':", result)

    print("\nTesting ed_replace:")

    count = ed_replace(
        filename,
        "345",
        "ABCDE",
        1
    )

    print("Number replaced:", count)
    print("After replacing occurrence 1:")
    print(ed_read(filename))

    # Reset demonstration file.
    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    count = ed_replace(
        filename,
        "345",
        "ABCDE"
    )

    print("\nNumber replaced:", count)
    print("After replacing all occurrences:")
    print(ed_read(filename))

    print("\nRunning ed_find unit tests:")
    test_ed_find()

    print("\nRunning ed_replace unit tests:")
    test_ed_replace()

    print("\nAll demonstrations finished.")


if __name__ == "__main__":
    main()