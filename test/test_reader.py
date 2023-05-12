import unittest

import src.err as err
from src.reader import ShipRadarFilter, ShipRadarCSVReader


class TestReadFilters(unittest.TestCase):
    def test_name(self):
        """
        Test for ship name filter
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'Test')
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'Test', 'date': '202301011202', 'location': 'x500y200'}],
                         "Failed test: CSV filter ship name")

    def test_time(self):
        """
        Test for time filter
        :return:
        """
        filters = ShipRadarFilter('date', '20230101', 721)
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'NotTest', 'date': '202301011200', 'location': 'x220y220'}],
                         "Failed test: CSV filter time")

    def test_coords(self):
        """
        Test for coords filter
        :return:
        """
        filters = ShipRadarFilter('coords', 0, 0, 300, 300)
        reader = ShipRadarCSVReader('data.csv')
        self.assertEqual(reader.parse(filters), [{'ship': 'Test', 'date': '202301011200', 'location': 'x0y0'},
                                                 {'ship': 'Test', 'date': '202301011201', 'location': 'x200y200'},
                                                 {'ship': 'NotTest', 'date': '202301011200', 'location': 'x220y220'}],
                         "Failed test: CSV filter coords")

    def test_nonexistent_filter(self):
        """
        Test for nonexistent filter
        :return:
        """
        with self.assertRaises(err.ShipRadarFilterError) as exc:
            filters = ShipRadarFilter('none', 0)
        self.assertTrue('Filter type does not exist' in str(exc.exception))

    def test_null_result_filter(self):
        """
        Test for filter that returns no results
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'DefinitelyNotTest')
        reader = ShipRadarCSVReader('data.csv')
        with self.assertRaises(err.ShipRadarFilterError) as exc:
            reader.parse(filters)
        self.assertTrue("No entries for this filter: ship_name: DefinitelyNotTest" in str(exc.exception))


# TODO write tests for invalid CSV file
class TestCSVReader(unittest.TestCase):
    def test_nonexistent_file(self):
        """
        Test for nonexistent file
        :return:
        """
        filters = ShipRadarFilter('ship_name', 'Test')
        reader = ShipRadarCSVReader('not_data.csv')
        with self.assertRaises(err.ShipRadarImportError) as exc:
            reader.parse(filters)
        self.assertTrue("No file not_data.csv" in str(exc.exception))
