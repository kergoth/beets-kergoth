"""Require the 'source' field be set, to organize the library by where the music was obtained.

Ex. iTunes, Amazon, etc.
"""

from __future__ import division, absolute_import, print_function

from beets import config, ui
from beets.plugins import BeetsPlugin


class MusicSourcePlugin(BeetsPlugin):
    def __init__(self):
        super(MusicSourcePlugin, self).__init__()
        self.register_listener('import_task_created', self.import_task_created)

    def import_task_created(self, session, task):
        try:
            reimporting = config['import']['library'].get()
        except Exception:
            reimporting = False

        if not reimporting:
            set_fields = config['import']['set_fields']
            if 'source' not in set_fields.keys():
                raise ui.UserError('No source specified, please include --set=source=SOURCE')
