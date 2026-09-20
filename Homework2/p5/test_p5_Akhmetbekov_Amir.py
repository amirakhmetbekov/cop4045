# -*- coding: utf-8 -*-

import tempfile
import unittest
from pathlib import Path

from p5_Akhmetbekov_Amir import (
    read_observations,
    station_statistics,
    write_statistics,
)


class TestWeatherStationAnalyzer(unittest.TestCase):

    def create_input_file(self, contents: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        filename = Path(directory.name) / "observations.csv"
        filename.write_text(contents, encoding="utf-8")
        return filename

    def test_read_observations_several_stations_and_negative_temperatures(self):
        filename = self.create_input_file(
            "Station B,2026-02-02,-5.5\n"
            "Station A,2026-02-03,10.0\n"
            "Station B,2026-02-01,-10.0\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(
            observations,
            {
                "Station A": [("2026-02-03", 10.0)],
                "Station B": [
                    ("2026-02-01", -10.0),
                    ("2026-02-02", -5.5),
                ],
            },
        )

    def test_read_observations_rejects_duplicate_station_date(self):
        filename = self.create_input_file(
            "Station A,2026-02-01,5.0\n"
            "Station A,2026-02-01,7.0\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {"Station A": [("2026-02-01", 5.0)]})
        self.assertEqual(errors, [(2, "duplicate station/date combination")])

    def test_read_observations_rejects_invalid_temperature_ranges(self):
        filename = self.create_input_file(
            "Station A,2026-02-01,-100.1\n"
            "Station B,2026-02-01,150.1\n"
            "Station C,2026-02-01,not-a-number\n"
            "Station D,2026-02-01,nan\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 4)
        self.assertEqual(errors[0][0], 1)
        self.assertEqual(errors[1][0], 2)
        self.assertEqual(errors[2][0], 3)
        self.assertEqual(errors[3][0], 4)

    def test_station_statistics_calculates_minimum_maximum_and_mean(self):
        observations = {
            "Station A": [
                ("2026-02-01", -2.0),
                ("2026-02-02", 4.0),
                ("2026-02-03", 7.0),
            ],
            "Station B": [("2026-02-01", -8.5)],
        }

        statistics = station_statistics(observations)

        self.assertEqual(
            statistics,
            {
                "Station A": {"min": -2.0, "max": 7.0, "mean": 3.0},
                "Station B": {"min": -8.5, "max": -8.5, "mean": -8.5},
            },
        )

    def test_write_statistics_sorts_stations_and_formats_values(self):
        statistics = {
            "Zulu": {"min": -2.25, "max": 10.0, "mean": 3.125},
            "Alpha": {"min": -10.0, "max": 4.56, "mean": -2.345},
        }
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        filename = Path(directory.name) / "statistics.csv"

        write_statistics(filename, statistics)

        self.assertEqual(
            filename.read_text(encoding="utf-8"),
            "Alpha,-10.0,4.6,-2.3\nZulu,-2.2,10.0,3.1\n",
        )

    def test_read_observations_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            read_observations("file-that-does-not-exist.csv")

    def test_write_statistics_missing_directory(self):
        with self.assertRaises(FileNotFoundError):
            write_statistics(
                "missing-directory/statistics.csv",
                {},
            )


if __name__ == "__main__":
    unittest.main()
