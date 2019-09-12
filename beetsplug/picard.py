"""Run 'beet picard' on the paths to be imported.

This is useful when you want to use MusicBrainz Picard to examine or manipulate
the tags of the files being imported/reimported. Spawning picard will differ
between platforms, so we assume a `beet-picard` alias/script is available to do
the work.
"""

from __future__ import division, absolute_import, print_function

import subprocess

from beets import ui, util
from beets.plugins import BeetsPlugin
from beets.ui.commands import PromptChoice


class ImportPicardPlugin(BeetsPlugin):
    def __init__(self):
        super(ImportPicardPlugin, self).__init__()

        self.register_listener('before_choose_candidate',
                               self.before_choose_candidate_listener)

    def before_choose_candidate_listener(self, session, task):
        return [PromptChoice('p', 'Picard', self.run_picard)]

    def run_picard(self, session, task):
        paths = [util.syspath(item.path) for item in task.items]
        argv = ['beet', 'picard'] + paths
        try:
            subprocess.check_call(argv)
        except subprocess.CalledProcessError as exc:
            raise ui.UserError(str(exc))
        return None
