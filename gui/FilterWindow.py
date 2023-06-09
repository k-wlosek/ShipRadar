"""
Contains the FilterWindow class, which is a window that allows the user to filter the data
"""

import flet


class FilterWindow(flet.UserControl):
    """
    A window that allows the user to filter the data.
    """

    def __init__(self, page: flet.Page):
        super().__init__()
        self.layout = None
        self.page = page
        self.page.title = "Filters"
        self.page.update()

        self.none_selected = flet.Row(
            [
                flet.Icon(flet.icons.NOT_INTERESTED, tooltip="Not selected")
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

    def build(self):
        """
        Builds the filter window.
        :return: The filter window view
        """
        self.layout = flet.Column(
            [
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.DRIVE_FILE_RENAME_OUTLINE_SHARP),
                                    title=flet.Text("Ship name"),
                                    subtitle=flet.Text(
                                        "Filter by ship name"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shipname")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(f"Selected ship name: "
                                                  f"{self.page.session.get('name_filter').filter}"
                                                  ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('name_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('name_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.HOURGLASS_FULL_ROUNDED),
                                    title=flet.Text("Date and time"),
                                    subtitle=flet.Text(
                                        "Filter by time"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shiptime")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected datetime: "
                                            f"{self.page.session.get('datetime_filter').filter[0]}\n"
                                            f"{self.page.session.get('datetime_filter').filter[1]}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('datetime_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('datetime_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.LOCATION_PIN),
                                    title=flet.Text("Location"),
                                    subtitle=flet.Text(
                                        "Filter by location"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shiplocation")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected location: "
                                            f"{self.page.session.get('location_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('location_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('location_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.NUMBERS_ROUNDED),
                                    title=flet.Text("LRIMO ship number"),
                                    subtitle=flet.Text(
                                        "Filter by ship number"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shipnumber")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected ship number: "
                                            f"{self.page.session.get('ship_no_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('ship_no_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('ship_no_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.TYPE_SPECIMEN_ROUNDED),
                                    title=flet.Text("Type"),
                                    subtitle=flet.Text(
                                        "Filter by ship type"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shiptype")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected type: "
                                            f"{self.page.session.get('ship_type_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('ship_type_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('ship_type_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.MOVING_ROUNDED),
                                    title=flet.Text("Movement status"),
                                    subtitle=flet.Text(
                                        "Filter by ship's movement status"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/shipmovestatus")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected move status: "
                                            f"{self.page.session.get('move_status_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('move_status_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('move_status_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.COMPASS_CALIBRATION_ROUNDED),
                                    title=flet.Text("Heading"),
                                    subtitle=flet.Text(
                                        "Filter by ship's heading"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/heading")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected heading: "
                                            f"{self.page.session.get('heading_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=self.reset_filters('heading_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('heading_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.ANCHOR_ROUNDED),
                                    title=flet.Text("Draught"),
                                    subtitle=flet.Text(
                                        "Filter by ship's draught"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/draught")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected draught: "
                                            f"{self.page.session.get('draught_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('draught_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('draught_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.SPEED_ROUNDED),
                                    title=flet.Text("Speed"),
                                    subtitle=flet.Text(
                                        "Filter by ship's speed"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/speed")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected speed: "
                                            f"{self.page.session.get('speed_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('speed_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('speed_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.MAP_ROUNDED),
                                    title=flet.Text("Destination"),
                                    subtitle=flet.Text(
                                        "Filter by ship's destination"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/destination")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected destination: "
                                            f"{self.page.session.get('destination_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('destination_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('destination_filter') else self.none_selected
                            ]
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.Column(
                            [
                                flet.ListTile(
                                    leading=flet.Icon(flet.icons.WATCH_ROUNDED),
                                    title=flet.Text("ETA"),
                                    subtitle=flet.Text(
                                        "Filter by ship's ETA"
                                    ),
                                    on_click=lambda _: self.page.go("/filters/eta")
                                ),
                                flet.Row(
                                    [
                                        flet.Text(
                                            f"Selected ETA: "
                                            f"{self.page.session.get('eta_filter').filter}"
                                        ),
                                        flet.IconButton(icon=flet.icons.DELETE,
                                                        icon_color="pink600",
                                                        on_click=lambda _: self.reset_filters('eta_filter'))
                                    ], alignment=flet.MainAxisAlignment.END
                                ) if self.page.session.get('eta_filter') else self.none_selected
                            ]
                        )
                    )
                )
            ]
        )
        return self.layout

    def reset_filters(self, filter_name: str) -> None:
        """
        Resets the filter
        :param filter_name: Filter to reset
        :return: None
        """
        self.page.session.set(filter_name, None)
        self.page.update()
        self.layout.update()

        self.page.go("/")
        self.page.go("/filters")  # I might not like this, but it works
