"""
Contains the MainWindow class, which is the main window of the app.
"""

import os.path
import time
import flet
import src.err
from src.logger import ShipRadarLogger
from src.reader import ShipRadarCSVReader, ShipRadarFilter


class MainWindow(flet.Row):
    """
    Main window of the app. Contains a file picker, a button to open filters window and a go button which opens plot
    """
    def __init__(self, page: flet.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = ShipRadarLogger("MainWindow")
        self.logger.debug("Initializing MainWindow")
        self.page = page

        self.files = []
        self.last_picked_file = None
        self.__pick_files_dialog = flet.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(self.__pick_files_dialog)
        self.__picker_text = flet.Text("Select a CSV file to open")

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
                                    subtitle=self.__picker_text,
                                    on_click=lambda _: self.__pick_files_dialog.pick_files(
                                        allowed_extensions=["csv"]
                                    ),
                                )
                            ),
                        ),
                        flet.Card(
                            content=flet.Container(
                                content=flet.ListTile(
                                    leading=flet.Icon(flet.icons.FILTER_LIST_OUTLINED),
                                    title=flet.Text("Filters"),
                                    subtitle=flet.Text(
                                        f"Selected filter {self.filter}"
                                        if self.filter else
                                        "Open filters window"
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
                            text="Go", on_click=self.open_plot_window
                        )
                    ]
                )
            ]
        )
        self._active_view: flet.Control = self.controls_view

    @property
    def active_view(self) -> flet.Control:
        """
        The active view of the main window.
        :return: Active view
        """
        return self._active_view

    @active_view.setter
    def active_view(self, value: flet.Control) -> None:
        """
        Sets the active view of the main window.
        :param value: view to set
        :return: None
        """
        self._active_view = value
        self.update()
        self.page.update()

    def file_picker_result(self, e: flet.FilePickerResultEvent) -> None:
        """
        Handles the result of the file picker.
        :param e: File picker result event
        :return: None
        """
        self.logger.debug(e.files)

        file = e.files[0] if e.files else None
        if file:
            self.files.append(file)

        try:
            self.last_picked_file = self.files[-1]
        except IndexError:
            self.last_picked_file = None
        self.logger.info(self.last_picked_file)
        self.__picker_text.value = f"Selected file: {self.last_picked_file.name}" \
            if self.last_picked_file else \
            "Select a CSV file to open"
        self.page.update()
        self.controls_view.update()

    def open_plot_window(self, e: flet.TapEvent) -> None:
        """
        Opens the plot window.
        :param e: Click event
        :return: None
        """
        # If app runs in browser, upload file
        if self.page.web:
            self.logger.debug("Running in browser")
            # Check extension
            self.logger.debug("Checking file extension")
            if not self.last_picked_file.name.endswith("csv"):
                self.logger.error("File is not CSV")
                self.page.snack_bar = flet.SnackBar(
                    content=flet.Text("Not a CSV file!")
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.last_picked_file.path = f"uploads/{self.last_picked_file.name}"

            # Upload file
            if not os.path.exists(self.last_picked_file.path):
                self.logger.debug("Uploading file")
                self.page.snack_bar = flet.SnackBar(
                    content=flet.Text("Uploading file...")
                )
                self.page.snack_bar.open = True
                self.page.update()
                self.__pick_files_dialog.upload([flet.FilePickerUploadFile(
                    self.last_picked_file.name,
                    upload_url=self.page.get_upload_url(
                        self.last_picked_file.name, 120  # 2 minutes should be enough
                    )
                )])
                while not os.path.exists(self.last_picked_file.path):
                    time.sleep(1)  # Wait for file to upload
                self.page.snack_bar = flet.SnackBar(
                    content=flet.Text("File uploaded!")
                )
                self.page.snack_bar.open = True
                self.page.update()
                self.logger.debug("File uploaded")
            else:
                self.logger.debug("File already uploaded")

        self.logger.debug("Opening plot window")
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

        filter_types: list[str] = ['name_filter', 'datetime_filter', 'location_filter', 'ship_no_filter',
                                   'ship_type_filter', 'move_status_filter', 'heading_filter',
                                   'draught_filter', 'speed_filter', 'destination_filter', 'eta_filter']
        data_list: list[list[dict[str, str]]] = []
        for filter_type in filter_types:
            filter_obj = self.page.session.get(filter_type)
            if filter_obj:
                try:
                    data_list.append(data_file.parse(filter_obj))
                except src.err.ShipRadarFilterError:
                    self.logger.error(f"No entries for {filter_type}")
                    self.page.snack_bar = flet.SnackBar(
                        content=flet.Text("No entries for selected filter(s)")
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
        if not data_list:
            null_filter = ShipRadarFilter('null')
            data = data_file.parse(null_filter)
        else:
            try:
                data: list[dict] = ShipRadarCSVReader.and_collectors(data_list)
            except IndexError:
                self.logger.error("Error while filtering data")
                self.page.snack_bar = flet.SnackBar(content=flet.Text("Error while filtering data!"))
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
        self.page.go("/plot")
