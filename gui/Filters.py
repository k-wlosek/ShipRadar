"""
Contains the filters for the GUI
"""

from datetime import datetime
import flet
from beartype.typing import Union
from imports.datetime_field import DatetimeField
from src.logger import ShipRadarLogger
from src.reader import ShipRadarFilter


class NameFilter(flet.UserControl):
    """
    Filter by ship name
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("NameFilter")
        self.page = page
        self.page.title = "Filter: Ship name"
        self.text_field = flet.TextField(label="Ship name", keyboard_type=flet.KeyboardType.TEXT,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship name"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(self.text_field.value)
        self.filter: ShipRadarFilter = ShipRadarFilter('ship_name', self.text_field.value.upper())
        self.page.session.set('name_filter', self.filter)
        self.page.go("/filters")


class DateTimeFilter(flet.UserControl):
    """
    Filter by date and time
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("DateTimeFilter")
        self.page = page
        self.page.title = "Filter: Date and time"
        self.from_datetime_field = DatetimeField(page=self.page)
        self.till_datetime_field = DatetimeField(page=self.page)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by date and time"),
                self.from_datetime_field,
                self.till_datetime_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.from_datetime_field.value=} {self.till_datetime_field.value=}")
        # Check if either value is a list, meaning there's a problem with said value
        if isinstance(self.from_datetime_field.value, list):
            # If all values in list are str then it's a problem with the date
            self.logger.debug("Problem with from date, probably invalid date")
            if all(isinstance(x, str) for x in self.from_datetime_field.value):
                self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid 1st date"))
                self.page.snack_bar.open = True
                self.page.update()
                return None
        if isinstance(self.till_datetime_field.value, list):
            self.logger.debug("Problem with till date, probably invalid date")
            if all(isinstance(x, str) for x in self.till_datetime_field.value):
                self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid 2nd date"))
                self.page.snack_bar.open = True
                self.page.update()
                return None
        if isinstance(self.from_datetime_field.value, datetime) and \
                isinstance(self.till_datetime_field.value, datetime):
            # All fields are filled
            self.filter = ShipRadarFilter('date',
                                          self.from_datetime_field.value,
                                          self.till_datetime_field.value
                                          )
            self.page.session.set('datetime_filter', self.filter)
            self.page.go("/filters")
            return None
        # Not all fields are filled
        self.page.snack_bar = flet.SnackBar(
            content=flet.Text("Please fill all fields")
        )
        self.page.snack_bar.open = True
        self.page.update()
        return None


