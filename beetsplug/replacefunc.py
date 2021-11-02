"""
Path format function to selectively apply replacement rules to a path component.

As one example, this can be used to apply replacement rules only to the
alternative library created by beets-alternatives, while leaving the original
library alone.

Usage:

  replacefunc:
    artist:
        The Jimi Hendrix Experience: Jimi Hendrix

  alternatives:
    test:
      paths:
        default: '$album/%replace{artist,$artist}/$track - $title'
"""

from __future__ import division, absolute_import, print_function

import re
from beets.ui import UserError

import confuse

from beets import util
from beets.plugins import BeetsPlugin


class ReplaceFuncPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.template_funcs["replace"] = self.replace
        self.replacements = {}

    def replace(self, field, path):
        if field in self.replacements:
            replacements = self.replacements[field]
        else:
            try:
                replacements = self.replacements[field] = get_replacements(
                    self.config[field]
                )
            except confuse.ConfigError as exc:
                raise UserError(
                    f"Configuration error in `simplereplace.{field}`: {exc}"
                )

        return util.sanitize_path(path, replacements)


# Copied with tweak from beets itself
def get_replacements(config):
    replacements = []
    for pattern, repl in config.get(dict).items():
        try:
            replacements.append((re.compile(pattern), repl or ""))
        except re.error as exc:
            raise UserError(f"error compiling regex `{pattern}`: {exc}")
    return replacements
