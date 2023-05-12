import flet
from src.logger import ShipRadarLogger


# Main window, has a file picker, a button to open filters window and a go button which opens another window
class MainWindow(flet.Row):
    def __init__(self, page: flet.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = ShipRadarLogger("MainWindow")
        self.page = page

        self.files = []
        self.last_picked_file = None
        pick_files_dialog = flet.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(pick_files_dialog)
        self.picker_text = flet.Text(f"Select a CSV file to open")

        self.filter = None

        self.controls_view = flet.Column(
            [
                flet.Column(
                    [
                        flet.Card(
                            content=flet.Container(
                                content=flet.ListTile(
                                    leading=flet.Icon(flet.icons.ATTACH_FILE_OUTLINED),
                                    title=flet.Text("Select data file"),
                                    subtitle=self.picker_text,
                                    on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["csv"]),
                                )
                            ),
                        ),
                        flet.Card(
                            content=flet.Container(
                                content=flet.ListTile(
                                    leading=flet.Icon(flet.icons.FILTER_LIST_OUTLINED),
                                    title=flet.Text("Filters"),
                                    subtitle=flet.Text(
                                        f"Selected filter {self.filter}" if self.filter else "Open filters window"),
                                    on_click=self.open_filters_window
                                )
                            )
                        )
                    ]
                ),

                flet.Row(
                    [
                        flet.ElevatedButton(
                            text="Go", on_click=self.open_canvas_window
                        )
                    ]
                )
            ]
        )
        self._active_view: flet.Control = self.controls_view

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, value: flet.Control):
        self._active_view = value
        self.update()

    def file_picker_result(self, e: flet.FilePickerResultEvent):
        self.logger.debug(e.files)

        file = e.files[0] if e.files else None
        if file:
            self.files.append(file)
        self.last_picked_file = self.files[-1].name
        self.logger.info(self.last_picked_file)
        self.picker_text.value = f"Selected file: {self.last_picked_file}" if self.last_picked_file else \
                                 "Select a CSV file to open"
        self.page.update()
        self.controls_view.update()

    def open_filters_window(self, e):
        self.open_filters_window = None

    def open_canvas_window(self, e):
        self.open_canvas_window = None
