from gui.MainWindow import MainWindow
from gui.FilterWindow import FilterWindow
from gui.Filters import NameFilter, DateTimeFilter, LocationFilter
from flet import app
import flet
import logging
# logging.basicConfig(level=logging.DEBUG)


class ShipRadarApp(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.page = page
        self.page.title = "ShipRadar"
        self.page.update()

    def build(self):
        self.layout = MainWindow(
            self.page,
            tight=True,
            expand=True
        )
        return self.layout.active_view

    def initialize(self):
        # self.page.add(self.layout)
        self.page.views.clear()
        self.page.views.append(
            flet.View(
                "/",
                [self.layout.active_view],
                padding=flet.padding.all(0)
            )
        )
        self.page.update()
        self.page.go("/")

    def route_change(self, e):
        self.page.views.clear()
        troute = flet.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.views.append(
                flet.View(
                    "/",
                    [self.layout.active_view],
                    padding=flet.padding.all(0)
                )
            )
        if troute.match("/filters"):
            self.filter = FilterWindow(self.page)
            self.page.views.append(
                flet.View(
                    "/filters",
                    [flet.IconButton(
                        icon=flet.icons.HOME, tooltip="Go back", on_click=lambda _: self.page.go("/")
                    ),
                     self.filter]
                )
            )
        if troute.match("/filters/shipname"):
            self.filter_name = NameFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shipname",
                    [flet.IconButton(
                        icon=flet.icons.HOME, tooltip="Go back", on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/shiptime"):
            self.filter_name = DateTimeFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shiptime",
                    [flet.IconButton(
                        icon=flet.icons.HOME, tooltip="Go back", on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/shiplocation"):
            self.filter_name = LocationFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shiplocation",
                    [flet.IconButton(
                        icon=flet.icons.HOME, tooltip="Go back", on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )

        self.page.update()

    def view_pop(self, e):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


def main(page):
    app = ShipRadarApp(page=page)
    page.add(app)
    page.update()
    page.on_route_change = app.route_change
    page.on_view_pop = app.view_pop
    page.go(page.route)
    app.initialize()

# Run the app
app(target=main)
