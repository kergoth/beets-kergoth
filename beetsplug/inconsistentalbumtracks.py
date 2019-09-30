"""Identify albums whose tracks have inconsistent album fields."""

from __future__ import absolute_import, division, print_function

from beets import ui
from beets.library import Album
from beets.plugins import BeetsPlugin
from beets.ui import decargs, print_


class InconsistentAlbumTracks(BeetsPlugin):
    def __init__(self):
        super(InconsistentAlbumTracks, self).__init__()

        self.config.add({
            'ignored_fields': ['added']
        })

        self.ignored_fields = set(self.config['ignored_fields'].as_str_seq())
        self.album_fields = set(Album.item_keys) - self.ignored_fields

    def commands(self):
        cmd = ui.Subcommand(
            u'inconsistent-album-tracks', help=u'Identify albums whose tracks have inconsistent album fields.'
        )
        cmd.func = self.command
        return [cmd]

    def command(self, lib, opts, args):
        query = decargs(args)
        for album in lib.albums(query):
            for item in album.items():
                for field in self.album_fields:
                    if item[field] != album[field]:
                        print_(u'{}: field `{}` has value `{}` but album value is `{}`'.format(item, field, item[field], album[field]))
