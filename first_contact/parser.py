import re

from first_contact.models import SatelliteChallenge


class ChallengeParser:

    TLE_PATTERN = re.compile(
        r"TLE:\s*\n"
        r"([^\r\n]+)\r?\n"
        r"(1 [^\r\n]+)\r?\n"
        r"(2 [^\r\n]+)"
    )

    LOCATION_PATTERN = re.compile(
        r"\(Lat,Long\):\s*"
        r"([-+]?[0-9]*\.?[0-9]+)\s*,\s*"
        r"([-+]?[0-9]*\.?[0-9]+)"
    )

    def parse(self, text: str) -> SatelliteChallenge:
        tle_match = self.TLE_PATTERN.search(text)
        location_match = self.LOCATION_PATTERN.search(text)

        if tle_match is None:
            raise ValueError("Unable to find TLE data")

        if location_match is None:
            raise ValueError("Unable to find station coordinates")

        return SatelliteChallenge(
            name=tle_match.group(1).strip(),
            tle_line1=tle_match.group(2).strip(),
            tle_line2=tle_match.group(3).strip(),
            latitude=float(location_match.group(1)),
            longitude=float(location_match.group(2)),
        )