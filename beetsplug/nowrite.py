"""Intercept and block write and move operations on items."""

from __future__ import absolute_import, division, print_function

from beets.library import Item
from beets.plugins import BeetsPlugin
from beets.ui import log
from beets.util import MoveOperation, displayable_path


class NoWritePlugin(BeetsPlugin):
    def __init__(self):
        super(NoWritePlugin, self).__init__()

        plugin = self

        # Monkeypatch!
        def nowrite(self, path=None, tags=None, id3v23=None):
            plugin._log.info(u'Ignoring attempt to write {0}'.format(displayable_path(self.path)))

        def nomove(self, operation=MoveOperation.MOVE, basedir=None,
                   with_album=True, store=True):
            plugin._log.info(u'Ignoring attempt to move {0}'.format(displayable_path(self.path)))

        Item.write = nowrite
        Item.move = nomove
