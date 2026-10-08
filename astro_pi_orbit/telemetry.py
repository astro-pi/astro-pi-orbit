from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import socket
import sys
import logging

from skyfield.api import Loader, load

logger = logging.getLogger("astro_pi_orbit")

CACHE_TTL = timedelta(days=3)
DOTFILE_DIRNAME = ".astro_pi_orbit"
FALLBACK_STATE_DIR = Path.home() / ".local" / "state"
if sys.platform == "win32":
    STATE_DIR = Path(os.environ.get("LOCALAPPDATA") or FALLBACK_STATE_DIR)
else:
    STATE_DIR = Path(os.environ.get("XDG_STATE_HOME") or FALLBACK_STATE_DIR)

_tle_dir: Path = Path(os.environ.get("TLE_DIR") or STATE_DIR / DOTFILE_DIRNAME)
_tle_filename = "iss.tle"
_tle_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
_tle_cache_filename = "cache_info.txt"

_bsp_dir = Path(os.environ.get("BSP_DIR") or STATE_DIR / DOTFILE_DIRNAME)
_bsp_421_filename = "de421.bsp"
_bsp_440s_filename = "de440s.bsp"

_timescale = load.timescale()

def is_online(ip = "1.1.1.1", port = 443) -> bool:
    """
    Open a TCP socket to 1.1.1.1:443 as a proxy
    for checking network connectivity.
    Port 443 is used by default over DNS as it is more likely
    to be unblocked in restricted school networks.
    """
    try:
        with socket.create_connection((ip, port), timeout=2):
            return True
    except (socket.error, socket.timeout):
        return False

def _load_iss():
    """
    Retrieves ISS telemetry data from a local or remote TLE file and
    returns a Skyfield EarthSatellite object corresponding to the ISS.
    """
    _tle_dir.mkdir(parents=True, exist_ok=True)
    tle_file = _tle_dir / _tle_filename
    cache_file = _tle_dir / _tle_cache_filename

    cache_expiry_time = None
    if cache_file.exists():
        try:
            cache_expiry_time = datetime.fromisoformat(
                    cache_file.read_text().strip())
        except (ValueError, OSError):
            pass

    is_expired = cache_expiry_time is None or datetime.now(tz=timezone.utc) >= cache_expiry_time
    loader = Loader(_tle_dir, verbose=False)

    def _load_local_file():
        """
        Load a local TLE file.
        """
        try:
            # find telemetry data locally
            satellites = loader.tle_file(_tle_filename)
            iss = next((sat for sat in satellites if sat.name == "ISS (ZARYA)"), None)
            if iss is None:
                raise RuntimeError(
                    f"Unable to find ISS (ZARYA) TLE data from {loader.path_to(_tle_filename)}. Is the file corrupted?"
                )
            return iss
        except FileNotFoundError:
            return

    def _load_remote_file():
        """Download telemetry data from Celestrak"""
        try:
            loader.download(_tle_url, tle_file)
            cache_file.write_text(
                (datetime.now(tz=timezone.utc) + CACHE_TTL).isoformat()
            )
            satellites = loader.tle_file(_tle_filename)
            iss = next((sat for sat in satellites if sat.name == "ISS (ZARYA)"), None)
            if iss is None:
                raise RuntimeError(f"Unable to retrieve ISS TLE data from {_tle_url}")
            return iss

        except Exception as e:
            logger.warning("Failed to download remote TLE data: %s", e)
            return

    iss = None
    online = False
    if is_expired:
        # check whether online only if is expired
        online = is_online()

    # load locally
    if not is_expired or not online:
        iss = _load_local_file()
    if iss:
        return iss

    if online:
        iss = _load_remote_file()
        if iss:
            return iss
        # downloading failed - fallback to the local file
        iss = _load_local_file()
        if iss:
            return iss

    raise FileNotFoundError(
        "Unable to retrieve ISS TLE data: "
        + f"cannot find {loader.path_to(_tle_filename)} or download {_tle_url}."
    )


def load_iss():
    ISS = _load_iss()
    # bind the `coordinates` function to the ISS object as a method
    setattr(ISS, "coordinates", coordinates.__get__(ISS, ISS.__class__))
    return ISS


def coordinates(satellite):
    """
    Return a Skyfield GeographicPosition object corresponding to the  Earth
    latitude and longitude beneath the current celestial position of the ISS.

    See: rhodesmill.org/skyfield/api-topos.html#skyfield.toposlib.GeographicPosition
    """
    return satellite.at(_timescale.now()).subpoint()


def load_ephemeris(bsp_filename):
    loader = Loader(_bsp_dir, verbose=False)
    return loader(bsp_filename)


# create ISS as a Skyfield EarthSatellite object
# See: rhodesmill.org/skyfield/api-satellites.html#skyfield.sgp4lib.EarthSatellite
ISS = load_iss


# Expose ephemeris in the API
de421 = load_ephemeris(_bsp_421_filename)
de440s = load_ephemeris(_bsp_440s_filename)
ephemeris = de421
