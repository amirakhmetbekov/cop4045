"""Unit tests for the Problem 6 file-system hierarchy."""

import unittest

from p6_Akhmetbekov_Amir import File, Folder, find_large_files


class AbsolutePathTests(unittest.TestCase):
    """Tests for Entry.absolute_path()."""

    def setUp(self) -> None:
        """Create a hierarchy with three nested folder levels."""
        self.root = Folder("root")
        self.level_one = Folder("level_one")
        self.level_two = Folder("level_two")
        self.level_three = Folder("level_three")
        self.file = File("report.txt", 120)

        self.root.add(self.level_one)
        self.level_one.add(self.level_two)
        self.level_two.add(self.level_three)
        self.level_three.add(self.file)

    def test_path_starts_with_entry_and_ends_with_root(self) -> None:
        """A nested entry's path lists itself first and root last."""
        self.assertEqual(
            self.file.absolute_path(),
            [
                self.file,
                self.level_three,
                self.level_two,
                self.level_one,
                self.root,
            ],
        )

    def test_root_path_contains_only_root(self) -> None:
        """An entry without a parent has a one-element path."""
        self.assertEqual(self.root.absolute_path(), [self.root])


class FindLargeFilesTests(unittest.TestCase):
    """Tests for the recursive find_large_files() function."""

    def setUp(self) -> None:
        """Create a nested hierarchy with files of varied sizes."""
        self.root = Folder("root")
        self.level_one = Folder("level_one")
        self.level_two = Folder("level_two")
        self.level_three = Folder("level_three")

        self.small_file = File("small.txt", 10)
        self.medium_file = File("medium.txt", 50)
        self.large_file = File("large.txt", 100)
        self.root.add(self.small_file)
        self.root.add(self.level_one)
        self.level_one.add(self.medium_file)
        self.level_one.add(self.level_two)
        self.level_two.add(self.level_three)
        self.level_three.add(self.large_file)

    def test_file_passed_directly_meets_threshold(self) -> None:
        """A qualifying File passed directly is returned by itself."""
        self.assertEqual(find_large_files(self.large_file, 100), [self.large_file])

    def test_file_passed_directly_below_threshold(self) -> None:
        """A File passed directly is excluded when it is below the threshold."""
        self.assertEqual(find_large_files(self.small_file, 11), [])

    def test_folder_search_with_different_thresholds(self) -> None:
        """A Folder search recurses and includes files meeting each threshold."""
        self.assertEqual(
            find_large_files(self.root, 50),
            [self.medium_file, self.large_file],
        )
        self.assertEqual(find_large_files(self.root, 101), [])

    def test_folder_search_includes_file_at_threshold(self) -> None:
        """Files exactly at the minimum size are included."""
        self.assertEqual(
            find_large_files(self.root, 10),
            [self.small_file, self.medium_file, self.large_file],
        )


class FolderAddTests(unittest.TestCase):
    """Tests for Folder.add() cycle prevention."""

    def test_rejects_self_and_ancestor_cycles(self) -> None:
        """A folder cannot contain itself or an ancestor of its own."""
        root = Folder("root")
        child = Folder("child")
        grandchild = Folder("grandchild")
        root.add(child)
        child.add(grandchild)

        with self.assertRaises(ValueError):
            root.add(root)
        with self.assertRaises(ValueError):
            grandchild.add(root)


if __name__ == "__main__":
    unittest.main()
