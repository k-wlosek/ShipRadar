import numpy as np
from scipy.interpolate import interp1d
from typing import List, Dict


class Calculation:
    @staticmethod
    def divide_collectors(collector: list[dict]) -> list[list[dict]]:
        """
        Divide collector into multiple collectors, by LRIMO number
        :param collector: collector, returned by reader.ShipRadarCSVReader.and_collector(collectors)
        :return: list of collectors, each collector contains only ships with same LRIMO number
        """
        divided_collectors = []
        # Sort by LRIMO number, so ships with same LRIMO number are next to each other
        collector.sort(key=lambda ship: ship['LRIMOShipNo'])
        # Divide collector into multiple collectors, by LRIMO number
        for entry in collector:
            if divided_collectors and divided_collectors[-1][0]['LRIMOShipNo'] == entry['LRIMOShipNo']:
                divided_collectors[-1].append(entry)
            else:
                divided_collectors.append([entry])
        return divided_collectors

    @staticmethod  # TODO: Ensure that this works, good luck
    def bezier_curve_fit(points: List[Dict[str, float]], num_points: int = 100) -> List[Dict[str, float]]:
        if len(points) < 2:
            return points

        longitudes = [point['Longitude'] for point in points]
        latitudes = [point['Latitude'] for point in points]

        t = np.linspace(0, 1, num_points)

        interp_longitudes = interp1d(np.arange(len(longitudes)), longitudes, kind='cubic')(t)
        interp_latitudes = interp1d(np.arange(len(latitudes)), latitudes, kind='cubic')(t)

        interpolated_points = [{'Longitude': lon, 'Latitude': lat} for lon, lat in
                               zip(interp_longitudes, interp_latitudes)]

        return interpolated_points