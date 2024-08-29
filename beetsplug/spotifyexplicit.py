from collections import defaultdict
import re

from beets import ui
from beets import library
from beets import plugins
from beets.ui import commands


class SpotifyExplicitPlugin(plugins.BeetsPlugin):
    def commands(self):
        for plugin in plugins.find_plugins():
            if plugin.name == 'spotify':
                self.spotify = plugin
                break
        else:
            raise ui.UserError('spotify plugin is required')

        def set_advisory(lib, opts, args):
            self.spotify.config['show_failures'] = True

            args = ui.decargs(args)
            items = lib.items(args)
            results, failures = self.query_spotify(items)
            if results:
                modify_items, modify_albums = defaultdict(dict), {}

                if failures:
                    self._log.warning(
                        '{} track(s) did not match a {} ID\n',
                        len(failures),
                        self.spotify.data_source,
                    )

                for item, track in results.items():
                    if track['explicit']:
                        advisory = 1
                    elif item.get('advisory', 0) != 2:
                        advisory = 0
                    else:
                        # Trust that the clean advisory is accurate
                        continue

                    modify_items[advisory][item.id] = item
                    if advisory == 1 and item.album and item._cached_album:
                        # FIXME: implement removal of albumadvisory if not explicit for this or other tracks
                        album = item._cached_album
                        modify_albums[album.id] = album

                for advisory, mod_items in modify_items.items():
                    if advisory:
                        mods, dels = {'advisory': advisory}, None
                    else:
                        mods, dels = None, ['advisory']
                    modify_objs(lib, mods, dels, mod_items.values(), ui.should_write(opts.write),
                                ui.should_move(opts.move), opts.pretend, False, not opts.yes)

                if modify_albums:
                    modify_objs(lib, {'albumadvisory': 1}, None, modify_albums.values(), ui.should_write(opts.write),
                                ui.should_move(opts.move), opts.pretend, True, not opts.yes)

        cmd = ui.Subcommand(
            'spotify-set-advisory', help=u'Set parental advisory fields from Spotify explicit track information.'
        )
        cmd.parser.add_option(
            '-m', '--move', action='store_true', dest='move',
            help="move files in the library directory"
        )
        cmd.parser.add_option(
            '-M', '--nomove', action='store_false', dest='move',
            help="don't move files in library"
        )
        cmd.parser.add_option(
            '-w', '--write', action='store_true', default=None,
            help="write new metadata to files' tags (default)"
        )
        cmd.parser.add_option(
            '-W', '--nowrite', action='store_false', dest='write',
            help="don't write metadata (opposite of -w)"
        )
        cmd.parser.add_option(
            '-p', '--pretend', action='store_true',
            help="show all changes but do nothing"
        )
        cmd.parser.add_option(
            '-y', '--yes', action='store_true',
            help='skip confirmation'
        )
        cmd.func = set_advisory
        return [cmd]

    def query_spotify(self, items):
        # FIXME: Copied from spotify.py so we can map item to result
        results_map, failures_map = {}, {}

        for item in items:
            # Apply regex transformations if provided
            for regex in self.spotify.config['regex'].get():
                if (
                    not regex['field']
                    or not regex['search']
                    or not regex['replace']
                ):
                    continue

                value = item[regex['field']]
                item[regex['field']] = re.sub(
                    regex['search'], regex['replace'], value
                )

            # Custom values can be passed in the config (just in case)
            artist = item[self.spotify.config['artist_field'].get()]
            album = item[self.spotify.config['album_field'].get()]
            keywords = item[self.spotify.config['track_field'].get()]

            # Query the Web API for each track, look for the items' JSON data
            query_filters = {'artist': artist, 'album': album}
            response_data_tracks = self.spotify._search_api(
                query_type='track', keywords=keywords, filters=query_filters
            )
            if not response_data_tracks:
                query = self.spotify._construct_search_query(
                    keywords=keywords, filters=query_filters
                )
                failures_map[item] = query
                continue

            # Apply market filter if requested
            region_filter = self.spotify.config['region_filter'].get()
            if region_filter:
                response_data_tracks = [
                    track_data
                    for track_data in response_data_tracks
                    if region_filter in track_data['available_markets']
                ]

            if (
                len(response_data_tracks) == 1
                or self.spotify.config['tiebreak'].get() == 'first'
            ):
                self._log.debug(
                    '{} track(s) found, count: {}',
                    self.spotify.data_source,
                    len(response_data_tracks),
                )
                chosen_result = response_data_tracks[0]
            else:
                # Use the popularity filter
                self._log.debug(
                    'Most popular track chosen, count: {}',
                    len(response_data_tracks),
                )
                chosen_result = max(
                    response_data_tracks, key=lambda x: x['popularity']
                )
            results_map[item] = chosen_result

        return results_map, failures_map

def modify_objs(lib, mods, dels, objs, write, move, pretend, album, confirm):
    model_cls = library.Album if album else library.Item
    if mods is None:
        mods = {}
    if dels is None:
        dels = tuple()

    # Apply changes *temporarily*, preview them, and collect modified
    # objects.
    ui.print_(f"Modifying {len(objs)} {u'album' if album else u'item'}s.")
    changed = []
    for obj in objs:
        obj_mods = {}
        for key, value in mods.items():
            if isinstance(value, str):
                value = model_cls._parse(key, value)
            obj_mods[key] = value

        if commands.print_and_modify(obj, obj_mods, dels) and obj not in changed:
            changed.append(obj)

    # Still something to do?
    if not changed:
        ui.print_(u'No changes to make.')
        return
    elif pretend:
        return

    # Confirm action.
    if confirm:
        if write and move:
            extra = u', move and write tags'
        elif write:
            extra = u' and write tags'
        elif move:
            extra = u' and move'
        else:
            extra = u''

        changed = ui.input_select_objects(
            f'Really modify{extra}', changed,
            lambda o: commands.print_and_modify(o, mods, dels)
        )

    # Apply changes to database and files
    with lib.transaction():
        for obj in changed:
            obj.try_sync(write, move)
