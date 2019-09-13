# Copyright 2016, Adrian Sampson.
# Copyright 2019, Christopher Larson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Prototyped version of `modify` whose values are defined with a template format string."""

from __future__ import division, absolute_import, print_function

from beets import library, ui
from beets.plugins import BeetsPlugin
from beets.ui import decargs, print_
from beets.ui.commands import _do_query, modify_parse_args, print_and_modify


class ModifyTmplPlugin(BeetsPlugin):
    def __init__(self):
        super(ModifyTmplPlugin, self).__init__()

    def commands(self):
        modify_cmd = ui.Subcommand(
            u'modifytmpl', help=u'change metadata fields, evaluating templates', aliases=(u'modt',)
        )
        modify_cmd.parser.add_option(
            u'-m', u'--move', action='store_true', dest='move',
            help=u"move files in the library directory"
        )
        modify_cmd.parser.add_option(
            u'-M', u'--nomove', action='store_false', dest='move',
            help=u"don't move files in library"
        )
        modify_cmd.parser.add_option(
            u'-w', u'--write', action='store_true', default=None,
            help=u"write new metadata to files' tags (default)"
        )
        modify_cmd.parser.add_option(
            u'-W', u'--nowrite', action='store_false', dest='write',
            help=u"don't write metadata (opposite of -w)"
        )
        modify_cmd.parser.add_album_option()
        modify_cmd.parser.add_format_option(target='item')
        modify_cmd.parser.add_option(
            u'-y', u'--yes', action='store_true',
            help=u'skip confirmation'
        )
        modify_cmd.func = modify_func
        return [modify_cmd]


def modify_func(lib, opts, args):
    query, mods, dels = modify_parse_args(decargs(args))
    if not mods and not dels:
        raise ui.UserError(u'no modifications specified')
    modify_items(lib, mods, dels, query, ui.should_write(opts.write),
                 ui.should_move(opts.move), opts.album, not opts.yes)


# Copied and tweaked from beets.ui.commands to apply a template
def modify_items(lib, mods, dels, query, write, move, album, confirm):
    """Modifies matching items according to user-specified assignments and
    deletions.

    `mods` is a dictionary of field and value pairse indicating
    assignments. `dels` is a list of fields to be deleted.
    """
    # Parse key=value specifications into a dictionary.
    model_cls = library.Album if album else library.Item

    # Get the items to modify.
    items, albums = _do_query(lib, query, album, False)
    objs = albums if album else items

    # Apply changes *temporarily*, preview them, and collect modified
    # objects.
    print_(u'Modifying {0} {1}s.'
           .format(len(objs), u'album' if album else u'item'))
    changed = []
    for obj in objs:
        # Changes from `modify` command here:
        obj_mods = {}
        for key, value in mods.items():
            value = obj.evaluate_template(value)
            obj_mods[key] = model_cls._parse(key, value)

        if print_and_modify(obj, obj_mods, dels) and obj not in changed:
            changed.append(obj)

    # Still something to do?
    if not changed:
        print_(u'No changes to make.')
        return

    # Confirm action.
    if confirm:
        if write and move:
            extra = u', move and write tags'
        elif write:
            extra = u' and write tags'
        elif move:
            extra = u' and move'
        else:
            extra = u''

        changed = ui.input_select_objects(
            u'Really modify%s' % extra, changed,
            lambda o: print_and_modify(o, mods, dels)
        )

    # Apply changes to database and files
    with lib.transaction():
        for obj in changed:
            obj.try_sync(write, move)
