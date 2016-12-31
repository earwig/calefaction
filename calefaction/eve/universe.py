# -*- coding: utf-8  -*-

import gzip
from threading import Lock

import yaml

__all__ = ["Universe"]

class _UniqueObject:
    """Base class for uniquely ID'd objects in the universe."""

    def __init__(self, universe, id_, data):
        self._universe = universe
        self._id = id_
        self._data = data

    @property
    def id(self):
        """The object's unique ID, as an integer."""
        return self._id


class _SolarSystem(_UniqueObject):
    """Represents a solar system."""

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

    @property
    def faction(self):
        """The solar system's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return self.constellation.faction

    @property
    def is_nullsec(self):
        """Whether the solar system is in nullsec."""
        return self.security < 0.05

    @property
    def is_lowsec(self):
        """Whether the solar system is in nullsec."""
        return self.security >= 0.05 and self.security < 0.45

    @property
    def is_highsec(self):
        """Whether the solar system is in nullsec."""
        return self.security >= 0.45


class _Constellation(_UniqueObject):
    """Represents a constellation."""

    @property
    def name(self):
        """The constellation's name, as a string."""
        return self._data["name"]

    @property
    def region(self):
        """The constellation's region, as a _Region object."""
        return self._universe.region(self._data["region"])

    @property
    def faction(self):
        """The constellation's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return self.region.faction


class _Region(_UniqueObject):
    """Represents a region."""

    @property
    def name(self):
        """The region's name, as a string."""
        return self._data["name"]

    @property
    def faction(self):
        """The region's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return None


class _Faction(_UniqueObject):
    """Represents a faction."""

    @property
    def name(self):
        """The faction's name, as a string."""
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


class _DummyFaction(_Faction):
    """Represents an unknown or invalid faction."""

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
        self._factions = {}

    @staticmethod
    def _load_yaml(path):
        """Load in and return a YAML file with the given path."""
        with gzip.open(str(path), "rb") as fp:
            return yaml.load(fp, Loader=yaml.CLoader)

    def _load(self):
        """Load in universe data. This can be called multiple times safely."""
        if self._loaded:
            return

        with self._lock:
            if self._loaded:
                return

            galaxy = self._load_yaml(self._dir / "galaxy.yml.gz")
            self._systems = galaxy["systems"]
            self._constellations = galaxy["constellations"]
            self._regions = galaxy["regions"]
            del galaxy

            entities = self._load_yaml(self._dir / "entities.yml.gz")
            self._factions = entities["factions"]
            del entities

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

    def faction(self, fid):
        """Return a _Faction with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if fid not in self._factions:
            return _DummyFaction(self)
        return _Faction(self, fid, self._factions[fid])

    def ship(self, sid):
        """Return a _Ship with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        ...
        raise NotImplementedError()
