Import Inspect Plugin
=====================

The ``importinspect`` plugin lets you inspect the metadata changes to be
applied when importing.

This is particularly helpful when you have many candidates with similar
information, as it gives you enough detail to differentiate, for example the
total number of tracks, month/day, albumdisambig, etc. The display is the same
as that used by ``beet-modify`` and others.

Enable the ``importinspect`` plugin in your configuration (see
`using-plugins`) and then use ``beet import`` as usual.

Interactive Usage
-----------------

The ``importinspect`` plugin is invoked during an import session. If enabled,
it adds a new option to the user prompt::

    [A]pply, More candidates, Skip, Use as-is, as Tracks, Group albums, Enter search, enter Id, aBort, iNspect changes?

This option enables inspection of the changes to be applied by the specified
candidate. If the ``on_apply`` option is enabled (it is by default), selecting
``[A]pply`` will also show inspection output and prompt to accept the
modification.

Configuration
-------------

To configure the plugin, make an ``importinspect:`` section in your
configuration file. The available options are:

- **on_apply**: Enable inspection when applying a candidate. Default: ``yes``.
- **timid**: Enable a confirmation prompt when applying a candidate, after
  viewing the inspection. Defaults to the value of the beets ``timid`` option.
- **ignored**: A list of item fields to ignore.
- **ignored_new**: A list of fields to ignore only when they're new.
- **ignored_existing**: A list of fields to ignore only when they're not new.

Example Output
--------------

::

    Gary Go - Gary Go (Bonus Track Version)
    album: Gary Go (Bonus Track Version) -> Gary Go
    albumartist_credit:  -> Gary Go
    albumartist_sort:  -> Gary Go
    albumdisambig:  -> Exclusive Amazon MP3 version
    albumtype:  -> album
    day: 11 -> 15
    month: 08 -> 09
    original_day: 00 -> 25
    original_month: 00 -> 05
    original_year: 0000 -> 2009
    Gary Go (Bonus Track Version) - 04 - Gary Go - Wonderful
    artist_credit:  -> Gary Go
    tracktotal: 13 -> 12

Example Configuration
---------------------

::

    importinspect:
      on_apply: yes
      ignored: month day original_month original_day
      ignored_new:
        # When inspecting candidates, it's a given that release fields will
        # be added, and a number of these are shown already by the import interface,
        # so focus on non-release fields. Changes to existing release fields will still
        # be shown, as that's useful when retagging an existing item.
        - albumstatus
        - asin
        - barcode
        - catalognumber
        - catalognum
        - country
        - data_source
        - discogs_albumid
        - isrc
        - label
        - language
        - mb_albumartistid
        - mb_albumid
        - mb_artistid
        - mb_releasegroupid
        - mb_releasetrackid
        - mb_trackid
        - mb_workid
        - media
        - releasecountry
        - releasestatus
        - script

Screencast
----------

.. image:: ../images/importinspect.png
   :target: https://asciinema.org/a/1r3HoearzkY2A8QG417bVM5nR
