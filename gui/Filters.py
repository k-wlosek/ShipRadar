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
        self.datetime_field = DatetimeField(page=self.page)

    def build(self):
        self.layout = flet.Column(
            [
                flet.Text("Filter by date and time"),
                self.datetime_field,
                flet.ElevatedButton(text="Submit", on_click=self.submit)
            ]
        )
        return self.layout

    def submit(self, e):
        self.logger.debug(self.datetime_field.value)
        if isinstance(self.datetime_field.value, datetime):
            # All fields are filled
            self.filter = ShipRadarFilter('ship_date', self.datetime_field.value)
            self.filter = ShipRadarFilter('ship_datetime', self.datetime_field.value)
            self.page.session.set('datetime_filter', self.filter)
            self.page.go("/filters")
        else:
            # Not all fields are filled
            self.page.show_snackbar("Please fill all fields")

