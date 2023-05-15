import flet
from imports.datetime_field import DatetimeField
from datetime import datetime
from src.logger import ShipRadarLogger
from src.reader import ShipRadarFilter


class NameFilter(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.logger = ShipRadarLogger("NameFilter")
        self.page = page
        self.page.title = "Filter: Ship name"
        self.text_field = flet.TextField(label="Ship name")

    def build(self):
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship name"),
                self.text_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e):
        self.logger.debug(self.text_field.value)
        self.filter = ShipRadarFilter('ship_name', self.text_field.value)
        self.page.session.set('name_filter', self.filter)
        self.page.go("/filters")


class DateTimeFilter(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.logger = ShipRadarLogger("DateTimeFilter")
        self.page = page
        self.page.title = "Filter: Date and time"
        self.from_datetime_field = DatetimeField(page=self.page)
        self.till_datetime_field = DatetimeField(page=self.page)

    def build(self):
        self.layout = flet.Column(
            [
                flet.Text("Filter by date and time"),
                self.from_datetime_field,
                self.till_datetime_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e) -> None:
        self.logger.debug(f"{self.from_datetime_field.value=} {self.till_datetime_field.value=}")
        # Check if either value is a list, meaning there's a problem with said value
        if isinstance(self.from_datetime_field.value, list):
            # If all values in list are str then it's a problem with the date
            self.logger.debug("Problem with from date, probably invalid date")
            if all(isinstance(x, str) for x in self.from_datetime_field.value):
                self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid from date"))
                self.page.snack_bar.open = True
                self.page.update()
                return None
        if isinstance(self.till_datetime_field.value, list):
            self.logger.debug("Problem with till date, probably invalid date")
            if all(isinstance(x, str) for x in self.till_datetime_field.value):
                self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid till date"))
                self.page.snack_bar.open = True
                self.page.update()
                return None
        if isinstance(self.from_datetime_field.value, datetime) and \
                isinstance(self.till_datetime_field.value, datetime):
            # All fields are filled
            self.filter = ShipRadarFilter('date', self.from_datetime_field.value, self.till_datetime_field.value)
            self.page.session.set('datetime_filter', self.filter)
            self.page.go("/filters")
        else:
            # Not all fields are filled
            self.page.snack_bar = flet.SnackBar(content=flet.Text("Please fill all fields"))
            self.page.snack_bar.open = True
            self.page.update()
            return None


class LocationFilter(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.logger = ShipRadarLogger("LocationFilter")
        self.page = page
        self.page.title = "Filter: Location"
        self.x1 = flet.TextField(label="x1", keyboard_type=flet.KeyboardType.NUMBER)
        self.y1 = flet.TextField(label="y1", keyboard_type=flet.KeyboardType.NUMBER)
        self.x2 = flet.TextField(label="x2", keyboard_type=flet.KeyboardType.NUMBER)
        self.y2 = flet.TextField(label="y2", keyboard_type=flet.KeyboardType.NUMBER)

    def build(self):
        self.layout = flet.Column(
            [
                flet.Text("Filter by ship name"),
                flet.Container(
                    content=flet.GridView(
                        controls=[
                            self.x1, self.y1, self.x2, self.y2
                        ],
                        spacing=5, expand=1, run_spacing=5
                    )
                ),
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e):
        self.logger.debug(self.text_field.value)
        self.filter = ShipRadarFilter('ship_name', self.text_field.value)
        self.page.session.set('name_filter', self.filter)
        self.page.go("/filters")