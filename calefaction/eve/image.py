# -*- coding: utf-8  -*-

__all__ = ["ImageServer"]

class ImageServer:

    def __init__(self):
        self._url = "https://imageserver.eveonline.com/"

    @property
    def alliance_widths(self):
        return [32, 64, 128]

    @property
    def corp_widths(self):
        return [32, 64, 128, 256]

    @property
    def character_widths(self):
        return [32, 64, 128, 256, 512, 1024]

    @property
    def faction_widths(self):
        return [32, 64, 128]

    @property
    def inventory_widths(self):
        return [32, 64]

    @property
    def render_widths(self):
        return [32, 64, 128, 256, 512]

    def alliance(self, id, width):
        return self._url + "Alliance/{}_{}.png".format(id, width)

    def corp(self, id, width):
        return self._url + "Corporation/{}_{}.png".format(id, width)

    def character(self, id, width):
        return self._url + "Character/{}_{}.jpg".format(id, width)

    def faction(self, id, width):
        return self._url + "Alliance/{}_{}.jpg".format(id, width)

    def inventory(self, id, width):
        return self._url + "Type/{}_{}.jpg".format(id, width)

    def render(self, id, width):
        return self._url + "Render/{}_{}.jpg".format(id, width)
