"""Set 'advisory' and 'albumadvisory' fields on import based on 'itunesadvisory'.

While beets supports extension of mediafile to add new fields, its maintainer
advises against leveraging it, so set flexible fields on import and rely on
those fields independent of the tags.
"""

from __future__ import absolute_import, division, print_function

import mediafile
from beets.dbcore import types
from beets.library import Item
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, show_model_changes, decargs, print_
from beets.ui.commands import print_and_modify, _do_query


class iTunesAdvisoryPlugin(BeetsPlugin):
    album_types = {
        'albumadvisory': types.INTEGER,
    }
    item_types = {
        'advisory': types.INTEGER,
    }

    def __init__(self):
        super(iTunesAdvisoryPlugin, self).__init__()

        self.config.add({
            'auto': True,
        })

        field = mediafile.MediaField(
            mediafile.MP3DescStorageStyle(u'ITUNESADVISORY'),
            mediafile.MP4StorageStyle(u'rtng'),
            mediafile.StorageStyle(u'ITUNESADVISORY'),
            mediafile.ASFStorageStyle(u'ITUNESADVISORY'),
            out_type=int,
        )
        mediafile.MediaFile.add_field('itunesadvisory', field)

        if self.config['auto'].get():
            self.import_stages = [self.imported]

    def commands(self):
        """Add the commands."""
        write_advisory = Subcommand('write-advisory',
                                    help=u'write the advisory state to tags')
        write_advisory.parser.add_option(
            u'-p', u'--pretend', action='store_true',
            help=u"show all changes but do nothing"
        )
        write_advisory.func = self.write_advisory
        read_advisory = Subcommand('read-advisory',
                                   help=u'read the advisory state from tags')
        read_advisory.parser.add_option(
            u'-p', u'--pretend', action='store_true',
            help=u"show all changes but do nothing"
        )
        read_advisory.func = self.read_advisory
        return [read_advisory, write_advisory]

    def write_advisory(self, lib, opts, args):
        self.config.set_args(opts)
        for item in lib.items(u'advisory:1..'):
            mf = mediafile.MediaFile(item.path)
            if item.advisory != mf.itunesadvisory:
                fakeitem = new_item(item)
                fakeitem.advisory = mf.itunesadvisory
                show_model_changes(item, fakeitem)
                if not opts.pretend:
                    mf.itunesadvisory = item.advisory
                    mf.save()

    def read_advisory(self, lib, opts, args):
        self.config.set_args(opts)
        query = decargs(args)
        items, _ = _do_query(lib, query, None, False)
        if not items:
            print_(u'No items matched the specified query: {0}.'.format(' '.join(query)))
            return
        self.read_items(lib, items, pretend=opts.pretend)

    def imported(self, session, task):
        self.read_items(session.lib, task.imported_items(), task.is_album and task.album or None)

    def read_items(self, lib, items, album=None, pretend=False):
        changed = set()
        albums = {}
        dels = []

        for item in items:
            mf = mediafile.MediaFile(item.path)
            advisory = mf.itunesadvisory
            if advisory:
                if advisory == 1:
                    if album:
                        albums[album.id] = album
                    elif not item.singleton and item.album_id not in albums:
                        albums[item.album_id] = item.get_album()

                if print_and_modify(item, {'advisory': advisory}, dels):
                    changed.add(item)

        for album_id, album in albums.items():
            if print_and_modify(album, {'albumadvisory': 1}, dels):
                changed.add(album)

        if not pretend:
            with lib.transaction():
                for obj in changed:
                    obj.store()


def new_item(item):
    newitem = Item()
    newitem.update(item)
    return newitem
