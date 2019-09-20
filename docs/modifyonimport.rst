Modify On Import Plugin
=======================

The ``modifyonimport`` plugin lets you define metadata changes to occur on
import when the specified queries match.

Configuration
-------------

To configure the plugin, make a ``modifyonimport:`` section in your
configuration file. The available options are:

- **modify_album**: A mapping from query to modifications to
  apply to the album being imported.
- **modify_album_items**: A mapping from album query to a mapping
  from item query to modifications to apply to the items in the album being
  imported.
- **modify_singleton**: A mapping from query to modifications to
  apply to a singleton item being imported.

Example::

    modifyonimport:
      modify_album:
        '': flexfield=1
        blank: 'albumartist=Foo'
      modify_album_items:
        blank:
          '250': artist=Modified
          'invalid': artist=ModifiedMore
        nothing:
          '250': artist=ModifiedNothing
      modify_singleton:
        '250': artist_sort=Bar artist_credit=Bar
