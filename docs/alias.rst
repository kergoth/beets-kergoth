Alias Plugin
============

The ``alias`` plugin lets you define command aliases, much like git, and also
makes available any beet-prefixed commands in your ``PATH`` as well.

Enable the ``alias`` plugin in your configuration (see
`using-plugins`) and then run the new commands it creates.

You may also run the command to list the defined aliases::

    beet alias

Configuration
-------------

To configure the plugin, make an ``alias:`` section in your
configuration file. The available options are:

- **from_path**: Make beet-prefixed commands from ``PATH`` available.
  Default: ``yes``
- **aliases**: Map alias names to beets commands or external shell commands.
  External commands should start with ``!``. This mirrors the behavior of git.
  An alias may also be defined in an expanded form including help text.

Example Configuration
---------------------

::

    alias:
      from_path: yes
      aliases:
        singletons: ls singleton:true

        # $ beet get-config alias.aliases.singletons
        get-config: '!sh -c "for arg; do beet config | yq -r \".$arg\"; done" -'

        # Red flags
        empty-artist: ls artist::'^$'
        empty-album: ls album::'^$' singleton:false

        # Mac-specific
        picard:
          command: '!open -A -a "MusicBrainz Picard"'
          help: Open items in MusicBrainz Picard
