import flet


class FilterWindow(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.page = page
        self.page.title = "Filters"

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
                )
            ]
        )
        return self.layout

    def open_filter(self, e):
        ...  # TODO: open filter window



