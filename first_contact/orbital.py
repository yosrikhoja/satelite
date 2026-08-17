from datetime import timedelta

from skyfield.api import EarthSatellite, load, wgs84

from first_contact.models import SatelliteChallenge


class VisibilityCalculator:

    def __init__(
            self,
            minimum_elevation: float = 30.0,
            search_window_hours: int = 24,
    ):
        self.minimum_elevation = minimum_elevation
        self.search_window_hours = search_window_hours
        self.timescale = load.timescale()

    def calculate(
            self,
            challenge: SatelliteChallenge,
    ) -> list[str]:

        satellite = EarthSatellite(
            challenge.tle_line1,
            challenge.tle_line2,
            challenge.name,
            self.timescale,
        )

        station = wgs84.latlon(
            latitude_degrees=challenge.latitude,
            longitude_degrees=challenge.longitude,
        )

        start = satellite.epoch

        end_datetime = (
                start.utc_datetime()
                + timedelta(hours=self.search_window_hours)
        )

        end = self.timescale.from_datetime(end_datetime)

        times, events = satellite.find_events(
            station,
            start,
            end,
            altitude_degrees=self.minimum_elevation,
        )

        return self._extract_windows(times, events)

    @staticmethod
    def _extract_windows(times, events) -> list[str]:
        result: list[str] = []
        current_rise: str | None = None

        for time, event in zip(times, events):
            timestamp = time.utc_strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            if event == 0:
                current_rise = timestamp

            elif event == 2 and current_rise is not None:
                result.extend(
                    [
                        current_rise,
                        timestamp,
                    ]
                )

                current_rise = None

        return result