# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 16:22:27 2026

@author: Amir
"""

import csv


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a new user to the social network."""
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print("Error adding user:", error)
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friendship between two users."""
    try:
        if user1 not in sn or user2 not in sn:
            return False

        if user1 == user2:
            return False

        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)

        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True

    except Exception as error:
        print("Error adding friend:", error)
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return all friends of a user up to the given link distance."""
    try:
        if user1 not in sn or distance <= 0:
            return []

        visited = {user1}
        current_level = [user1]
        result = []

        for level in range(distance):
            next_level = []

            for user in current_level:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        next_level.append(friend)
                        result.append(friend)

            current_level = next_level

            if len(current_level) == 0:
                break

        return result

    except Exception as error:
        print("Error getting friends:", error)
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save the social network to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for username in sn:
                fullname = sn[username][0]
                friends = sn[username][1]

                row = [username, fullname] + friends
                writer.writerow(row)

    except Exception as error:
        print("Error saving network:", error)
        raise


def load_network(filename: str) -> dict:
    """Load a social network from a CSV file."""
    try:
        sn = {}

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    username = row[0]
                    fullname = row[1]
                    friends = row[2:]

                    sn[username] = (fullname, friends)

        return sn

    except Exception as error:
        print("Error loading network:", error)
        raise


def main() -> None:
    """Test all social network functions."""
    try:
        print("Amir Akhmetbekov")

        sn = {
            "alice": ("Alice Smith", ["maria"]),
            "maria": ("Maria Cortez", ["alice", "joe", "david"]),
            "joe": ("Joseph Adams", ["maria", "eve"]),
            "eve": ("Evelyn Cooper", ["joe"]),
            "david": ("David Benson", ["maria"])
        }

        print("\nPart a - add_user:")
        print(add_user(sn, "sam", "Sam Wilson"))
        print(sn["sam"])

        print("\nPart b - add_friend:")
        print(add_friend(sn, "sam", "eve"))
        print("Sam's friends:", sn["sam"][1])
        print("Eve's friends:", sn["eve"][1])

        print("\nPart c - get_friends:")
        print("alice, distance 1:", get_friends(sn, "alice", 1))
        print("alice, distance 2:", get_friends(sn, "alice", 2))
        print("wrong username:", get_friends(sn, "unknown", 2))

        print("\nPart d - save_network:")
        save_network("social_network.csv", sn)
        print("Network saved to social_network.csv")

        print("\nPart e - load_network:")
        loaded_network = load_network("social_network.csv")
        print(loaded_network)

    except Exception as error:
        print("Error in main:", error)
        raise


if __name__ == "__main__":
    main()