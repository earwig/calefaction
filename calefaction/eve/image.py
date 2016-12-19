# -*- coding: utf-8  -*-

__all__ = ["ImageServer"]

class ImageServer:
    """EVE API module for the image server."""

    def __init__(self):
        self._url = "https://imageserver.eveonline.com/"

    @property
    def alliance_widths(self):
        """Return a list of valid widths for alliance logos."""
        return [32, 64, 128]

    @property
    def corp_widths(self):
        """Return a list of valid widths for corporation logos."""
        return [32, 64, 128, 256]

    @property
    def character_widths(self):
        """Return a list of valid widths for character portraits."""
        return [32, 64, 128, 256, 512, 1024]

    @property
    def faction_widths(self):
        """Return a list of valid widths for faction logos."""
        return [32, 64, 128]

    @property
    def inventory_widths(self):
        """Return a list of valid widths for inventory item images."""
        return [32, 64]

    @property
    def render_widths(self):
        """Return a list of valid widths for ship render images."""
        return [32, 64, 128, 256, 512]

    def alliance(self, id, width):
        """Return a URL for an alliance logo."""
        return self._url + "Alliance/{}_{}.png".format(id, width)

    def corp(self, id, width):
        """Return a URL for a corporation logo."""
        return self._url + "Corporation/{}_{}.png".format(id, width)

    def character(self, id, width):
        """Return a URL for a character portrait."""
        return self._url + "Character/{}_{}.jpg".format(id, width)

    def faction(self, id, width):
        """Return a URL for a faction logo."""
        return self._url + "Alliance/{}_{}.jpg".format(id, width)

    def inventory(self, id, width):
        """Return a URL for an inventory item image."""
        return self._url + "Type/{}_{}.jpg".format(id, width)

    def render(self, id, width):
        """Return a URL for ship render image."""
        return self._url + "Render/{}_{}.jpg".format(id, width)
