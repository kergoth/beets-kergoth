"""Query items whose album matches a sub-query.

Ex. `beet ls album_has:albumtotal:1`

FIXME: invalidate the cache as needed, and ideally rework to use a joined fetch
with an inner join query based on the matching albums, if possible.
"""

from __future__ import absolute_import, division, print_function

from beets import config
from beets.dbcore import Query, MatchQuery, OrQuery
from beets.library import Album, parse_query_string
from beets.plugins import BeetsPlugin
from beets.ui import _open_library


class AlbumQuery(Query):
    """Query items whose album matches a sub-query."""
    _cached_album_results = {}

    def __init__(self, query_string):
        self.query_string = query_string
        if self.query_string in self._cached_album_results:
            self.albums = self._cached_album_results[self.query_string]
        else:
            query, _ = parse_query_string(query_string, Album)
            self.albums = self.lib.albums(query)
        self.item_query = OrQuery([MatchQuery('album_id', album.id) for album in self.albums])

    def clause(self):
        return self.item_query.clause()

    def match(self, item):
        return self.item_query.match()


class QueryAlbumPlugin(BeetsPlugin):
    def __init__(self):
        super(QueryAlbumPlugin, self).__init__()

        class RealAlbumQuery(AlbumQuery):
            lib = _open_library(config)
            log = self._log

        self.item_queries = {'album_has': RealAlbumQuery}
