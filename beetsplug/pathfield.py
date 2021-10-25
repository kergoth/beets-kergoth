"""Add template functions for working with paths via fields.

- path: join the arguments with a null (\0)
- pathfield: replace a null (\0) with the path separator

With the former, we can store a path with \0 separators in a saved format, i.e.
with the savedformats plugin. With the latter, we can make use of such a path in
a path format, whether provided by that plugin or the inline plugin.

Example:

  item_fields:
    some_path: '\0'.join('Music', 'Subdir1', genre)

  item_formats:
    some_other_path: '%path{Music,Subdir2,$composer}'

  paths:
    comp:1: %pathfield{$some_other_path}/%$artist - $title
    default: %pathfield{$some_path}/%$artist - $title
"""

from __future__ import division, absolute_import, print_function

from beets import config
from beets.plugins import BeetsPlugin
from beets.library import Album, Item


class PathfieldPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.template_funcs['path'] = self.tmpl_path
        self.template_funcs['pathfield'] = self.tmpl_pathfield

    def tmpl_path(self, *p):
        return '\0'.join(p)

    def tmpl_pathfield(self, path):
        return path.replace('\0', '/')
