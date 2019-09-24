from __future__ import absolute_import, division, print_function

from beets.plugins import BeetsPlugin


class ConvertSingletonsPlugin(BeetsPlugin):
    def __init__(self):
        super(ConvertSingletonsPlugin, self).__init__()

        self.register_listener('import_begin', self.import_begin)
        self.register_listener('album_imported', self.import_album)
        self.register_listener('import', self.import_end)

    def import_begin(self, session):
        self.to_convert = set()

    def import_album(self, lib, album):
        if not album.album or album.album == '[non-album tracks]':
            self.to_convert |= set(album.items())

    def import_end(self, lib, paths):
        albums = {}
        with lib.transaction():
            for item in self.to_convert:
                if item.album_id not in albums:
                    albums[item.album_id] = item.get_album()
                self._log.info('converted {0} to a singleton'.format(item))
                item.album_id = None
                item.store()

        with lib.transaction():
            for album in albums.values():
                if not album.items():
                    self._log.info('removed remnant empty album {0} due to conversions to singleton'.format(album.id))
                    album.remove(with_items=False)
