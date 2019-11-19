"""Apply modifications on album/item import."""

from __future__ import absolute_import, division, print_function

from beets import ui, util
from beets.library import Album, Item, parse_query_string
from beets.plugins import BeetsPlugin
from beets.ui import decargs
from beets.ui.commands import modify_parse_args, print_and_modify
from beets.util import shlex_split


class ModifyOnImport(BeetsPlugin):
    def __init__(self):
        super(ModifyOnImport, self).__init__()

        self.config.add({
            'modify_album': {},
            'modify_album_items': {},
            'modify_singleton': {},
        })

        self.import_stages = [self.imported]
        self.register_listener('import_begin', self.import_begin)

    def import_begin(self, session):
        self.should_write = ui.should_write()
        self.should_move = ui.should_move()

        for name, model_cls in [('album', Album), ('singleton', Item)]:
            modifies = self.get_modifies(self.config['modify_' + name].items(), model_cls, 'modify_' + name)
            setattr(self, name + '_modifies', modifies)

        self.album_item_modifies = []
        for albumquery, itemmodifies in self.config['modify_album_items'].items():
            albumdbquery, _ = parse_query_string(util.as_string(albumquery), Album)
            modifies = self.get_modifies(itemmodifies.items(), Item, u'modify_album_items.{0}'.format(albumquery))
            self.album_item_modifies.append((albumdbquery, modifies))

    def get_modifies(self, items, model_cls, context):
        modifies = []
        for query, modify in items:
            modify = modify.as_str()
            mod_query, mods, dels = self.parse_modify(modify, model_cls)
            if mod_query:
                raise ui.UserError(u'modifyonimport.{0}["{1}"]: unexpected query `{2}` in value'.format(context, query, mod_query))
            elif not mods and not dels:
                raise ui.UserError(u'modifyonimport.{0}["{1}"]: no modifications found'.format(context, query))
            dbquery, _ = parse_query_string(util.as_string(query), model_cls)
            modifies.append((dbquery, mods, dels))
        return modifies

    def parse_modify(self, modify, model_cls):
        modify = util.as_string(modify)
        args = shlex_split(modify)
        query, mods, dels = modify_parse_args(decargs(args))
        return ' '.join(query), mods, dels

    def imported(self, session, task):
        objs = task.imported_items()
        if task.is_album:
            self.modify_objs(session.lib, [task.album], self.album_modifies, task.is_album)
            # Album modifications can alter the items
            for obj in objs:
                obj.load()

            for albumdbquery, modifies in self.album_item_modifies:
                if albumdbquery.match(task.album):
                    self.modify_objs(session.lib, objs, modifies, is_album=False)
        else:
            self.modify_objs(session.lib, objs, self.singleton_modifies, is_album=False)

    def modify_objs(self, lib, objs, modifies, is_album):
        model_cls = Album if is_album else Item
        changed = []
        for obj in objs:
            all_mods, all_dels = {}, {}
            for dbquery, mods, dels in modifies:
                if dbquery.match(obj):
                    all_mods.update(mods)
                    all_dels.update(dels)

            if all_mods or all_dels:
                obj_mods = {}
                for key, value in all_mods.items():
                    value = obj.evaluate_template(value)
                    obj_mods[key] = model_cls._parse(key, value)

                if print_and_modify(obj, obj_mods, all_dels) and obj not in changed:
                    changed.append(obj)

        with lib.transaction():
            for obj in changed:
                obj.store()

        return changed
