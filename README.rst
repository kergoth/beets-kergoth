beets-kergoth
=============

This is my personal collection of beets_ plugins that are not currently being
distributed separately.

Generally useful
----------------

These plugins I consider to be useful in general and polished enough that I
intend to either submit them upstream to beets or split off into separate
projects / python packages.

- The `Alias Plugin`_ lets you define command aliases, much like git, and also
  makes available any beet-prefixed commands in your ``PATH`` as well.
- The `Import Inspect Plugin`_ lets you inspect the metadata changes to be
  applied when importing.
- The `Genres Plugin`_ simply displays the genres of tracks or albums in
  alphabetical order
- The `Modify On Import Plugin`_ lets you define metadata changes to occur
  on import when the specified queries match.
- The `Replace Format Plugin`_ defines format functions for search/replace of
  text, both single replacements and applications of a set of replacements
  like the built in ``replace`` configuration option.
- The `Saved Formats Plugin`_ lets you define saved, named format strings by
  storing them in fields for later reference.
- The `Saved Queries Plugin`_ lets you save queries by name for later use.
- The `Tablelist Plugin`_ lists items in a table format, as an alternative to list.

Special Purpose
---------------

These plugins are useful to me, but probably not to anyone else.

- The ``musicsource`` plugin just forces me to define a ``source`` field when
  importing new music, as this is how I organize my library. ``source`` is
  where the music was acquired, e.g. Amazon, iTunes, Google, etc.
- The ``picard`` plugin lets me launch MusicBrainz Picard with the items I'm
  importing, either to use it to tag rather than beets, or as an inspection
  tool to examine its metadata. This assumes a ``picard`` beets command
  exists, as this is how it runs it.
- The ``reimportskipfields`` plugin lets you specify fields from set_fields
  to also be applied to skipped items on reimport. I use this to facilitate
  resuming from a reimport, as it lets me apply a ``reimported`` field to
  anything I tried to reimport, whether I was able to match it to a candidate
  or not.

Prototype / Proof of Concept plugins
------------------------------------

These plugins were thrown together in experimentation. Some may be worth
cleaning up, but others are useful pretty rarely.

- The ``abcalc`` plugin performs the same calculation as absubmit, but runs it
  only against non-MusicBrainz tracks, and stores the low level values rather
  than submitting them. I've used this to populate the acoustic fingerprint
  tags for use by external de-duplication scripts.
- The ``advisory`` plugin sets ``advisory`` and ``albumadvisory`` flexible
  fields, on import, based on the ``itunesadvisory`` tag in the files.
- The ``existingqueries`` plugin adds a couple queries that originated in the
  beets source.
- The ``hasart`` plugin adds a query to check for embedded album art.
- The ``inconsistentalbumtracks`` plugin identifies albums whose tracks have
  inconsistent album fields.
- The ``inlinehook`` plugin lets you define hooks inline in config.yaml with
  python, much the way ``inline`` does for fields.
- The ``last_import`` plugin keeps track of the most recently imported items
  with a flexible field.
- The ``modifytmpl`` plugin lets you define fields using templates / format
  strings. This will be going upstream into the main ``modify`` command.
- The ``nowrite`` plugin blocks writes/moves of items in the library, which is
  particularly useful in testing beets or testing changes to beets without
  mucking up your existing library.
- The ``otherqueries`` plugin defines other random queries of questionable
  usefulness at this time.
- The ``crossquery`` plugin lets you query albums/items whose items/album
  match a sub-query.
- The ``spotifyexplicit`` plugin uses the ``spotify`` plugin to look up items
  from my library, determines if Spotify considers these items as explicit
  tracks (Parental Advisory), and prints them if so. I use this to set an
  ``advisory`` field on my tracks.
- The ``zeroalbum`` plugin clears fields in albums in the database, obeying
  the 'zero' plugin configuration.


.. _beets: http://beets.io/
.. _Alias Plugin: docs/alias.rst
.. _Import Inspect Plugin: docs/importinspect.rst
.. _Genres Plugin: docs/genres.rst
.. _Modify On Import Plugin: docs/modifyonimport.rst
.. _Replace Format Plugin: docs/replaceformat.rst
.. _Saved Formats Plugin: docs/savedformats.rst
.. _Saved Queries Plugin: docs/savedqueries.rst
.. _Tablelist Plugin: docs/tablelist.rst
