"""Define saved format strings by storing them in fields."""

from __future__ import division, absolute_import, print_function
from collections import defaultdict

from beets import config
from beets.library import Album
from beets.plugins import BeetsPlugin
from beets.util import functemplate
from beets.dbcore import types


class SavedFormatsPlugin(BeetsPlugin):
    """Define saved format strings by storing them in fields.

    Similar to inline, except we specify a format string, not code.
    """

    def __init__(self):
        super(SavedFormatsPlugin, self).__init__()

        config.add(
            {
                "item_formats": {},
                "album_formats": {},
            }
        )
        self.cache = defaultdict(lambda: defaultdict(dict))
        self.register_listener("database_change", self.database_change)
        self.register_listener("item_removed", self.item_removed)
        self.set_template_fields()

    def database_change(self, lib, model):
        self.dirty_item(model)
        if isinstance(model, Album):
            for model in model.items():
                self.dirty_item(model)

    def item_removed(self, item):
        self.dirty_item(item)

    def dirty_item(self, item):
        cache = self.cache[item.__class__]
        if item.id and item.id in cache:
            del cache[item.id]

    def set_template_fields(self):
        for name, cfgname, fieldsname in (
            ("item", "item_formats", "template_fields"),
            ("album", "album_formats", "album_template_fields"),
        ):
            for field, template in config[cfgname].items():
                self._log.debug(f"adding {name} field {field}")

                templatestr = template.as_str()
                template = functemplate.template(templatestr)

                def apply_item(item, field=field, template=template):
                    # I would like to pre-determine the field types up front,
                    # but there's no event that's fired after the plugin queries
                    # and fields are merged, so we wait until first use instead.
                    if item.id in self.cache:
                        if field in self.cache[item.id]:
                            return self.cache[item.id][field]

                    field_type = item._type(field)
                    value = self.cache[item.id][field] = field_type.parse(
                        item.evaluate_template(template)
                    )
                    return value

                fields = getattr(self, fieldsname)
                fields[field] = apply_item
