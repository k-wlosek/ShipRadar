import src.err as err
import src.logger as logger
import csv
from datetime import datetime


class ShipRadarFilter:
    type = None
    filter = None

    def __init__(self, type: str, *args):
        self.logger = logger.ShipRadarLogger("ShipRadarFilterLogger")
        self.filter = None
        self.type: str = type
        self.additional_info: tuple = args
        self.__parse_type()

    def __parse_type(self) -> None:
        """
        Parses the type of the filter and sets the filter accordingly.
        :return: None
        """
        match self.type:
            case 'ship_no':
                self.filter: int = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'ship_type':
                self.filter: str = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'move_status':
                self.filter: str = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'heading':
                self.filter: int = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'draught':
                self.filter: float = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'speed':
                self.filter: float = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'destination':
                self.filter: str = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'eta':
                self.filter: datetime = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'ship_name':
                self.filter: str = self.additional_info[0]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case 'date':
                try:
                    # Get date as 2 datetime objects, from and till
                    # delta = timedelta(minutes=self.additional_info[1])
                    self.filter: tuple[datetime, datetime] = self.additional_info[0], self.additional_info[1]
                    self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
                except ValueError as exc:
                    self.logger.debug(f"Date filter exception: {exc}\nFilterError raised.")
                    raise err.ShipRadarFilterError('Wrong time format')
            case 'coords':  # TODO Split into 2 filters, one for longitude and one for latitude OR NOT?
                # longitude1, latitude1, logitude2, latitude2
                self.filter: tuple[float, float, float, float] = self.additional_info[0], \
                    self.additional_info[1], self.additional_info[2], self.additional_info[3]
                self.logger.debug(f"Filter set for {self.type} with filter {self.filter}")
            case _:
                self.logger.debug(f"Filter type does not exist.\nFilterError raised.")
                raise err.ShipRadarFilterError('Filter type does not exist')


class ShipRadarCSVReader:
    def __init__(self, file: str):
        self.logger = logger.ShipRadarLogger("CSVReaderLogger")
        self.file = file

    def parse(self, filter_obj: ShipRadarFilter):
        """
        Parses CSV file with given filter
        :param filter_obj: ShipRadarFilter object
        :return: collector: list of dicts satisfying filter
        """
        self.logger.debug(f"Parsing CSV file with filter {filter_obj} started")
        collector = []
        if (filter_obj.type is None) or (filter_obj.filter is None):
            # Check if Filter's fields are filled
            self.logger.debug(f"Filter has not been initialized.\nFilterError raised.")
            raise err.ShipRadarFilterError('Filter not initialized')
        try:
            with open(self.file, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=';')
                for ind, row in enumerate(csvreader):

                    if ind == 0:
                        # Header validation
                        self.logger.debug(f"Header validation started")
                        for key in row.keys():
                            if key not in ["LRIMOShipNo", "ShipName", "ShipType", "MovementDateTime",
                                           "Longitude", "Latitude", "MoveStatus", "Heading", "Draught",
                                           "Speed", "Destination", "ETA"]:
                                self.logger.debug(f"Header validation failed.\nImportError raised.")
                                raise err.ShipRadarImportError('Wrong header in CSV file')
                        self.logger.debug(f"Header validation passed")

                    # Filtering
                    match filter_obj.type:
                        case 'ship_no':
                            if int(row["LRIMOShipNo"]) != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'ship_type':
                            if row["ShipType"] != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'move_status':
                            if row["MoveStatus"] != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'heading':
                            if int(row["Heading"]) != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'draught':
                            # Ensure that the decimal separator is a dot
                            if float(row["Draught"].replace(",", ".")) != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'speed':
                            # Ensure that the decimal separator is a dot
                            if float(row["Speed"].replace(",", ".")) != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'destination':
                            if row["Destination"] != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'eta':
                            if datetime.fromisoformat(row["ETA"]) != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'ship_name':
                            if row["ShipName"] != filter_obj.filter:
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'date':
                            # Filter is a tuple of 2 datetime objects, from and till
                            row_date = datetime.fromisoformat(row["MovementDateTime"])
                            if not (filter_obj.filter[0] <= row_date <= filter_obj.filter[1]):
                                self.logger.verbose(f"Row {row} NOT ADDED")
                                continue
                            else:
                                self.logger.verbose(f"Row {row} ADDED")
                                collector.append(row)

                        case 'coords':
                            # Filter is a tuple of 4 floats, longitude1, latitude1, longitude2, latitude2
                            x, y = float(row["Longitude"]), float(row["Latitude"])
                            if not (((filter_obj.filter[0] <= x <= filter_obj.filter[2])
                                    or (filter_obj.filter[2] <= x <= filter_obj.filter[0]))
                                    and
                                    ((filter_obj.filter[1] <= y <= filter_obj.filter[3])
                                     or (filter_obj.filter[3] <= y <= filter_obj.filter[1]))):
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
    def and_collectors(collectors: list[list[dict[str, str]]]) -> list[dict[str, str]]:
        """
        Returns a list of a logical AND of collectors
        :return: List of ship satisfying all filters from individual collectors
        :rtype: list
        """
        if not collectors:
            return []

        result = set(tuple(ship.items()) for ship in collectors[0])
        for collector in collectors[1:]:
            result = result.intersection(set(tuple(ship.items()) for ship in collector))

        return [dict(items) for items in result]

    @staticmethod
    def divide_collectors(collector: list[dict]) -> list[list[dict]]:
        """
        Divide collector into multiple collectors, by ship name
        :param collector: collector, returned by reader.ShipRadarCSVReader.and_collector(collectors)
        :return: list of collectors, each collector contains only ships with same name
        """
        divided_collectors = []
        for item in collector:
            no_value = item["ShipName"]
            found = False
            for sublist in divided_collectors:
                if sublist[0]["ShipName"] == no_value:
                    sublist.append(item)
                    found = True
                    break
            if not found:
                divided_collectors.append([item])

        return divided_collectors

    @staticmethod
    def verify_headers(filepath: str) -> bool:
        with open(filepath) as file:
            reader = csv.reader(file, delimiter=";")
            header = next(reader)
            if set(header) != {"LRIMOShipNo", "ShipName", "ShipType", "MovementDateTime", "Latitude", "Longitude",
                               "MoveStatus", "Heading", "Draught", "Speed", "Destination", "ETA"}:
                return False
        return True
