import datetime

import flet
from flet.plotly_chart import PlotlyChart
import pandas as pd
import plotly.graph_objects as go



class Plot(flet.UserControl):
    def __init__(self, page: flet.Page, data: list[dict], title: str, show_lines: bool = False):
        super().__init__()
        self.page = page
        self.data = pd.DataFrame(data)
        self.title = title
        self.show_lines = show_lines
        self.page.update()

    def build(self):
        # TODO Too big, don't need the whole Earth map, just the part where points are

        # Sort the data based on MovementDateTime
        sorted_data: pd.DataFrame = self.data.sort_values(by='MovementDateTime')

        # Convert latitude and longitude values to floats
        latitudes: list[float] = sorted_data['Latitude'].astype(float)
        longitudes: list[float] = sorted_data['Longitude'].astype(float)

        # Calculate the center coordinates based on the latitude and longitude values of the points
        center_lat: float = (max(latitudes) + min(latitudes)) / 2
        center_lon: float = (max(longitudes) + min(longitudes)) / 2

        # Set the zoom level based on the range of latitude and longitude values
        lat_range: float = max(latitudes) - min(latitudes)
        lon_range: float = max(longitudes) - min(longitudes)
        zoom: float = max(lat_range, lon_range) * 144  # Adjust the zoom factor as needed

        # Convert MovementDateTime to datetime objects
        movement_datetimes: list[datetime.datetime] = pd.to_datetime(sorted_data['MovementDateTime'])

        hovertext: list[str] = [sorted_data['ShipName'], sorted_data['MovementDateTime'],
                     sorted_data['Destination']]

        # Create the scattergeo trace for points
        scatter_points = go.Scattergeo(
            lat=latitudes,
            lon=longitudes,
            customdata=hovertext,
            mode='markers',
            marker=dict(
                color='blue',
                size=5,
                line=dict(
                    width=0.5,
                    color='black'
                )
            ),
            showlegend=False,  # Remove the legend
            hovertemplate="<br>".join([
                "Ship Name: %{customdata[0]}",
                "MovementDateTime: %{customdata[1]}",
                "Destination: %{customdata[2]}"
            ])
        )

        # Create the scattergeo trace for lines if show_lines is True
        scatter_lines = None
        if self.show_lines:
            # Create a list of line coordinates by combining adjacent points
            line_coordinates = [(lon1, lat1, lon2, lat2) for (lat1, lon1), (lat2, lon2) in
                                zip(zip(latitudes[:-1], longitudes[:-1]), zip(latitudes[1:], longitudes[1:]))]

            scatter_lines = go.Scattergeo(
                lat=[lat1 for lon1, lat1, lon2, lat2 in line_coordinates],
                lon=[lon1 for lon1, lat1, lon2, lat2 in line_coordinates],
                mode='lines',
                line=dict(color='blue', width=2),
                showlegend=False  # Remove the legend
            )

        # Create the figure and add the traces
        fig = go.Figure(data=[scatter_points, scatter_lines] if self.show_lines else [scatter_points])

        fig.update_geos(
            center=dict(lon=center_lon, lat=center_lat),
            projection_scale=zoom
        )

        fig.update_layout(
            title='Ships',
            title_x=0.5,
            margin=dict(r=0, l=0, t=50, b=0),  # Adjust the margins
            hovermode='closest',  # Set hover mode to show closest point information
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
                showcountries=True,
                showocean=True,
                oceancolor='rgb(200, 255, 255)',
                showcoastlines=True,
                coastlinecolor='rgb(150, 150, 150)',
                showframe=False,
                projection_type='equirectangular'
            )
        )


        fig.show()

        return PlotlyChart(
            fig
        )



