import src.err as err
import csv
from datetime import datetime, timedelta
import numpy as np


class ShipRadarFilter:
    type = None
    filter = None

    def __init__(self, type: str, *args):
        self.filter = None
        self.type = type
        self.additional_info = args
        self.parse_type()

    def parse_type(self):
        match self.type:
            case 'ship_name':
                self.filter = self.additional_info[0]
            case 'date':
                try:
                    time_obj = datetime.strptime(self.additional_info[0], '%Y%m%d')
                    delta = timedelta(minutes=self.additional_info[1])
                    self.filter = time_obj, time_obj + delta
                except ValueError:
                    raise err.ShipRadarFilterError('Wrong time format')
            case 'coords':
                x1, y1, x2, y2 = self.additional_info[0], self.additional_info[1], \
                                 self.additional_info[2], self.additional_info[3]
                self.filter = range(x1, x2), range(y1, y2)
            case _:
                raise err.ShipRadarFilterError('Filter type does not exist')


class ShipRadarCSVReader:
    def __init__(self, file: str):
        self.file = file

    def parse(self, filter_obj: ShipRadarFilter):
        collector = []
        if (filter_obj.type is None) or (filter_obj.filter is None):
            # Check if Filter's fields are filled
            raise err.ShipRadarFilterError('Filter not initialized')
        with open(self.file, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            for ind, row in enumerate(csvreader):
                # print(row)
                # if not ind:
                #     continue  # First row is headers - TODO validate headers of csv
                match filter_obj.type:
                    case 'ship_name':
                        if row["ship"] != filter_obj.filter:
                            continue
                        else:
                            collector.append(row)
                    case 'date':
                        row_date = datetime.strptime(row["date"], '%Y%m%d%H%M')
                        if not (filter_obj.filter[0] <= row_date <= filter_obj.filter[1]):
                            continue
                        else:
                            collector.append(row)
                    case 'coords':
                        x, y = int(row["location"].split('y')[0][1:]), int(row["location"].split('y')[1])
                        if not ((x in filter_obj.filter[0]) and (y in filter_obj.filter[1])):
                            continue
                        else:
                            collector.append(row)
                    case _:
                        raise err.ShipRadarBaseException('Unknown error')

        if not collector:
            raise err.ShipRadarFilterError(f'No entries for this filter: {filter_obj.type}: {filter_obj.filter}')

        return collector
