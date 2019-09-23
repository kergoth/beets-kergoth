"""Set 'advisory' and 'albumadvisory' fields on import based on 'itunesadvisory'.

While beets supports extension of mediafile to add new fields, its maintainer
advises against leveraging it, so set flexible fields on import and rely on
those fields independent of the tags.
"""

from __future__ import division, absolute_import, print_function

import mediafile

from beets.dbcore import types
from beets.plugins import BeetsPlugin
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
