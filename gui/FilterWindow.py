import flet


class FilterWindow(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.page = page
        self.page.title = "Filters"
        self.page.update()

    def build(self):
        self.layout = flet.Column(
            [
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.DRIVE_FILE_RENAME_OUTLINE_SHARP),
                            title=flet.Text("Ship name"),
                            subtitle=flet.Text(
                                f"Filter by ship name"),
                            on_click=lambda _: self.page.go("/filters/shipname")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.HOURGLASS_FULL_ROUNDED),
                            title=flet.Text("Date and time"),
                            subtitle=flet.Text(
                                f"Filter by time"),
                            on_click=lambda _: self.page.go("/filters/shiptime")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.LOCATION_PIN),
                            title=flet.Text("Location"),
                            subtitle=flet.Text(
                                f"Filter by location"),
                            on_click=lambda _: self.page.go("/filters/shiplocation")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.NUMBERS_ROUNDED),
                            title=flet.Text("LRIMO ship number"),
                            subtitle=flet.Text(
                                f"Filter by ship number"),
                            on_click=lambda _: self.page.go("/filters/shipnumber")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.TYPE_SPECIMEN_ROUNDED),
                            title=flet.Text("Type"),
                            subtitle=flet.Text(
                                f"Filter by ship type"),
                            on_click=lambda _: self.page.go("/filters/shiptype")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.MOVING_ROUNDED),
                            title=flet.Text("Movement status"),
                            subtitle=flet.Text(
                                f"Filter by ship's movement status"),
                            on_click=lambda _: self.page.go("/filters/shipmovestatus")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.COMPASS_CALIBRATION_ROUNDED),
                            title=flet.Text("Heading"),
                            subtitle=flet.Text(
                                f"Filter by ship's heading"),
                            on_click=lambda _: self.page.go("/filters/heading")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.ANCHOR_ROUNDED),
                            title=flet.Text("Draught"),
                            subtitle=flet.Text(
                                f"Filter by ship's draught"),
                            on_click=lambda _: self.page.go("/filters/draught")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.SPEED_ROUNDED),
                            title=flet.Text("Speed"),
                            subtitle=flet.Text(
                                f"Filter by ship's speed"),
                            on_click=lambda _: self.page.go("/filters/speed")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.MAP_ROUNDED),
                            title=flet.Text("Destination"),
                            subtitle=flet.Text(
                                f"Filter by ship's destination"),
                            on_click=lambda _: self.page.go("/filters/destination")
                        )
                    )
                ),
                flet.Card(
                    content=flet.Container(
                        content=flet.ListTile(
                            leading=flet.Icon(flet.icons.WATCH_ROUNDED),
                            title=flet.Text("ETA"),
                            subtitle=flet.Text(
                                f"Filter by ship's ETA"),
                            on_click=lambda _: self.page.go("/filters/eta")
                        )
                    )
                )
            ]
        )
        return self.layout




