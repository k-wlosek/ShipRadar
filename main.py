from flet import app
from gui.App import ShipRadarApp
from flet import WEB_BROWSER
import logging

# logging.basicConfig(level=logging.DEBUG)


def main(page):
    app = ShipRadarApp(page=page)
    page.add(app)
    page.update()
    page.on_route_change = app.route_change
    page.on_view_pop = app.view_pop
    page.go(page.route)
    # app.initialize()


if __name__ == '__main__':
    app(target=main)#, view=WEB_BROWSER, upload_dir="uploads", port=5025)
