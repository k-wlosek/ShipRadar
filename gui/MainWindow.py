import flet

import src.err
from src.logger import ShipRadarLogger
from src.reader import ShipRadarCSVReader


# Main window, has a file picker, a button to open filters window and a go button which opens another window
class MainWindow(flet.Row):
    def __init__(self, page: flet.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = ShipRadarLogger("MainWindow")
        self.logger.debug("Initializing MainWindow")
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
                                        f"Selected filter {self.filter}" if self.filter else "Open filters window"
                                    ),
                                    on_click=lambda _: self.page.go("/filters")
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
        self.page.update()

    def file_picker_result(self, e: flet.FilePickerResultEvent):
        self.logger.debug(e.files)

        file = e.files[0] if e.files else None
        if file:
            self.files.append(file)

        try:
            self.last_picked_file = self.files[-1]
        except IndexError:
            self.last_picked_file = None
        self.logger.info(self.last_picked_file)
        self.picker_text.value = f"Selected file: {self.last_picked_file.name}" if self.last_picked_file else \
                                 "Select a CSV file to open"
        self.page.update()
        self.controls_view.update()

    def open_canvas_window(self, e) -> None:
        # TODO: verify filters, datafile and all
        self.logger.debug("Opening canvas window")

        try:
            data_file = ShipRadarCSVReader(self.last_picked_file.path)
        except AttributeError:
            self.logger.error("No file selected")
            self.page.snack_bar = flet.SnackBar(content=flet.Text("No file selected!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        # Confirmed that a file is selected, now check if headers are correct
        if not ShipRadarCSVReader.verify_headers(self.last_picked_file.path):
            self.logger.error("Invalid CSV header")
            self.page.snack_bar = flet.SnackBar(content=flet.Text("Invalid CSV file!"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        filter_types: list[str] = ['name_filter', 'datetime_filter', 'location_filter', 'ship_no',
                                   'ship_type_filter', 'move_status_filter', 'heading_filter', 'draught_filter',
                                   'speed_filter', 'destination_filter', 'eta_filter']
        data_list: list[list[dict[str, str]]] = []
        for filter_type in filter_types:
            filter = self.page.session.get(filter_type)
            if filter:
                try:
                    data_list.append(data_file.parse(filter))
                except src.err.ShipRadarFilterError:
                    self.logger.error(f"No entries for {filter_type}")
                    self.page.snack_bar = flet.SnackBar(content=flet.Text(f"No entries for selected filter(s)"))
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
        try:
            data: list[dict] = ShipRadarCSVReader.and_collectors(data_list)
        except IndexError:
            self.logger.error("No filters selected")
            self.page.snack_bar = flet.SnackBar(content=flet.Text("No filters selected!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not data:
            self.logger.error("No data satisfying all filters")
            self.page.snack_bar = flet.SnackBar(content=flet.Text("No data satisfying all filters!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        data_list: list[list[dict]] = ShipRadarCSVReader.divide_collectors(data)

        self.page.session.set("filter", data_list)
        self.page.go("/canvas")
