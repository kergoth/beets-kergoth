Saved Queries Plugin
====================

The ``savedqueries`` plugin lets you save queries by name for later use.

Enable the ``savedqueries`` plugin in your configuration (see `using-plugins`)
and then define and use saved queries with the ``query:`` and ``album_query:``
prefixes.

Configuration
-------------

To configure the plugin, make ``album_queries:`` or ```item_queries`` sections
in your configuration file. Every line defines a new query, with the key as the
name and the value as a query string.

Example Usage
-------------

Configuration::

    album_queries:
      is_various_not_comp: 'comp:0 albumartist:@"Various Artists"'

    item_queries:
      is_live: 'albumtype:live'
      is_soundtrack: 'genre:soundtrack , albumtype:soundtrack'

Command-line::

    $ beet ls -a album_query:is_various_not_comp
    $ beet ls \^query:is_live
