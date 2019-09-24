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
from beets.ui import Subcommand, show_model_changes
from beets.ui.commands import print_and_modify


class iTunesAdvisoryPlugin(BeetsPlugin):
    album_types = {
        'albumadvisory': types.INTEGER,
    }
    item_types = {
        'advisory': types.INTEGER,
    }

    def __init__(self):
        super(iTunesAdvisoryPlugin, self).__init__()

        field = mediafile.MediaField(
            mediafile.MP3DescStorageStyle(u'ITUNESADVISORY'),
            mediafile.MP4StorageStyle(u'rtng'),
            mediafile.StorageStyle(u'ITUNESADVISORY'),
            mediafile.ASFStorageStyle(u'ITUNESADVISORY'),
            out_type=int,
        )
        mediafile.MediaFile.add_field('itunesadvisory', field)

        self.import_stages = [self.imported]

    def imported(self, session, task):
        changed = set()
        items = task.imported_items()

        explicit = False
        for item in items:
            mf = mediafile.MediaFile(item.path)
            advisory = mf.itunesadvisory
            if advisory:
                if advisory == 1:
                    explicit = True
                if print_and_modify(item, {'advisory': advisory}, []):
                    changed.add(item)

        if task.is_album and explicit:
            task.album.albumadvisory = 1
            if print_and_modify(task.album, {'albumadvisory': 1}, []):
                changed.add(task.album)

        with session.lib.transaction():
            for obj in changed:
                obj.store()

    def commands(self):
        """Add the write-advisory command."""
        write_advisory = Subcommand('write-advisory',
                                    help=u'write the advisory state to tags')
        write_advisory.parser.add_option(
            u'-p', u'--pretend', action='store_true',
            help=u"show all changes but do nothing"
        )
        write_advisory.func = self.write_advisory
        return [write_advisory]

    def write_advisory(self, lib, opts, args):
        for item in lib.items(u'advisory:1..'):
            mf = mediafile.MediaFile(item.path)
            if item.advisory != mf.itunesadvisory:
                fakeitem = new_item(item)
                fakeitem.advisory = mf.itunesadvisory
                show_model_changes(item, fakeitem)
                if not opts.pretend:
                    mf.itunesadvisory = item.advisory
                    mf.save()


def new_item(item):
    newitem = Item()
    newitem.update(item)
    return newitem
