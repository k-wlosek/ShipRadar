"""
Contains the main application class for the ShipRadar app.
"""

import flet
from gui.PlotWindow import Plot
from gui.MainWindow import MainWindow
from gui.FilterWindow import FilterWindow
from gui.Filters import NameFilter, DateTimeFilter, LocationFilter, ShipNoFilter, ShipTypeFilter, \
    MoveStatusFilter, HeadingFilter, DraughtFilter, SpeedFilter, DestinationFilter, ETAFilter


class ShipRadarApp(flet.UserControl):
    """
    The main application class for the ShipRadar app.
    """
    def __init__(self, page: flet.Page):
        super().__init__()
        self.filter_name = None
        self.plot = None
        self.filter = None
        self.layout = None
        self.page = page
        self.page.title = "ShipRadar"
        self.page.session.set('filter', None)
        self.page.update()

    def build(self) -> flet.Control:
        """
        Builds the main application.
        :return: The main application view
        """
        self.layout = MainWindow(
            self.page,
            tight=True,
            expand=True
        )
        return self.layout.active_view

    def route_change(self, e: flet.RouteChangeEvent) -> None:
        """
        Handles route changes.
        :param e: Route change event
        :return: None
        """
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
                        icon=flet.icons.HOME,
                        tooltip="Go to main screen",
                        on_click=lambda _: self.page.go("/")
                    ),
                     self.filter],
                    scroll=flet.ScrollMode.ADAPTIVE
                )
            )
        if troute.match("/filters/shipname"):
            self.filter_name = NameFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shipname",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
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
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
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
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _:
                        self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/shipnumber"):
            self.filter_name = ShipNoFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shipnumber",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/shiptype"):
            self.filter_name = ShipTypeFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shiptype",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/shipmovestatus"):
            self.filter_name = MoveStatusFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/shipmovestatus",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/heading"):
            self.filter_name = HeadingFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/heading",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/draught"):
            self.filter_name = DraughtFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/draught",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/speed"):
            self.filter_name = SpeedFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/speed",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/destination"):
            self.filter_name = DestinationFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/destination",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/filters/eta"):
            self.filter_name = ETAFilter(self.page)
            self.page.views.append(
                flet.View(
                    "/filters/eta",
                    [flet.IconButton(
                        icon=flet.icons.ARROW_BACK,
                        tooltip="Go back",
                        on_click=lambda _: self.page.go("/filters")
                    ),
                     self.filter_name]
                )
            )
        if troute.match("/plot"):
            self.plot = Plot(self.page, self.page.session.get('filter'), "Plot")
            self.page.views.append(
                flet.View(
                    "/plot",
                    [flet.IconButton(
                        icon=flet.icons.HOME,
                        tooltip="Go to main screen",
                        on_click=lambda _: self.page.go("/")
                    ),
                     self.plot]
                )
            )
        self.page.update()

    def view_pop(self, e: flet.ViewPopEvent) -> None:
        """
        Go back to the previous view
        :param e: Pop event
        :return: None
        """
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
