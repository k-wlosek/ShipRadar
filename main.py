"""
Main entry point for the application.
"""

import sys
from flet import app, WEB_BROWSER, Page
from gui.App import ShipRadarApp
from src.logger import ShipRadarLogger


def main(page: Page) -> None:
    """
    Main entry point for the application.
    :param page: Page object, implicitly passed by flet
    :return: None
    """
    app_obj = ShipRadarApp(page=page)
    page.add(app_obj)
    page.update()
    page.on_route_change = app_obj.route_change
    page.on_view_pop = app_obj.view_pop
    page.go(page.route)


if __name__ == '__main__':
    root = ShipRadarLogger()
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        root.debug("Running in a bundle")
        app(target=main)
    else:
        root.debug("Running in a normal Python environment")
        root.info("ShipRadar starting in browser")
        app(target=main, view=WEB_BROWSER, upload_dir="uploads", port=5025)
