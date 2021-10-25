"""Define fields for the default list formats, format_album and format_item.

For example, this enables one to easily adjust the existing format to append an extra field, ie.:

    beet ls -f '$format_item [$existing/$albumtotal]'
"""

from __future__ import division, absolute_import, print_function

from beets import config
from beets.plugins import BeetsPlugin


class DefaultFormatsPlugin(BeetsPlugin):
    """Store the default item and album format strings in fields for easy reference."""

    def __init__(self):
        super(DefaultFormatsPlugin, self).__init__()

        self.format_item = config['format_item'].get()
        self.format_album = config['format_album'].get()

        self._log.debug('adding item field format_item')
        def format_item(item):
            return item.evaluate_template(self.format_item)
        self.template_fields['format_item'] = format_item

        self._log.debug('adding album field format_album')
        def format_album(album):
            return album.evaluate_template(self.format_album)
        self.album_template_fields['format_album'] = format_album
