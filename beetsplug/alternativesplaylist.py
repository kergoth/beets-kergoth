from __future__ import division, absolute_import, print_function

import fnmatch
import os

import beets
from beets.util import bytestring_path, mkdirall, syspath
from beetsplug import playlist


class AlternativesPlaylistPlugin(beets.plugins.BeetsPlugin):
    def __init__(self):
        super(AlternativesPlaylistPlugin, self).__init__()
        self.config.add({
            'auto': True,
            'playlist_dir': '.',
            'relative_to': 'library',
            'is_relative': False,
        })

        if self.config['relative_to'].get() not in ['playlist', 'library']:
            self.relative_to = beets.util.bytestring_path(
                self.config['relative_to'].as_filename())
        else:
            self.relative_to = None
        self.is_relative = self.config['is_relative'].get()

        self.alternatives, self.playlist = None, None

        self.register_listener('pluginload', self.pluginload)
        if self.config['auto'].get():
            self.register_listener('alternatives_after_update', self.alternatives_after_update)

    def commands(self):
        spl_alt_update = beets.ui.Subcommand(
            'altplaylistupdate',
            help=u'update the playlists for alternatives. Playlist names may be '
            u'passed as arguments. This assumes the alt itself has already been updated.'
        )
        spl_alt_update.func = self.update_cmd
        return [spl_alt_update]

    def update_cmd(self, lib, opts, args):
        if not args:
            raise beets.ui.UserError('must specify alternative')
        args = beets.ui.decargs(args)
        alternative = args.pop(0)
        self.write_playlists(alternative, lib)

    def pluginload(self):
        for plugin in beets.plugins.find_plugins():
            if plugin.name == 'alternatives':
                self.alternatives = plugin
                self.alternatives.update = self.patch_alt_update
            elif plugin.name == 'playlist':
                self.playlist = plugin

        if not self.alternatives:
            raise beets.ui.UserError(
                'alternatives plugin is required for alternativesplaylist')
        if not self.playlist:
            raise beets.ui.UserError(
                'playlist plugin is required for alternativesplaylist')

    def write_playlists(self, alternative, lib):
        self._log.debug(f'alternativesplaylist: write_playlists({alternative})')
        for m3u in self.find_playlists():
            try:
                self.update_playlist(lib, alternative, m3u)
            except beets.util.FilesystemError:
                self._log.error('Failed to update playlist: {0}'.format(
                    beets.util.displayable_path(playlist)))

    def alternatives_after_update(self, alternative, lib):
        if 'playlists' in self.alternatives.config[alternative.name]:
            enabled = self.alternatives.config[alternative.name]['playlists'].get()
        else:
            enabled = True

        if enabled:
            self.write_playlists(alternative.name, lib)

    def find_playlists(self):
        playlist_dir = beets.util.syspath(self.playlist.playlist_dir)
        for file in find(playlist_dir):
            if fnmatch.fnmatch(file, '*.[mM]3[uU]') or fnmatch.fnmatch(file, '*.[mM]3[uU]8'):
                m3u = beets.util.bytestring_path(file)
                yield m3u

    def update_playlist(self, lib, alternative, m3u):
        config = self.alternatives.config[alternative]
        if 'directory' in config:
            alt_dir = config['directory'].as_str()
        else:
            alt_dir = alternative
        alt_dir = bytestring_path(alt_dir)
        if not os.path.isabs(syspath(alt_dir)):
            alt_dir = os.path.join(lib.directory, alt_dir)

        playlist_dir = beets.util.bytestring_path(self.playlist.playlist_dir)
        m3uname = os.path.relpath(m3u, playlist_dir)

        outm3u = os.path.join(self.playlist_dir(alternative, alt_dir), m3uname)
        self._log.info(f'Writing playlist {beets.util.displayable_path(outm3u)}')

        # Gather up the items in the playlist and map to the alternative
        m3ubase, _ = os.path.splitext(m3uname)
        query = playlist.PlaylistQuery('playlist', beets.util.as_string(m3ubase), False)
        pathmap = {}
        for item in lib.items(query):
            alt_path = item.get(f'alt.{alternative}')
            if alt_path:
                pathmap[beets.util.bytestring_path(item.path)] = beets.util.bytestring_path(alt_path)

        src_base_dir = beets.util.bytestring_path(
            self.playlist.relative_to if self.playlist.relative_to
            else os.path.dirname(m3u)
        )

        if not self.relative_to and self.config['relative_to'] == 'library':
            relative_to = beets.util.bytestring_path(alt_dir)
        else:
            relative_to = self.relative_to

        alt_base_dir = beets.util.bytestring_path(
            relative_to if relative_to
            else os.path.dirname(outm3u)
        )

        lines = []
        with open(m3u, mode='rb') as m3ufile:
            for line in m3ufile:
                srcpath = line.rstrip(b'\r\n')
                is_relative = not os.path.isabs(srcpath)
                if is_relative:
                    srcpath = os.path.join(src_base_dir, srcpath)
                srcpath = beets.util.normpath(srcpath)
                if not os.path.exists(srcpath):
                    self._log.error('Path {} in playlist {} does not exist', srcpath, m3uname)
                    continue

                newpath = pathmap.get(srcpath)
                if not newpath:
                    self._log.debug(
                        'Failed to map path {} in playlist {} for alt {}', srcpath, m3uname, alternative)
                    continue

                if is_relative or self.is_relative:
                    newpath = os.path.relpath(newpath, alt_base_dir)

                lines.append(line.replace(srcpath, newpath))

        if lines:
            mkdirall(outm3u)
            with open(outm3u, 'wb') as m3ufile:
                m3ufile.writelines(lines)

    def playlist_dir(self, alternative, alt_dir):
        playlist_dir = self.config['playlist_dir'].as_str()
        playlist_dir = bytestring_path(playlist_dir)
        if not os.path.isabs(syspath(playlist_dir)):
            playlist_dir = os.path.join(alt_dir, playlist_dir)
        return playlist_dir

    def patch_alt_update(self, lib, options):
        """Tweaked update method for alternatives to send events."""
        try:
            alt = self.alternatives.alternative(options.name, lib)
        except KeyError as e:
            raise beets.ui.UserError(f"Alternative collection '{e.args[0]}' not found.")
        beets.plugins.send('alternatives_before_update', alternative=alt, lib=lib)
        alt.update(create=options.create)
        beets.plugins.send('alternatives_after_update', alternative=alt, lib=lib)


def find(dir, dirfilter=None, **walkoptions):
    """ Given a directory, recurse into that directory,
    returning all files as absolute paths. """

    for root, dirs, files in os.walk(dir, **walkoptions):
        if dirfilter is not None:
            for d in dirs:
                if not dirfilter(d):
                    dirs.remove(d)

        for file in files:
            yield os.path.join(root, file)
