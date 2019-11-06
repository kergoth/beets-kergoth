"""Smart playlists for alternatives."""
from __future__ import absolute_import, division, print_function

import os

import beets
from beets.dbcore import AndQuery
from beets.dbcore.query import NoneQuery, NotQuery
from beets.plugins import BeetsPlugin, find_plugins
from beets.ui import Subcommand, UserError, decargs
from beets.util import (bytestring_path, mkdirall, normpath, path_as_posix,
                        sanitize_path, syspath)
from confuse import Filename


class SplAlternatives(BeetsPlugin):
    def __init__(self):
        super(SplAlternatives, self).__init__()

        self.config.add({
            'auto': True,
            'forward_slash': False,
            'playlist_dir': '_Playlists',
        })

        self.alternatives, self.smartplaylist = None, None

        self.register_listener('pluginload', self.pluginload)
        if self.config['auto'].get():
            self.register_listener(
                'alternatives_after_update_with_lib', self.alternatives_after_update)

    def commands(self):
        spl_alt_update = Subcommand(
            'splaltupdate',
            help=u'update the smart playlists for alternatives. Playlist names may be '
            u'passed as arguments. This assumes the alt itself has already been updated.'
        )
        spl_alt_update.func = self.update_cmd
        return [spl_alt_update]

    def update_cmd(self, lib, opts, args):
        self.smartplaylist.build_queries()
        if not args:
            raise UserError('must specify alternative')

        args = decargs(args)
        alternative = args.pop(0)
        if args:
            for a in args:
                if not a.endswith(".m3u"):
                    args.add("{0}.m3u".format(a))

            playlists = set((name, q, a_q)
                            for name, q, a_q in self.smartplaylist._unmatched_playlists
                            if name in args)
            if not playlists:
                raise UserError(
                    u'No playlist matching any of {0} found'.format(
                        [name for name, _, _ in self.smartplaylist._unmatched_playlists])
                )

            self._matched_playlists = playlists
            self._unmatched_playlists = self.smartplaylist._unmatched_playlists - playlists
        else:
            self._matched_playlists = self.smartplaylist._unmatched_playlists
            self._unmatched_playlists = self.smartplaylist._unmatched_playlists

        self.update_playlists(lib, alternative)

    def pluginload(self):
        for plugin in find_plugins():
            if plugin.name == 'alternatives':
                self.alternatives = plugin
                self.alternatives.update = self.patch_alt_update
            elif plugin.name == 'smartplaylist':
                self.smartplaylist = plugin

        if not self.alternatives:
            raise UserError(
                'alternatives plugin is required for splalternatives')
        if not self.smartplaylist:
            raise UserError(
                'smartplaylist plugin is required for splalternatives')

    def alternatives_after_update(self, alternative, lib):
        """Update smart playlists after an alternative is updated."""

        self._log.warning('alternative_after_update({})'.format(alternative))
        self.smartplaylist.build_queries()
        self._matched_playlists = self.smartplaylist._unmatched_playlists
        self.update_playlists(lib, alternative)

    def update_playlists(self, lib, alternative):
        """Copied and modified method from smartplaylists to operate relative to the alt."""
        self._log.info(u"Updating {0} smart playlists...",
                       len(self._matched_playlists))

        playlist_dir = self.playlist_dir(alternative)

        # Maps playlist filenames to lists of track filenames.
        m3us = {}

        HasAltPath = NotQuery(NoneFieldQuery('alt.{}'.format(alternative), fast=False))
        for playlist in sorted(self._matched_playlists):
            name, (query, q_sort), (album_query, a_q_sort) = playlist
            self._log.debug(u"Creating playlist {0}", name)
            items = []

            if query:
                query = AndQuery([HasAltPath, query])
                items.extend(lib.items(query, q_sort))
            if album_query:
                album_query = AndQuery([HasAltPath, album_query])
                for album in lib.albums(album_query, a_q_sort):
                    items.extend(album.items())

            # As we allow tags in the m3u names, we'll need to iterate through
            # the items and generate the correct m3u file names.
            for item in items:
                m3u_name = item.evaluate_template(name, True)
                m3u_name = sanitize_path(m3u_name, lib.replacements)
                if m3u_name not in m3us:
                    m3us[m3u_name] = []

                item_path = item.get('alt.{}'.format(alternative))
                if item_path:
                    m3u_path = normpath(os.path.join(playlist_dir, bytestring_path(m3u_name)))
                    item_path = os.path.relpath(bytestring_path(item_path), os.path.dirname(m3u_path))
                    if item_path not in m3us[m3u_name]:
                        m3us[m3u_name].append(item_path)

        self.write_playlists(m3us, playlist_dir)

        self._log.info(u"{0} playlists updated", len(
            self._matched_playlists))

    def write_playlists(self, m3us, playlist_dir):
        """Write playlists to disk."""
        for m3u in m3us:
            m3u_path = normpath(os.path.join(playlist_dir,
                                             bytestring_path(m3u)))
            mkdirall(m3u_path)
            with open(syspath(m3u_path), 'wb') as f:
                for path in m3us[m3u]:
                    if self.config['forward_slash'].get():
                        path = path_as_posix(path)
                    f.write(path + b'\n')

    def playlist_dir(self, alternative):
        alt_dir = self.alternatives.config[alternative]['directory'].as_filename()
        playlist_dir = self.config['playlist_dir'].get(Filename(cwd=alt_dir))
        playlist_dir = bytestring_path(playlist_dir)
        return playlist_dir

    def patch_alt_update(self, lib, options):
        """Tweaked update method for alternatives to send events with the lib object."""
        try:
            alt = self.alternatives.alternative(options.name, lib)
        except KeyError as e:
            raise UserError(u"Alternative collection '{0}' not found."
                            .format(e.args[0]))
        beets.plugins.send('alternatives_before_update', alternative=alt)
        beets.plugins.send(
            'alternatives_before_update_with_lib', alternative=alt, lib=lib)
        alt.update(create=options.create)
        beets.plugins.send('alternatives_after_update_with_lib',
                           alternative=alt, lib=lib)
        beets.plugins.send('alternatives_after_update', alternative=alt)


class NoneFieldQuery(NoneQuery):
    """Match fields which aren't set / are None."""
    def match(self, item):
        try:
            return item[self.field] is None
        except KeyError:
            return True
