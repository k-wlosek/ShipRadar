"""
Contains the Plot class, which is used to create a plot window
"""
import itertools
from typing import Union
import flet
import pandas as pd
import plotly.graph_objects as go
import distinctipy
from flet.plotly_chart import PlotlyChart


class Plot(flet.UserControl):
    """
    A class to create a plot window
    """
    def __init__(self, page: flet.Page, data: list[list[dict]], title: str):
        super().__init__()
        self.layout: Union[None, flet.Control] = None
        self.__chart: Union[None, PlotlyChart] = None
        self.__fig: Union[None, go.Figure] = None
        self.page = page
        self.page.on_resize = self.on_resize
        self.data = data
        self.title = title

        self.show_lines = True
        self.__block = False

        self.colors: list[tuple[float, float, float]] = distinctipy.get_colors(len(self.data))
        self.page.update()

    def on_resize(self, e: flet.ScaleUpdateEvent) -> None:
        """
        Update the chart when the page is resized
        :param e: Resize event
        :return: None
        """
        self.__chart.figure = self.__fig
        self.page.update()
        self.layout.update()

    def build(self):
        """
        Build the plot window
        :return: The layout of the plot window
        """
        self.__initialize_chart()

        self.__chart = PlotlyChart(self.__fig)
        self.layout = flet.Column(
            [
                flet.Container(content=self.__chart,
                               height=self.page.height * 0.8
                               ),
                flet.Row(
                    [
                        flet.ElevatedButton(text="Open as interactive",
                                            icon=flet.icons.OPEN_IN_NEW,
                                            on_click=self.__show_fig
                                            ),
                        flet.ElevatedButton(text="Toggle lines",
                                            icon=flet.icons.LINE_STYLE,
                                            on_click=self.__toggle_lines
                                            )
                    ]
                )
            ]
        )

        return self.layout

    def __initialize_chart(self) -> None:
        """
        Initialize the chart
        :return: None
        """
        self.__block = True

        all_data_list: list[dict] = list(itertools.chain(*self.data))

        # Create a dataframe of all the data to determine the center coordinates and zoom level
        all_data: pd.DataFrame = pd.DataFrame(all_data_list)
        all_data.sort_values(by='MovementDateTime',
                             key=lambda x: pd.to_datetime(x),
                             inplace=True
                             )

        # Convert latitude and longitude values to floats
        latitudes: list[float] = all_data['Latitude'].astype(float)
        longitudes: list[float] = all_data['Longitude'].astype(float)

        # Calculate the center coordinates based on the latitude and longitude values of the points
        center_lat: float = (max(latitudes) + min(latitudes)) / 2
        center_lon: float = (max(longitudes) + min(longitudes)) / 2

        # Create the figure
        self.__fig: go.Figure = go.Figure()

        # Add the scattergeo trace for points
        for ship, color in zip(self.data, self.colors):
            data_frame: pd.DataFrame = pd.DataFrame(ship)

            # Sort the data based on MovementDateTime
            sorted_data: pd.DataFrame = data_frame.sort_values(by='MovementDateTime',
                                                               key=lambda x: pd.to_datetime(x)
                                                               )
            # Create a text column for the hovertext
            sorted_data['text']: str = sorted_data.apply(lambda row:
                                                         f"<b>Ship name:</b> {row['ShipName']}<br>"
                                                         f"<b>LRIMO number:</b> {row['LRIMOShipNo']}<br>"
                                                         f"<b>Ship type:</b> {row['ShipType']}<br>"
                                                         f"<b>Movement date:</b> {row['MovementDateTime']}<br>"
                                                         f"<b>Move status:</b> {row['MoveStatus']}<br>"
                                                         f"<b>Destination:</b> {row['Destination']}<br>"
                                                         f"<b>ETA:</b> {row['ETA']}<br>"
                                                         f"<b>Heading:</b> {row['Heading']}<br>"
                                                         f"<b>Speed:</b> {row['Speed']}<br>"
                                                         f"<b>Draught:</b> {row['Draught']}<br>", axis=1
                                                         )

            # Create the scattergeo trace for points
            scatter_points = go.Scattergeo(
                lat=sorted_data['Latitude'].astype(float),
                lon=sorted_data['Longitude'].astype(float),
                hovertext=sorted_data['text'],
                mode='lines+markers' if self.show_lines else 'markers',
                marker={
                    "color": f'rgb({color[0] * 255}, {color[1] * 255}, {color[2] * 255})',
                    "size": 5
                },
                line={
                    "width": 1,
                    "color": f'rgb({color[0] * 255}, {color[1] * 255}, {color[2] * 255})'
                },
                showlegend=True,
                name=sorted_data['ShipName'][0]
            )
            self.__fig.add_trace(scatter_points)

        # Adjust the center and zoom level of the map
        self.__fig.update_geos(
            center={
                "lon": center_lon,
                "lat": center_lat
            },
            fitbounds='locations'
        )

        self.__fig.update_layout(
            title='Selected ship movements',
            title_x=0.5,
            margin={
                "r": 0,
                "l": 0,
                "t": 30,
                "b": 0
            },
            hovermode='closest',  # Set hover mode to show the closest point information
            geo={
                "showland": True,
                "landcolor": 'rgb(243, 243, 243)',
                "countrycolor": 'rgb(204, 204, 204)',
                "showcountries": True,
                "showocean": True,
                "oceancolor": 'rgb(200, 255, 255)',
                "showcoastlines": True,
                "coastlinecolor": 'rgb(150, 150, 150)',
                "showframe": False,
                "projection_type": 'natural earth'
            }
        )

        self.__block = False

    def __toggle_lines(self, e: flet.TapEvent) -> None:
        """
        Toggle the lines on the chart
        :param e: Click event
        :return: None
        """
        if self.__block:
            self.page.snack_bar = flet.SnackBar(content=flet.Text("Please wait, chart is being updated"))
            self.page.snack_bar.open = True
            self.page.update()
            return None
        self.show_lines = False if self.show_lines else True  # Toggle the show_lines variable
        self.__initialize_chart()

        # Update the chart and GUI
        self.__chart.figure = self.__fig
        self.page.update()
        self.layout.update()
        return None

    def __show_fig(self, e: flet.TapEvent) -> None:
        """
        Show the figure in a new window
        :param e: Click event
        :return: None
        """
        self.__fig.show()
