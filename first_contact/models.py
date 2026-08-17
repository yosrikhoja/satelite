from dataclasses import dataclass


@dataclass(frozen=True)
class SatelliteChallenge:
    name: str
    tle_line1: str
    tle_line2: str
    latitude: float
    longitude: float