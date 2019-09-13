"""Apply modifications on album/item import."""

from __future__ import division, absolute_import, print_function

from beets import dbcore, ui, util
from beets.library import parse_query_string, Item, Album
from beets.plugins import BeetsPlugin
from beets.ui import decargs
from beets.ui.commands import modify_parse_args, modify_items
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
            modifies = self.get_modifies(self.config['modify_' + name].items(), model_cls)
            setattr(self, name + '_modifies', modifies)

        self.album_item_modifies = []
        for albumquery, itemmodifies in self.config['modify_album_items'].items():
            albumdbquery, _ = parse_query_string(util.as_string(albumquery), Album)
            modifies = self.get_modifies(itemmodifies.items(), Item)
            self.album_item_modifies.append((albumdbquery, modifies))

    def get_modifies(self, items, model_cls):
        modifies = []
        for query, modify in items:
            modify = modify.as_str()
            _, mods, dels = self.parse_modify(modify, model_cls)
            dbquery, _ = parse_query_string(util.as_string(query), model_cls)
            modifies.append((dbquery, mods, dels))
        return modifies

    def parse_modify(self, modify, model_cls):
        modify = util.as_string(modify)
        args = shlex_split(modify)
        query, mods, dels = modify_parse_args(decargs(args))
        query = util.as_string(' '.join(query))
        dbquery, _ = parse_query_string(query, model_cls)
        return dbquery, mods, dels

    def imported(self, session, task):
        if task.is_album:
            modifies = self.album_modifies
        else:
            modifies = self.singleton_modifies

        objs = task.imported_items()
        self.modify_objs(session.lib, objs, modifies, task.is_album)
        if task.is_album:
            for albumdbquery, modifies in self.album_item_modifies:
                if albumdbquery.match(task.album):
                    self.modify_objs(session.lib, task.album.items(), modifies, False)

    def modify_objs(self, lib, objs, modifies, is_album):
        for obj in objs:
            all_mods, all_dels = {}, {}
            for dbquery, mods, dels in modifies:
                if dbquery.match(obj):
                    all_mods.update(mods)
                    all_dels.update(dels)
            if all_mods or all_dels:
                idquery = dbcore.MatchQuery('id', obj.id)
                modify_items(lib, all_mods, all_dels, idquery, self.should_write, self.should_move, is_album, False)
