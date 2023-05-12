from gui.MainWindow import MainWindow
from flet import app
import flet



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
        self.page.add(self.layout)
        self.page.update()
        super().update()

def main(page):
    app = ShipRadarApp(page=page)
    page.add(app)
    page.update()
    app.initialize()

# Run the app
app(target=main)
