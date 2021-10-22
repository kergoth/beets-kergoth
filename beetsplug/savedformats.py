"""Define saved format strings by storing them in fields."""

from __future__ import division, absolute_import, print_function

from beets import config
from beets.plugins import BeetsPlugin
from beets.library import Album, Item


class SavedFormatsPlugin(BeetsPlugin):
    """Define saved format strings by storing them in fields.

    Similar to inline, except we specify a format string, not code.
    """

    def __init__(self):
        super(SavedFormatsPlugin, self).__init__()

        config.add({
            'item_formats': {},
            'album_formats': {},
        })
        self.set_template_fields()

    def set_template_fields(self):
        for field, template in config['item_formats'].items():
            self._log.debug('adding item field {}', field)

            template = template.as_str()

            def apply_item(item, field=field, template=template):
                value = item.evaluate_template(template)
                return item._type(field).parse(value)
            self.template_fields[field] = apply_item

        for field, template in config['album_formats'].items():
            self._log.debug('adding album field {}', field)

            template = template.as_str()

            def apply_album(album, field=field, template=template):
                value = album.evaluate_template(template)
                return album._type(field).parse(value)
            self.album_template_fields[field] = apply_album
