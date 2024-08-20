Tablelist Plugin
================

The ``tablelist`` plugin is a replacement for the built-in list command.
It works in a similar manner, but displays its output in a table rather
than in plain text.

Enable the ``tablelist`` plugin in your configuration (see
`using-plugins`) and use ``tablelist`` with item or album queries.
There is also an alias ``tls`` which saves some keystrokes on your keyboard.

Prerequisites
-------------

This plugin requires rich (https://github.com/Textualize/rich), you need to
install it via pip::
  pip install rich

Configuration
-------------

To configure the plugin, make a ``tablelist:`` section in your
configuration file. The available options are:

- **album_columns**: Whitespace separated list of fields to show in the table
  (in album mode).
  Default: ``albumartist album year``
- **item_columns**: Whitespace separated list of fields to show in the table
  (in item mode).
  Default: ``track title artist album year``
- **style**: Dictionary with styling options. The following options can be used
  inside this item:
- **box**: Name of the table box style. The naming follows the naming of available
  Rich styles (case being ignored). Existing styles are shown here:
  https://rich.readthedocs.io/en/latest/appendix/box.html#appendix-box
  Default: ``minimal``
- **show_header**: Flag for showing/hiding the table header.
  Default: ``true``

Example Configuration
---------------------

::

    tablelist:
      album_columns: id albumartist album year
      item_columns: track title artist album year disc disctotal
      style:
        box: heavy
        show_header: false
