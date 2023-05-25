"""
Tests for reader.py module - CSV reader
"""

import ast
import unittest
from src import err
from src.reader import ShipRadarFilter, ShipRadarCSVReader


class TestCSVReader(unittest.TestCase):
    """
    Tests for ShipRadarCSVReader class
    """
    def test_nonexistent_file(self):
        """
        Test for nonexistent file
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'Test')
        reader = ShipRadarCSVReader('not_data.csv')
        with self.assertRaises(err.ShipRadarImportError) as exc:
            reader.parse(filters)
        self.assertTrue("No file not_data.csv" in str(exc.exception), "Failed test: CSV nonexistent file")

    def test_and_collectors(self):
        """
        Test for and collectors method
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'SILUNA ACE')
        filters2 = ShipRadarFilter('ship_type', 'Passenger')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        collectors = [reader.parse(filters), reader.parse(filters2)]
        with open('expected/and_collectors_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        real = reader.and_collectors(collectors)
        # The order is inconsistent, so we compare the lengths and then the contents
        self.assertEqual(len(real), len(expected), "Failed test: CSV and_collectors\nLengths do not match")
        for item in real:
            self.assertIn(item, expected, "Failed test: CSV and_collectors\nContents do not match")

    def test_divide_collectors(self):
        """
        Test for divide collectors method
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'SILUNA ACE')
        filters2 = ShipRadarFilter('ship_type', 'Passenger')
        reader = ShipRadarCSVReader('baza_reduced.csv')
        collectors = [reader.parse(filters), reader.parse(filters2)]
        and_collectors = reader.and_collectors(collectors)
        with open('expected/divide_collectors_test.txt', encoding='utf-8') as f:
            for line in f:
                expected = ast.literal_eval(line)
        real = reader.divide_collectors(and_collectors)
        # The order is inconsistent, so we compare the lengths and then the contents
        self.assertEqual(len(real), len(expected), "Failed test: CSV divide_collectors\nLengths do not match")
        for item in real:
            self.assertIn(item, expected, "Failed test: CSV divide_collectors\nContents do not match")

    def test_verify_headers(self):
        """
        Test for verify headers method
        :return:
        """
        self.assertTrue(ShipRadarCSVReader.verify_headers('baza_reduced.csv'),
                        "Failed test: CSV verify_headers")
