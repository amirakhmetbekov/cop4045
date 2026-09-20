# -*- coding: utf-8 -*-

import math
import sys


def read_observations(filename: str) -> tuple:
    """Read valid weather observations and report invalid input lines."""
    observations = {}
    errors = []
    seen = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            fields = line.rstrip("\n\r").split(",")

            if len(fields) != 3:
                errors.append((line_number, "malformed line"))
                continue

            station, date, temperature_text = fields

            if not station or not date:
                errors.append((line_number, "malformed line"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "temperature is not a valid float"))
                continue

            if not math.isfinite(temperature) or not -100.0 <= temperature <= 150.0:
                errors.append((line_number, "temperature is outside the valid range"))
                continue

            key = (station, date)
            if key in seen:
                errors.append((line_number, "duplicate station/date combination"))
                continue

            seen.add(key)
            observations.setdefault(station, []).append((date, temperature))

    for station in observations:
        observations[station].sort(key=lambda item: item[0])

    return observations, errors


def station_statistics(observations: dict) -> dict:
    """Calculate minimum, maximum, and mean temperature for each station."""
    statistics = {}

    for station, station_observations in observations.items():
        temperatures = [
            temperature
            for date, temperature in station_observations
        ]

        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures)
        }

    return statistics


def station_outliers(observations: dict) -> dict:
    """Return stations whose latest temperature exceeds their mean."""
    statistics = station_statistics(observations)
    latest_observations = {
        station: station_observations[-1]
        for station, station_observations in observations.items()
    }

    return {
        station: (date, temperature, statistics[station]["mean"])
        for station, (date, temperature) in latest_observations.items()
        if temperature > statistics[station]["mean"]
    }


def write_statistics(filename: str, statistics: dict) -> None:
    """Write station statistics in lexicographic station order."""
    with open(filename, "w", encoding="utf-8") as file:
        for station in sorted(statistics):
            station_statistics = statistics[station]
            file.write(
                f"{station},{station_statistics['min']:.1f},"
                f"{station_statistics['max']:.1f},"
                f"{station_statistics['mean']:.1f}\n"
            )


def main() -> None:
    """Analyze observations from command-line input and write statistics."""
    if len(sys.argv) != 3:
        print("Usage: python p5_Akhmetbekov_Amir.py input_file output_file")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)
        write_statistics(output_filename, statistics)
    except OSError as error:
        print(f"File error: {error}")
        return

    if errors:
        print("Input errors:")
        for line_number, error_message in errors:
            print(f"Line {line_number}: {error_message}")

    print("Statistics:")
    for station in sorted(statistics):
        print(station, statistics[station])

    print("Outliers:")
    for station in sorted(outliers):
        print(station, outliers[station])


if __name__ == "__main__":
    main()
