"""Intercept and block write and move operations on items."""

from __future__ import division, absolute_import, print_function

from beets.library import Item
from beets.plugins import BeetsPlugin
from beets.ui import log
from beets.util import MoveOperation


class NoWritePlugin(BeetsPlugin):
    def __init__(self):
        super(NoWritePlugin, self).__init__()

        # Monkeypatch!
        def nowrite(self, path=None, tags=None, id3v23=None):
            log.warning('nowrite: ignoring attempt to write {0}'.format(self.path))

        def nomove(self, operation=MoveOperation.MOVE, basedir=None,
                   with_album=True, store=True):
            log.warning('nowrite: ignoring attempt to move {0}'.format(self.path))

        Item.write = nowrite
        Item.move = nomove
