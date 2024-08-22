"""Support saved, named queries."""

from __future__ import absolute_import, division, print_function

from beets import config
from beets.dbcore import Query, types
from beets.library import Album, Item, parse_query_string
from beets.plugins import BeetsPlugin


class SavedQuery(Query):
    """
    A query that is saved by name and can be referenced by that name.
    """
    queries = None
    def __new__(cls, keyword, name, *args):
        return cls.queries[name]


class FactoryDict(dict):
    """
    A dictionary that creates missing values by calling a factory function
    with the key as an argument.
    """
    def __init__(self, factory, iterable=None, **kwargs):
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__(**kwargs)
        self.factory = factory

    def __missing__(self, name):
        self[name] =  value = self.factory(name)
        return value


class SavedQueriesPlugin(BeetsPlugin):
    """Support saved, named queries.

    Also support creation of Item/Album boolean fields for the query. Do not
    query the fields, as the performance is not great. Use the `query:NAME`
    query syntax for queries, and use the fields for inspection or a format
    string.
    """

    def __init__(self):
        super(SavedQueriesPlugin, self).__init__()

        self.config.add({
            'add_fields': True,
        })

        config.add({
            'item_queries': {},
            'album_queries': {},
        })

        self.item_query_objects = FactoryDict(self.parse_item_query)
        self.album_query_objects = FactoryDict(self.parse_album_query)

        class ItemSavedQuery(SavedQuery):
            queries = self.item_query_objects
        self.item_query = ItemSavedQuery

        class AlbumSavedQuery(SavedQuery):
            queries = self.album_query_objects
        self.album_query = AlbumSavedQuery

        self._log.debug('adding named item query `query`')
        self.item_queries = {'query': ItemSavedQuery}
        self._log.debug('adding named album query `album_query`')
        self.album_queries = {'album_query': AlbumSavedQuery}

        if self.config['add_fields'].get():
            self.item_types = {}
            self.template_fields = {}
            for name in config['item_queries'].keys():
                self._log.debug('adding item field {}', name)
                self.item_types[name] = types.BOOLEAN
                self.template_fields[name] = lambda item, name=name: self.item_query_objects[name].match(item)

            self.album_types = {}
            self.album_template_fields = {}
            for name in config['album_queries'].keys():
                self._log.debug('adding album field {}', name)
                self.album_types[name] = types.BOOLEAN
                self.album_template_fields[name] = lambda album, name=name: self.album_query_objects[name].match(album)

    def parse_item_query(self, name):
        if not config['item_queries'][name].exists():
            if config['album_queries'][name].exists():
                return self.parse_album_query(name)

        querystring = config['item_queries'][name].as_str()
        query, _ = parse_query_string(querystring, Item)
        return query

    def parse_album_query(self, name):
        querystring = config['album_queries'][name].as_str()
        query, _ = parse_query_string(querystring, Album)
        return query
