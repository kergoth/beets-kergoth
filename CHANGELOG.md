# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- alias: also pull from a toplevel aliases section of the config.
- alias: parameter expansion support, thanks to fortysix2ahead!
- defaultformats: add new plugin. This stores the `item_format` and `album_format` as fields, which lets you extend the default formats at the command-line, rather than having to duplicate them. For example, `beet ls -f '$item_format | $genre'`.
- hookscripts: add new plugin. This just eases execution of external scripts based on hooks. I don't know if I'll be keeping this one in the long term.
- inlinehook: allow extension of argspecs in the config, to support custom plugin events.
- open: add new plugin. This adds a command to open items with the appropriate platform-specific method, such as `xdg-open` on Linux, or `open` on macOS.
- pathfield: add new plugin. By default, field expansion in a path format will replace any `/` characters, to ensure that the field only affects a single path component, rather than adding new subdirectories. This plugin allows you to work around that if you want to do otherwise, through substitution and two template functions.
- replacefunc: add new plugin. This is intended as a more convenience replaceformat.

### Removed

- modifytmpl: remove this plugin. beets modify supports format strings natively now.

### Changed

- Add caching in a few places for a minor performance improvement
- last_import: also add to album items
- spotifyexplicit: rework as a spotify-set-advisory command

### Fixed

- A variety of very minor and cosmetic fixes
- Fixed compatibility issues with beets 2.0
- Various minor fixes for the tests

## [0.4.0] - 2019-11-21

### Added

- Added advisory plugin
- Added inconsistentalbumtracks plugin
- Added nowrite plugin
- Added prototype alternativesplaylist plugin
- Added prototype convertsingletons plugin
- Added prototype crossquery plugin
- Added zeroalbum plugin
- alias: send events on success/failure
- modifyonimport: added configuration sanity checks
- modifytmpl: added up front checks for common user mistakes in field changes
- spotifyexplicit: send an event for each explicit track

### Changed

- modifyonimport: values are now interpreted as templates / path format strings, like the `modifytmpl` plugin
- modifyonimport: conversion to singleton is explicitly *unsupported*, use `convertsingletons`. Attempting to support this in this plugin caused a large number of problems.

### Fixed

- modifyonimport: fixed applying modifications to the album
- importinspect: fixed `ignored` field support
