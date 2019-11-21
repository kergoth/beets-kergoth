# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2019-11-21

### Added

- Added advisory plugin
- Added inconsistentalbumtracks plugin
- Added nowrite plugin
- Added zeroalbum plugin
- Added prototype alternativesplaylist plugin
- Added prototype convertsingletons plugin
- Added prototype crossquery plugin
- modifyonimport: added configuration sanity checks
- modifytmpl: added up front checks for common user mistakes in field changes

### Changed

- modifyonimport: values are now interpreted as templates / path format strings, like the `modifytmpl` plugin
- modifyonimport: conversion to singleton is explicitly *unsupported*, use `convertsingletons`. Attempting to support this in this plugin caused a large number of problems.

### Fixed

- modifyonimport: fixed applying modifications to the album
- importinspect: fixed `ignored` field support
