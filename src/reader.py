import src.err as err
import src.logger as logger
import csv
from datetime import datetime, timedelta


class ShipRadarFilter:
    type = None
    filter = None

    def __init__(self, type: str, *args):
        self.logger = logger.ShipRadarLogger("ShipRadarFilterLogger")
        self.filter = None
        self.type = type
        self.additional_info = args
        self.__parse_type()

    def __parse_type(self):
        match self.type:
            case 'ship_name':
                self.filter = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'date':
                try:
                    # Get date as YYYYMMDD and offset in minutes for a time range
                    time_obj = datetime.strptime(self.additional_info[0], '%Y%m%d')
                    delta = timedelta(minutes=self.additional_info[1])
                    self.filter = time_obj, time_obj + delta
                    self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
                except ValueError as exc:
                    self.logger.debug(f"Date filter exception: {exc}\nFilterError raised.")
                    raise err.ShipRadarFilterError('Wrong time format')
            case 'coords':
                x1, y1, x2, y2 = self.additional_info[0], self.additional_info[1], \
                                 self.additional_info[2], self.additional_info[3]
                self.filter = range(x1, x2), range(y1, y2)
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case _:
                self.logger.debug(f"Filter type does not exist.\nFilterError raised.")
                raise err.ShipRadarFilterError('Filter type does not exist')


class ShipRadarCSVReader:
    def __init__(self, file: str):
        self.logger = logger.ShipRadarLogger("CSVReaderLogger")
        self.file = file

    def parse(self, filter_obj: ShipRadarFilter):
        self.logger.debug(f"Parsing CSV file with filter {filter_obj} started")
        collector = []
        if (filter_obj.type is None) or (filter_obj.filter is None):
            # Check if Filter's fields are filled
            self.logger.debug(f"Filter has not been initialized.\nFilterError raised.")
            raise err.ShipRadarFilterError('Filter not initialized')
        try:
            with open(self.file, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=',')
                for ind, row in enumerate(csvreader):
                    # print(row)
                    # if not ind:
                    #     continue  # First row is headers - TODO validate headers of csv
                    # TODO up - necessary?
                    match filter_obj.type:
                        case 'ship_name':
                            if row["ship"] != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)
                        case 'date':
                            row_date = datetime.strptime(row["date"], '%Y%m%d%H%M')
                            if not (filter_obj.filter[0] <= row_date <= filter_obj.filter[1]):
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)
                        case 'coords':
                            x, y = int(row["location"].split('y')[0][1:]), int(row["location"].split('y')[1])
                            if not ((x in filter_obj.filter[0]) and (y in filter_obj.filter[1])):
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)
                        case _:
                            self.logger.debug(f"Unknown error occurred")
                            raise err.ShipRadarBaseException('Unknown error')
        except FileNotFoundError:
            self.logger.debug(f"File {self.file} not found.\nImportError raised.")
            raise err.ShipRadarImportError(f"No file {self.file}")

        if not collector:
            self.logger.debug(f"Collector {collector} is empty: No ships for given filter {filter_obj}")
            raise err.ShipRadarFilterError(f'No entries for this filter: {filter_obj.type}: {filter_obj.filter}')

        return collector

    @staticmethod
    def and_collectors(collectors: list):
        """
        Returns a list of a logical AND of collectors
        :return: List of ship satifying all filters from individual collectors
        """
        return list(set.intersection(*map(set, collectors)))
