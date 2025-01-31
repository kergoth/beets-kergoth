Genres Plugin
====================

The ``genres`` plugin prints the genres of tracks or albums in alphabetical order.

Available options:

- ``-a``: album mode, looks at the genre of albums, if omitted uses the genre of tracks
- ``-c`` / ``--count``: appends the number of tracks or items to the genre list
- ``-m`` / ``--multi``: splits a genre based on comma, semicolon or slash and treats the result individually

Configuration
-------------

None for now.

Example Usage
-------------

Command-line::

    $ beet genres
    <empty genre>
    Electronic
    Pop/Dance
    Progressive Metal; Progressive Rock
    Rock, Metal
    Synthie Pop

    $ beet genres -m
    <empty genre>
    Dance
    Electronic
    Metal
    Pop
    Progressive Rock
    Progressive Metal
    Rock
    Synthie Pop

    $ beet genres -a Yello
    Electronic
    Synthie Pop

    $ beet genres -a -c Yello
    Electronic (3 albums)
    Synthie Pop (2 albums)

