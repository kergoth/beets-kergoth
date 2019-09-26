"""Query items whose album matches a sub-query.

Ex. `beet ls album_has:albumtotal:1`
"""

from __future__ import absolute_import, division, print_function

from beets.dbcore import Query
from beets.library import Album, parse_query_string
from beets.plugins import BeetsPlugin


class AlbumQuery(Query):
    """Query items whose album matches a sub-query."""
    def __init__(self, query):
        self.query_string = query
        self.query, _ = parse_query_string(self.query_string, Album)

    def match(self, item):
        album = item.get_album()
        return self.query.match(album)


class QueryAlbumPlugin(BeetsPlugin):
    def __init__(self):
        super(QueryAlbumPlugin, self).__init__()

        self.item_queries = {'album_has': AlbumQuery}
