# -*- coding: utf-8  -*-

import gzip
from threading import Lock

import yaml

__all__ = ["Universe"]

class _SolarSystem:
    """Represents a solar system."""

    def __init__(self, universe, sid, data):
        self._universe = universe
        self._id = sid
        self._data = data

    @property
    def id(self):
        """The solar system's ID, as an integer."""
        return self._id

    @property
    def name(self):
        """The solar system's name, as a string."""
        return self._data["name"]

    @property
    def constellation(self):
        """The solar system's constellation, as a _Constellation object."""
        return self._universe.constellation(self._data["constellation"])

    @property
    def region(self):
        """The solar system's region, as a _Region object."""
        return self._universe.region(self._data["region"])

    @property
    def security(self):
        """The solar system's security status, as a float."""
        return self._data["security"]


class _Constellation:
    """Represents a constellation."""

    def __init__(self, universe, cid, data):
        self._universe = universe
        self._id = cid
        self._data = data

    @property
    def id(self):
        """The constellation's ID, as an integer."""
        return self._id

    @property
    def name(self):
        """The constellation's name, as a string."""
        return self._data["name"]

    @property
    def region(self):
        """The constellation's region, as a _Region object."""
        return self._universe.region(self._data["region"])


class _Region:
    """Represents a region."""

    def __init__(self, universe, rid, data):
        self._universe = universe
        self._id = rid
        self._data = data

    @property
    def id(self):
        """The region's ID, as an integer."""
        return self._id

    @property
    def name(self):
        """The region's name, as a string."""
        return self._data["name"]


class _DummySolarSystem(_SolarSystem):
    """Represents an unknown or invalid solar system."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown",
            "constellation": -1,
            "region": -1,
            "security": 0.0
        })


class _DummyConstellation(_Constellation):
    """Represents an unknown or invalid constellation."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown",
            "region": -1
        })


class _DummyRegion(_Region):
    """Represents an unknown or invalid region."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown"
        })


class Universe:
    """EVE API module for static universe data."""

    def __init__(self, datadir):
        self._dir = datadir
        self._lock = Lock()
        self._loaded = False
        self._systems = {}
        self._constellations = {}
        self._regions = {}

    def _load(self):
        """Load in universe data. This can be called multiple times safely."""
        if self._loaded:
            return

        with self._lock:
            if self._loaded:
                return

            filename = str(self._dir / "galaxy.yml.gz")
            with gzip.open(filename, "rb") as fp:
                data = yaml.load(fp, Loader=yaml.CLoader)

            self._systems = data["systems"]
            self._constellations = data["constellations"]
            self._regions = data["regions"]
            self._loaded = True

    def system(self, sid):
        """Return a _SolarSystem with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if sid not in self._systems:
            return _DummySolarSystem(self)
        return _SolarSystem(self, sid, self._systems[sid])

    def constellation(self, cid):
        """Return a _Constellation with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if cid not in self._constellations:
            return _DummyConstellation(self)
        return _Constellation(self, cid, self._constellations[cid])

    def region(self, rid):
        """Return a _Region with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if rid not in self._regions:
            return _DummyRegion(self)
        return _Region(self, rid, self._regions[rid])
