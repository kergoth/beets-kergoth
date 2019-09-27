"""Query items whose album matches a sub-query.

Note that this is not as performant as would be ideal, but gets the job done. Do
not use this unless it's truly necessary. Most album fields are also accessible
on the item, so use those directly when possible. This will become entirely
unnecessary once https://github.com/beetbox/beets/pull/2988 is merged.

Ex. `beet ls album_has:albumtotal:1`

FIXME: rework to use a joined fetch with an inner join query based on the
matching albums
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
            albums = self.albums = self._cached_album_results[self.query_string]
        else:
            query, _ = parse_query_string(query_string, Album)
            albums = self.lib.albums(query)
            self._cached_album_results[self.query_string] = self.albums = albums
        self.item_query = OrQuery([MatchQuery('album_id', album.id) for album in albums])

    def clause(self):
        return self.item_query.clause()

    def match(self, item):
        return self.item_query.match()

    @classmethod
    def clear_cache(cls):
        if cls._cached_album_results:
            cls._cached_album_results = {}


class QueryAlbumPlugin(BeetsPlugin):
    def __init__(self):
        super(QueryAlbumPlugin, self).__init__()

        class RealAlbumQuery(AlbumQuery):
            lib = _open_library(config)
            log = self._log

        self.query_cls = RealAlbumQuery

        self.register_listener('pluginload', self.event_pluginload)
        self.register_listener('database_change', self.event_database_change)

        self.item_queries = {'album_has': RealAlbumQuery}

    def event_pluginload(self):
        self.query_cls.clear_cache()

    def event_database_change(self, lib, model):
        self.query_cls.clear_cache()
