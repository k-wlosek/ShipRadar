import unittest
from src.reader import ShipRadarFilter, ShipRadarCSVReader


class TestReadFilters(unittest.TestCase):
    def test_name(self):
        filters = ShipRadarFilter('ship_name', 'Test')
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'Test', 'date': '202301011202', 'location': 'x500y200'}],
                         "Failed test: CSV filter ship name")

    def test_time(self):
        filters = ShipRadarFilter('date', '20230101', 721)
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'NotTest', 'date': '202301011200', 'location': 'x220y220'}],
                         "Failed test: CSV filter time")

    def test_coords(self):
        filters = ShipRadarFilter('coords', 0, 0, 300, 300)
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'NotTest', 'date': '202301011200', 'location': 'x220y220'}],
                         "Failed test: CSV filter coords")


# TODO write tests for invalid CSV file
