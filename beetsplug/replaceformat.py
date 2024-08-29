r"""
Path format function to apply the specified set of replacements to a path.

This can be used to apply replacements only to the alternative library created
by beets-alternatives, for example, while leaving the original library alone.

`replace_path` operates on a per-path-component basis, while `replace`
operates on the whole. The former is useful for replacing across a full path,
the latter on a field, as the latter can handle the case where the field
contains a path separator.

`sub` and `sub_path` are the same as `replace` and `replace_path`, but apply
a single specified replacement rather than referencing a set of replacements
in the config.

Usage:

  foo_replace:
    Foo: Bar

  bar_replace:
    '/.*': ''

  paths:
    default: '%replace_path{foo_replace,$album/$track - $artist - $title}'
    genre:foo: 'Foo/%replace{bar_replace,$album}/$track - $artist - $title'
    genre:bar: '%sub{$album,Foo,Bar}/$track - $artist - $title'
    singleton:bar: '%sub_path{[non-album tracks]/$track - $artist - $title,^\.}'
"""

from __future__ import division, absolute_import, print_function

import functools
import re

import confuse

from beets import config, util
from beets.ui import UserError
from beets.plugins import BeetsPlugin


class ReplacePlugin(BeetsPlugin):
    def __init__(self):
        super(ReplacePlugin, self).__init__()
        self.template_funcs['replace'] = self.replace
        self.template_funcs['replace_path'] = self.replace_path
        self.template_funcs['sub'] = self.sub
        self.template_funcs['sub_path'] = self.sub_path
        self.replacements = {}
        self.patterns = {}

    def replace(self, config_path, string):
        if config_path in self.replacements:
            replacements = self.replacements[config_path]
        else:
            replacements = self.replacements[config_path] = get_replacements(config_path)

        for regex, repl in replacements:
            string = regex.sub(repl, string)
        return string

    def replace_path(self, config_path, path):
        if config_path in self.replacements:
            replacements = self.replacements[config_path]
        else:
            replacements = self.replacements[config_path] = get_replacements(config_path)

        return util.sanitize_path(path, replacements)

    def sub(self, string, pattern, repl=''):
        if pattern in self.patterns:
            pattern = self.patterns[pattern]
        else:
            pattern = self.patterns[pattern] = re.compile(pattern)

        try:
            return pattern.sub(repl, string)
        except re.error as exc:
            raise UserError(f'%sub: error compiling regex `{pattern}`: {str(exc)}')

    def sub_path(self, path, pattern, repl=''):
        if pattern in self.patterns:
            pattern = self.patterns[pattern]
        else:
            pattern = self.patterns[pattern] = re.compile(pattern)

        try:
            return util.sanitize_path(path, [(pattern, repl)])
        except re.error as exc:
            raise UserError(f'%sub_path: error compiling regex `{pattern}`: {str(exc)}')


# Copied with tweak from beets itself
def get_replacements(config_path):
    replacements = []
    lookup = functools.reduce(lambda x, y: x[y], config_path.split("."), config)
    for pattern, repl in lookup.get(dict).items():
        try:
            replacements.append((re.compile(pattern), repl or ''))
        except re.error as exc:
            raise confuse.ConfigError(f'{config_path}: error compiling regex `{pattern}`: {str(exc)}')
    return replacements
