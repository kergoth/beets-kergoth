Saved Formats Plugin
====================

The ``savedformats`` plugin lets you define saved, named format strings by
storing them in fields for later reference.

This is similar to inline, except we specify a format string, not python code.

Among other things, you can use this to reduce duplication in your ``paths`` or
``alternatives`` configuration, make it easier to append to the default
``format_album`` and ``format_item`` at the command-line, and avoid issues with
undefined or troublesome fields.

Enable the ``savedformats`` plugin in your configuration (see
`using-plugins`) and then define and use saved formats in config.yaml and use
them as you would any other field.

Configuration
-------------

To configure the plugin, make ``album_formats:`` or ```item_formats`` sections
in your configuration file. Every line defines a new field, with the key as the
field name and the value as a format string as is used in ``paths``.

Example Configurations
----------------------

::

    album_formats:
        album_id: '$id'

    item_formats:
        artist_title: '%the{$artist} - $title'

Ease additions to the default formats at a command-line:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration::

    item_formats:
      format_item: $artist - $album - $title

    album_formats:
      format_album: $albumartist - $album

    format_album: '$format_album'
    format_item: '$format_item'

Command-line::

    $ beet ls -a -f '$format_album $albumtotal'
    $ beet ls -f '$format_item via $source'

Avoid issues with undefined fields:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration::

    album_formats:
      e_data_source: '%ifdef{data_source}'

Command-line::

    # This shows an empty string instead of '$data_source' on albums where it's
    # not defined.
    $ beet ls -f '$format_album $e_data_source'

Ease working with a troublesome field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    types:
      missing_tracks: int

    album_formats:
      # This lets me use %if{$missing_tracks,foo} without the problems using
      # $missing causes due to being negative when track totals aren't set.
      missing_tracks: '%if{$albumtotal,$missing,0}'
