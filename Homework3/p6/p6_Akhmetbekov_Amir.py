"""Base classes for the Problem 6 file-system hierarchy."""

from __future__ import annotations

from typing import List, Optional


class Entry:
    """Base class for an entry in a file-system hierarchy."""

    def __init__(
        self: Entry,
        name: str,
        parent: Optional[Entry] = None,
    ) -> None:
        """Initialize an entry with its name and optional parent."""
        self.name: str = name
        self._parent: Optional[Entry] = parent

    def parent(self: Entry) -> Optional[Entry]:
        """Return this entry's parent, or None if it has no parent."""
        return self._parent

    def absolute_path(self: Entry) -> List[Entry]:
        """Return this entry and its ancestors, ending with the root entry."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def size(self: Entry) -> int:
        """Return this entry's size in bytes."""
        raise NotImplementedError("Entry subclasses must implement size().")


class File(Entry):
    """A file-system entry that stores a nonnegative number of bytes."""

    def __init__(
        self: File,
        name: str,
        bytes_used: int,
        parent: Optional[Entry] = None,
    ) -> None:
        """Initialize a file with its name, size, and optional parent."""
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative.")

        super().__init__(name, parent)
        self.bytes_used: int = bytes_used

    def size(self: File) -> int:
        """Return the number of bytes used by this file."""
        return self.bytes_used


class Folder(Entry):
    """A file-system entry that contains other entries."""

    def __init__(
        self: Folder,
        name: str,
        parent: Optional[Entry] = None,
    ) -> None:
        """Initialize an empty folder with its name and optional parent."""
        super().__init__(name, parent)
        self._children: List[Entry] = []

    def add(self: Folder, entry: Entry) -> None:
        """Add an entry as a child and update its parent reference.

        Raises:
            ValueError: If adding the entry would create a hierarchy cycle.
        """
        ancestor: Optional[Entry] = self
        while ancestor is not None:
            if ancestor is entry:
                raise ValueError("Adding this entry would create a cycle.")
            ancestor = ancestor.parent()

        self._children.append(entry)
        entry._parent = self

    def size(self: Folder) -> int:
        """Return the total size of this folder's children in bytes."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> List[File]:
    """Recursively find files at least as large as the given byte threshold.

    Args:
        entry: The file or folder to search.
        minimum_size: The minimum file size in bytes to include.

    Returns:
        A list of matching files contained in entry.

    Raises:
        TypeError: If entry is not a File or Folder.
    """
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []

    if isinstance(entry, Folder):
        large_files: List[File] = []
        for child in entry._children:
            large_files.extend(find_large_files(child, minimum_size))
        return large_files

    raise TypeError("entry must be a File or Folder.")


def main() -> None:
    """Demonstrate the file-system hierarchy and its recursive operations."""
    student_id: str = input("Enter your FAU student ID: ").strip()
    print(f"FAU student ID: {student_id if student_id else '(not entered)'}")

    root = Folder("root")
    college = Folder("college")
    courses = Folder("courses")
    homework = Folder("homework3")

    root.add(File("readme.txt", 80))
    root.add(college)
    college.add(File("schedule.pdf", 250))
    college.add(courses)
    courses.add(File("syllabus.pdf", 900))
    courses.add(homework)
    project_file = File("project.py", 1200)
    homework.add(project_file)

    print("\nFile sizes:")
    print(f"  readme.txt: 80 bytes")
    print(f"  schedule.pdf: 250 bytes")
    print(f"  syllabus.pdf: 900 bytes")
    print(f"  project.py: {project_file.size()} bytes")
    print(f"\nTotal size of outermost folder '{root.name}': {root.size()} bytes")

    for minimum_size in (200, 900):
        matching_files: List[File] = find_large_files(root, minimum_size)
        print(f"\nFiles at least {minimum_size} bytes:")
        for matching_file in matching_files:
            print(f"  {matching_file.name}: {matching_file.size()} bytes")

    print(f"\nAbsolute path for '{project_file.name}' (current entry to root):")
    for path_entry in project_file.absolute_path():
        print(f"  {path_entry.name} ({type(path_entry).__name__})")


if __name__ == "__main__":
    main()