class LocationFilter(flet.UserControl):
    """
    Filter by location
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("LocationFilter")
        self.page = page
        self.page.title = "Filter: Location"
        self.x1 = flet.TextField(label="From longitude", keyboard_type=flet.KeyboardType.NUMBER, width=100,
                                 text_align=flet.TextAlign.CENTER)
        self.y1 = flet.TextField(label="From latitude", keyboard_type=flet.KeyboardType.NUMBER, width=100,
                                 text_align=flet.TextAlign.CENTER)
        self.x2 = flet.TextField(label="To longitude", keyboard_type=flet.KeyboardType.NUMBER, width=100,
                                 text_align=flet.TextAlign.CENTER)
        self.y2 = flet.TextField(label="To latitude", keyboard_type=flet.KeyboardType.NUMBER, width=100,
                                 text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship name"),
                flet.Row(
                        [
                            self.x1, self.y1, self.x2, self.y2
                        ]
                    ),
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.x1.value=} {self.y1.value=} {self.x2.value=} {self.y2.value=}")
        try:
            self.x1.value = float(self.x1.value)
            self.y1.value = float(self.y1.value)
            self.x2.value = float(self.x2.value)
            self.y2.value = float(self.y2.value)
        except ValueError:
            self.page.snack_bar = flet.SnackBar(
                content=flet.Text("Invalid coordinates")
            )
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.filter = ShipRadarFilter('coords',
                                      self.x1.value,
                                      self.y1.value,
                                      self.x2.value,
                                      self.y2.value
                                      )
        self.page.session.set('location_filter', self.filter)
        self.page.go("/filters")
        return None


class ShipNoFilter(flet.UserControl):
    """
    Filter by ship number
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("ShipNoFilter")
        self.page = page
        self.page.title = "Filter: Ship number"
        self.text_field = flet.TextField(label="Ship number", keyboard_type=flet.KeyboardType.NUMBER,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship number"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        try:
            self.text_field.value = int(self.text_field.value)
        except ValueError:
            self.page.snack_bar = flet.SnackBar(
                content=flet.Text("Invalid ship number")
            )
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.filter = ShipRadarFilter('ship_no', self.text_field.value)
        self.page.session.set('ship_no_filter', self.filter)
        self.page.go("/filters")
        return None


class ShipTypeFilter(flet.UserControl):
    """
    Filter by ship type
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("ShipTypeFilter")
        self.page = page
        self.page.title = "Filter: Ship type"
        self.text_field = flet.TextField(label="Ship type", keyboard_type=flet.KeyboardType.TEXT,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship type"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        self.filter = ShipRadarFilter('ship_type', self.text_field.value)
        self.page.session.set('ship_type_filter', self.filter)
        self.page.go("/filters")


class MoveStatusFilter(flet.UserControl):
    """
    Filter by move status
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("MoveStatusFilter")
        self.page = page
        self.page.title = "Filter: Move type"
        self.text_field = flet.TextField(label="Move type", keyboard_type=flet.KeyboardType.TEXT,
                                         text_align=flet.TextAlign.CENTER)

    def build(self):
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by move type"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        self.filter = ShipRadarFilter('move_status', self.text_field.value)
        self.page.session.set('move_status_filter', self.filter)
        self.page.go("/filters")


class HeadingFilter(flet.UserControl):
    """
    Filter by heading
    """
    def __init__(self, page: flet.UserControl):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("HeadingFilter")
        self.page = page
        self.page.title = "Filter: Heading"
        self.text_field = flet.TextField(label="Heading", keyboard_type=flet.KeyboardType.NUMBER,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by heading"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        try:
            self.text_field.value = int(self.text_field.value)
        except ValueError:
            self.page.snack_bar = flet.SnackBar(
                content=flet.Text("Invalid heading")
            )
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.filter = ShipRadarFilter('heading', self.text_field.value)
        self.page.session.set('heading_filter', self.filter)
        self.page.go("/filters")
        return None


class DraughtFilter(flet.UserControl):
    """
    Filter by draught
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("DraughtFilter")
        self.page = page
        self.page.title = "Filter: Draught"
        self.text_field = flet.TextField(label="Draught", keyboard_type=flet.KeyboardType.NUMBER,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by draught"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        try:
            self.text_field.value = float(self.text_field.value)
        except ValueError:
            self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid draught"))
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.filter = ShipRadarFilter('draught', self.text_field.value)
        self.page.session.set('draught_filter', self.filter)
        self.page.go("/filters")
        return None


class SpeedFilter(flet.UserControl):
    """
    Filter by speed
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("SpeedFilter")
        self.page = page
        self.page.title = "Filter: Speed"
        self.text_field = flet.TextField(label="Speed", keyboard_type=flet.KeyboardType.NUMBER,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by speed"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        try:
            self.text_field.value = float(self.text_field.value)
        except ValueError:
            self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid speed"))
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.filter = ShipRadarFilter('speed', self.text_field.value)
        self.page.session.set('speed_filter', self.filter)
        self.page.go("/filters")
        return None


class DestinationFilter(flet.UserControl):
    """
    Filter by destination
    """
    def __init__(self, page: flet.UserControl):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("DestinationFilter")
        self.page = page
        self.page.title = "Filter: Destination"
        self.text_field = flet.TextField(label="Destination", keyboard_type=flet.KeyboardType.TEXT,
                                         text_align=flet.TextAlign.CENTER)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by destination"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.text_field.value=}")
        self.filter = ShipRadarFilter('destination', self.text_field.value.upper())
        self.page.session.set('destination_filter', self.filter)
        self.page.go("/filters")


class ETAFilter(flet.UserControl):
    """
    Filter by ETA
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter: Union[None, ShipRadarFilter] = None
        self.layout: Union[None, flet.Control] = None
        self.logger = ShipRadarLogger("ETAFilter")
        self.page = page
        self.page.title = "Filter: ETA"
        self.datetime_field = DatetimeField(page=self.page)

    def build(self) -> flet.Control:
        """
        Build the filter layout
        :return: The filter layout
        """
        self.layout = flet.Column(
            [
                flet.Text("Filter by ETA"),
                self.datetime_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e: flet.TapEvent) -> None:
        """
        Submit the filter
        :param e: Click event
        :return: None
        """
        self.logger.debug(f"{self.datetime_field.value=}")
        if isinstance(self.datetime_field.value, list):
            # If all values in list are str then it's a problem with the date
            self.logger.debug("Problem with from date, probably invalid date")
            if all(isinstance(x, str) for x in self.datetime_field.value):
                self.page.snack_bar = flet.SnackBar(
                    content=flet.Text("Invalid date")
                )
                self.page.snack_bar.open = True
                self.page.update()
                return None
        if isinstance(self.datetime_field.value, datetime):
            # All fields are filled
            self.filter = ShipRadarFilter('eta', self.datetime_field.value)
            self.page.session.set('eta_filter', self.filter)
            self.page.go("/filters")
            return None
        # Not all fields are filled
        self.page.snack_bar = flet.SnackBar(
            content=flet.Text("Please fill all fields")
        )
        self.page.snack_bar.open = True
        self.page.update()
        return None
