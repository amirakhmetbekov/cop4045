# -*- coding: utf-8 -*-

import csv


def load_casts(filename: str) -> dict:
    """Read the casts CSV file and return movie cast information."""
    casts = {}

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            title = row[0]
            year = row[1]
            director = row[2]
            actors = row[3:]

            casts[(title, year)] = (director, actors)

    return casts


def display_top_collaborations(
        rated_filename: str,
        casts_filename: str,
        limit: int = None) -> None:
    """Display director and actor collaborations for top-rated movies."""

    casts = load_casts(casts_filename)
    collaborations = {}

    with open(rated_filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            movie = (row["Title"], row["Year"])

            if movie in casts:
                director = casts[movie][0]
                actors = casts[movie][1]

                for actor in actors:
                    pair = (director, actor)

                    if pair in collaborations:
                        collaborations[pair] += 1
                    else:
                        collaborations[pair] = 1

    ranking = [
        (director, actor, count)
        for (director, actor), count in collaborations.items()
    ]

    ranking.sort(key=lambda item: item[2], reverse=True)

    if limit is not None:
        ranking = ranking[:limit]

    for item in ranking:
        print(item)


def display_top_actors(
        grossing_filename: str,
        casts_filename: str,
        limit: int = None) -> None:
    """Display actors ranked by total box office money."""

    casts = load_casts(casts_filename)
    actor_totals = {}

    with open(grossing_filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            movie = (row["Title"], row["Year"])

            if movie in casts:
                box_office = int(row["USA Box Office"])
                actors = casts[movie][1]

                for actor in actors:
                    if actor in actor_totals:
                        actor_totals[actor] += box_office
                    else:
                        actor_totals[actor] = box_office

    ranking = [
        (actor, total)
        for actor, total in actor_totals.items()
    ]

    ranking.sort(key=lambda item: item[1], reverse=True)

    if limit is not None:
        ranking = ranking[:limit]

    for item in ranking:
        print(item)


def main() -> None:
    """Test the functions for parts a and b."""

    print("Amir Akhmetbekov")

    casts_file = "imdb-top-casts.csv"
    rated_file = "imdb-top-rated.csv"
    grossing_file = "imdb-top-grossing.csv"

    print("\nPart a - Top Collaborations:")
    display_top_collaborations(
        rated_file,
        casts_file,
        10
    )

    print("\nPart b - Top Actors:")
    display_top_actors(
        grossing_file,
        casts_file,
        10
    )


if __name__ == "__main__":
    main()