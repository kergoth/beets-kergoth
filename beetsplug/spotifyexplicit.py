from beets import ui
from beets import plugins


class SpotifyExplicitPlugin(plugins.BeetsPlugin):
    def commands(self):
        for plugin in plugins.find_plugins():
            if plugin.name == 'spotify':
                self.spotify = plugin
                break
        else:
            raise ui.UserError('spotify plugin is required')

        def explicits(lib, opts, args):
            args = ui.decargs(args)
            items = lib.items(args)
            results = self.spotify._match_library_tracks(lib, args)
            if results:
                for item, track in zip(items, results):
                    if track['explicit']:
                        title = track['name']
                        album = track['album']['name']
                        artist = track['artists'][0]['name']
                        tracknum = track['track_number']
                        url = track['external_urls']['spotify']
                        plugins.send("spotify_explicit_track", lib=lib, track=track, item=item)
                        print('{} - {} - {} - {} - {}'.format(album, tracknum, artist, title, url))

        explicit_cmd = ui.Subcommand(
            'spotify-explicit', help=u''
        )
        explicit_cmd.parser.add_all_common_options()
        explicit_cmd.func = explicits
        return [explicit_cmd]
