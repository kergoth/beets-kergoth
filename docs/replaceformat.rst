Replace Format Plugin
=====================

The ``replaceformat`` plugin defines format functions for search/replace of
text, both single replacements and applications of a set of replacements like
the built in ``replace`` configuration option.

Available functions:

- ``replace``: apply a set of defined replacements to a string
- ``replace_path``: apply a set of defined replacements to a path,
  applying the replacements on a per-path-component basis
- ``sub``: apply a single search/replace to a string
- ``sub_path``: apply a single search/replace to a path, applying the
  replacement on a per-path-component basis

The ``replace_path`` function operates similarly to the built-in
``replace`` option, but uses a user-defined set of replacements
in a single case rather than globally to all paths.

Configuration
-------------

The ``replace`` and ``replace_path`` functions operate on a defined set of
replacements from the user configuration. Simply define a configuration section
with a mapping from search to replace, then reference this as the first
argument to the functions.

Examples::

    num_replace:
      '250': '500'
    path_replace:
      '^data': 'newdata'

    paths:
      default: '%replace_path{path_replace,$albumartist/%replace{num_replace,$album}/$artist - $title}'
      some_query:1: '$albumartist/$album/$artist - %sub{$title,Foo,Bar}'
