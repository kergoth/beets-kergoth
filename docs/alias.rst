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
  An alias may also accept placeholders in the form of ``{0}``, ``{1}`` etc.
  These placeholders will be replaced by the provided arguments with the
  respective index. ``{0}`` will be replaced by parameter 0, ``{1}`` with
  parameter 1 and so on. There's a special placeholder ``{}`` which is used
  for parameters without a matching placeholder (see examples below). This
  is necessary to enable building aliases for beets commands with a variable
  number of arguments (like modify). If this placeholder does not exist, the
  parameters will be appended to the command.

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

        # Simple parameter expansion
        list-live: ls artist:{0} album:{1}
        # command: list-live yello live
        # expands to: beet ls artist:yello album:live

        # Expansion: more placeholders than parameters (command will probably fail)
        list-fail: ls artist:{0} album:{1}
        # command: beet list-fail yello
        # expands to: beet ls artist:yello album:{1}

        # Expansion: more parameters than placeholders, parameters appended
        list-live-2017a: ls year:{2}
        # command: beet list-live-2017a yello live 2017
        # expands to: beet ls year:2017 yello live

        # Expansion: more parameters than placeholders, parameters inserted
        list-live-2017b: ls {} year:{2}
        # command: beet list-live-2017b yello live 2017
        # expands to: beet ls yello live year:2017
        
        # Expansion: real-world example, modify all live albums by Yello
        set-genre-pop: modify -a {} genre={0}
        # command: beet "Synthie Pop" yello live
        # exapands to: beet modify -a yello live genre="Synthie Pop"

        # Mac-specific
        picard:
          command: '!open -A -a "MusicBrainz Picard"'
          help: Open items in MusicBrainz Picard
