"""Identify albums whose tracks have inconsistent album fields."""

from __future__ import absolute_import, division, print_function

from collections import defaultdict

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
            inconsistent_fields = defaultdict(list)
            album_items = album.items()

            for item in album_items:
                for field in self.album_fields:
                    if item[field] != album[field]:
                        inconsistent_fields[field].append(item)

            for field in sorted(inconsistent_fields):
                items = inconsistent_fields[field]
                if len(items) == len(album_items):
                    print_(u'{}: field `{}` has album value `{}` but all track values are `{}`'.format(album, field, album[field], items[0][field]))
                else:
                    for item in items:
                        print_(u'{}: field `{}` has value `{}` but album value is `{}`'.format(item, field, item[field], album[field]))
