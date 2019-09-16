"""Inspect candidate changes when importing.

Add a command to inspect candidate changes and has an option to automatically
inspect the changes when the user selects Apply, and will prompt to continue
when timid.
"""

from __future__ import division, absolute_import, print_function

from beets import autotag, config, importer, library, ui
from beets.plugins import BeetsPlugin
from beets.ui.commands import PromptChoice


def new_item(i):
    ni = library.Item()
    ni.update(i)
    return ni


class ImportInspectPlugin(BeetsPlugin):
    def __init__(self):
        super(ImportInspectPlugin, self).__init__()

        self.config.add({
            'on_apply': True,
            # Fields always ignored
            'ignored': '',
            # Fields ignored only when they're new (no previous value)
            'ignored_new': '',
            # Fields ignored only when they're existing (changed from previous value)
            'ignored_existing': '',
        })

        self.album_fields = set(library.Album.item_keys)
        self.nonalbum_fields = library.Item._media_tag_fields.difference(self.album_fields)
        self.all_fields = list(sorted(self.album_fields | self.nonalbum_fields))

        self.ignored = set(self.config['ignored'].as_str_seq())
        self.album_fields = list(sorted(self.album_fields - self.ignored))
        self.nonalbum_fields = list(sorted(self.nonalbum_fields - self.ignored))

        self.ignored_new = set(self.config['ignored_new'].as_str_seq())
        self.ignored_existing = set(self.config['ignored_existing'].as_str_seq())

        self.register_listener('before_choose_candidate',
                               self.before_choose_candidate_listener)

        if self.config['on_apply'].get():
            self.register_listener('import_task_choice',
                                   self.import_task_choice_listener)

    def before_choose_candidate_listener(self, session, task):
        if task.candidates:
            return [PromptChoice('n', 'iNspect changes',
                                      self.importer_inspect_candidate)]

    def importer_inspect_candidate(self, session, task):
        # Prompt the user for a candidate.
        sel = ui.input_options([], numrange=(1, len(task.candidates)))
        match = task.candidates[sel - 1]

        self.show_changes(session.lib, task, match)
        return None

    def import_task_choice_listener(self, session, task):
        if task.apply:
            if config['import']['quiet'].get():
                return

            changes = self.show_changes(session.lib, task)

            # Only prompt when timid
            if 'timid' in self.config:
                timid = self.config['timid'].get(bool)
            else:
                timid = config['import']['timid'].get()

            if not changes or not timid:
                return

            if not ui.input_yn(u'Continue to apply these changes (Y/n)?'):
                task.set_choice(importer.action.SKIP)

    def show_changes(self, lib, task, match=None):
        if match is None:
            match = task.match

        changes = False
        if task.is_album:
            newmapping = {new_item(item): track_info for item, track_info in match.mapping.items()}
            autotag.apply_metadata(match.info, newmapping)

            # olditems[0].get_album() isn't working, create our own to compare
            olditems = list(match.mapping.keys())
            oldvalues = dict((key, olditems[0][key]) for key in self.album_fields)
            oldalbum = library.Album(lib, **oldvalues)

            newitems = list(newmapping.keys())
            values = dict((key, newitems[0][key]) for key in self.album_fields)
            album = library.Album(lib, **values)
            compare_fields = self.get_fields(self.album_fields, oldvalues)

            album_changes = show_model_changes(album, oldalbum, compare_fields)
            if album_changes:
                changes = True

            new_by_info = {track_info: item for item, track_info in newmapping.items()}
            for item, track_info in match.mapping.items():
                newitem = new_by_info[track_info]
                compare_fields = self.get_fields(self.nonalbum_fields, item)
                item_changes = show_model_changes(newitem, item, compare_fields)
                if item_changes:
                    changes = True
        else:
            fakeitem = new_item(task.item)
            autotag.apply_item_metadata(fakeitem, match.info)
            compare_fields = self.get_fields(self.all_fields, task.item)
            changes = show_model_changes(fakeitem, task.item, compare_fields)

        return changes

    def get_fields(self, keys, old):
        compare_fields = []
        for key in sorted(keys):
            if old.get(key):
                ignored = self.ignored_existing
            else:
                ignored = self.ignored_new
            if key not in ignored:
                compare_fields.append(key)
        return compare_fields


def show_model_changes(new, old=None, fields=None, always=False):
    """Given a Model object, print a list of changes from its pristine
    version stored in the database. Return a boolean indicating whether
    any changes were found.

    `old` may be the "original" object to avoid using the pristine
    version from the database. `fields` may be a list of fields to
    restrict the detection to. `always` indicates whether the object is
    always identified, regardless of whether any changes are present.
    """
    old = old or new._db._get(type(new), new.id)

    # Build up lines showing changed fields.
    changes = []
    for field in sorted(old):
        # Subset of the fields. Never show mtime.
        if field == 'mtime' or (fields and field not in fields):
            continue

        # Detect and show difference for this field.
        line = ui._field_diff(field, old, new)
        if line:
            changes.append(u'  {0}: {1}'.format(field, line))

    # New fields.
    for field in sorted(set(new) - set(old)):
        if fields and field not in fields:
            continue

        changes.append(u'  {0}: {1}'.format(
            field,
            ui.colorize('text_highlight', new.formatted()[field])
        ))

    # Print changes.
    if changes or always:
        ui.print_(format(old))
    if changes:
        ui.print_(u'\n'.join(changes))

    return bool(changes)
