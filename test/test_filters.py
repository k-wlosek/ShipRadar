"""
Tests for reader.py module - filters
"""

import unittest
import ast
from datetime import datetime
from src import err
from src.reader import ShipRadarFilter, ShipRadarCSVReader


class TestReadFilters(unittest.TestCase):
    """
    Tests for ShipRadarFilter class
    """
    def test_name(self):
        """
        Test for ship name filter
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'WINDSUPPLIER')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/name_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter ship name")

    def test_ship_no(self):
        """
        Test for LIRMO ship number filter
        :return:
        """
        filters = ShipRadarFilter('ship_no', 9295490)
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/number_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter ship number")

    def test_ship_type(self):
        """
        Test for ship type filter
        :return:
        """
        filters = ShipRadarFilter('ship_type', 'Cargo')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/type_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter ship type")

    def test_move_status(self):
        """
        Test for move status filter
        :return:
        """
        filters = ShipRadarFilter('move_status', 'Moored')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/move_status_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter move status")

    def test_heading(self):
        """
        Test for heading filter
        :return:
        """
        filters = ShipRadarFilter('heading', 42)
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/heading_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter heading")

    def test_draught(self):
        """
        Test for draught filter
        :return:
        """
        filters = ShipRadarFilter('draught', 3.0)
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/draught_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter draught")

    def test_speed(self):
        """
        Test for speed filter
        :return:
        """
        filters = ShipRadarFilter('speed', 0.1)
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/speed_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter speed")

    def test_destination(self):
        """
        Test for destination filter
        :return:
        """
        filters = ShipRadarFilter('destination', 'ESBJERG')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/destination_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter destination")

    def test_eta(self):
        """
        Test for eta filter
        :return:
        """
        filters = ShipRadarFilter('eta', datetime.fromisoformat('9999-12-31 23:59:59.000'))
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/eta_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter eta")

    def test_time(self):
        """
        Test for time filter
        :return:
        """
        filters = ShipRadarFilter('date',
                                  datetime.fromisoformat('2011-12-31 10:57:13.000'),
                                  datetime.fromisoformat('2012-01-01 20:57:14.000'))
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/time_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter time")

    def test_coords(self):
        """
        Test for coords filter
        :return:
        """
        filters = ShipRadarFilter('coords', 8.0, 55.0, 11.0, 56.0)
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with open('expected/coords_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        self.assertEqual(reader.parse(filters), expected, "Failed test: CSV filter coords")

    def test_nonexistent_filter(self):
        """
        Test for nonexistent filter
        :return:
        """
        with self.assertRaises(err.ShipRadarFilterError) as exc:
            _ = ShipRadarFilter('none', 0)  # Result is not used, so it is not assigned to a variable
        self.assertTrue('Filter type does not exist' in str(exc.exception))

    def test_null_result_filter(self):
        """
        Test for filter that returns no results
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'DefinitelyNotTest')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        with self.assertRaises(err.ShipRadarFilterError) as exc:
            reader.parse(filters)
        self.assertTrue("No entries for this filter: ship_name: DefinitelyNotTest" in str(exc.exception))
