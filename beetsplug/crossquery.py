"""Query albums/items whose items/album match a sub-query.

Note that this is not as performant as would be ideal, but gets the job done. Do
not use this unless it's truly necessary. Most album fields are also accessible
on the item, so use those directly when possible. This will become mostly
unnecessary once https://github.com/beetbox/beets/pull/2988 is merged.

Ex.
```
beet ls album_has:albumtotal:1
beet ls -a any_track_has:genre:foo
beet ls -a all_tracks_have:genre:foo
```

FIXME: rework to use a joined fetch with an inner join query based on the
matching sub-query.
"""

from __future__ import absolute_import, division, print_function

from itertools import groupby

from beets import config
from beets.dbcore import Query, MatchQuery, AndQuery, OrQuery
from beets.dbcore.query import NotQuery
from beets.library import Album, Item, parse_query_string
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
        return self.item_query.match(item)

    @classmethod
    def clear_cache(cls):
        if cls._cached_album_results:
            cls._cached_album_results = {}


class AnyTrackQuery(Query):
    """Query albums with at least one track matching a sub-query."""
    _cached_results = {}

    def __init__(self, query_string):
        self.query_string = query_string
        if self.query_string in self._cached_results:
            albums = self.albums = self._cached_results[self.query_string]
        else:
            query, _ = parse_query_string(query_string, Item)
            album_only_query = AndQuery([query, NotQuery(MatchQuery(u'album_id', 0))])
            items = self.lib.items(album_only_query)
            albums = set(i.album_id for i in items)
            self._cached_results[self.query_string] = self.albums = albums
        self.album_query = OrQuery([MatchQuery('id', id) for id in albums])

    def clause(self):
        return self.album_query.clause()

    def match(self, item):
        return self.album_query.match(item)

    @classmethod
    def clear_cache(cls):
        if cls._cached_results:
            cls._cached_results = {}


class AllTrackQuery(Query):
    """Query albums with at least one track matching a sub-query."""
    _cached_results = {}

    def __init__(self, query_string):
        self.query_string = query_string
        if self.query_string in self._cached_results:
            albums = self.albums = self._cached_results[self.query_string]
        else:
            query, _ = parse_query_string(query_string, Item)
            album_only_query = AndQuery([query, NotQuery(MatchQuery(u'album_id', 0))])
            items = self.lib.items(album_only_query)

            def item_album(i):
                return i.album_id

            items_by_album = sorted(items, key=item_album)
            grouped_items = groupby(items_by_album, item_album)
            albums = set()
            for album_id, items in grouped_items:
                items = list(items)
                album = items[0].get_album()
                all_items = album.items()
                if len(items) == len(all_items):
                    albums.add(album_id)

            self._cached_results[self.query_string] = self.albums = albums
        self.album_query = OrQuery([MatchQuery('id', id) for id in albums])

    def clause(self):
        return self.album_query.clause()

    def match(self, item):
        return self.album_query.match(item)

    @classmethod
    def clear_cache(cls):
        if cls._cached_results:
            cls._cached_results = {}


class CrossQueryPlugin(BeetsPlugin):
    def __init__(self):
        super(CrossQueryPlugin, self).__init__()

        class RealAlbumQuery(AlbumQuery):
            lib = _open_library(config)
            log = self._log

        self.item_queries = {'album_has': RealAlbumQuery}

        class RealAnyTrackQuery(AnyTrackQuery):
            lib = _open_library(config)
            log = self._log

        class RealAllTrackQuery(AllTrackQuery):
            lib = _open_library(config)
            log = self._log

        self.album_queries = {
            'any_track_has': RealAnyTrackQuery,
            'all_tracks_have': RealAllTrackQuery,
        }

        self.query_cls = [RealAlbumQuery, RealAnyTrackQuery]

        self.register_listener('pluginload', self.event_pluginload)
        self.register_listener('database_change', self.event_database_change)

    def event_pluginload(self):
        for cls in self.query_cls:
            cls.clear_cache()

    def event_database_change(self, lib, model):
        for cls in self.query_cls:
            cls.clear_cache()
