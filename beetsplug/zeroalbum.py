"""Clear fields in albums in the database, obeying the 'zero' plugin configuration.

The zero plugin focuses on updating tags, and incidentally can update the database,
but when it does so, it only updates the files and corresponding items, but not the
album associated to those items. This plugin does so.
"""

from __future__ import absolute_import, division, print_function

from beets import config
from beets.library import Item
from beets.plugins import BeetsPlugin, find_plugins


class ZeroAlbumPlugin(BeetsPlugin):
    def __init__(self):
        super(ZeroAlbumPlugin, self).__init__()

        self.config = config['zero']
        self.fields = list(Item._media_fields)

        self.import_stages = [self.imported]
        self.register_listener('pluginload', self.pluginload)

    def pluginload(self):
        self.zero_plugin = None
        if self.config['auto'] and self.config['update_database']:
            for plugin in find_plugins():
                if plugin.name == 'zero':
                    self.zero_plugin = plugin
                    break

    def imported(self, session, task):
        if self.zero_plugin and task.is_album:
            self.zero_plugin.set_fields(task.album, dict(task.album))
            task.album.store()
