from optparse import Values
from re import split

from beets.library import Library
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs


def cmd_genres(lib: Library, opts: Values, args, config):
    query = decargs(args)
    results = lib.albums(query) if opts.album else lib.items(query)
    items = 'albums' if opts.album else 'tracks'

    genres = {}
    for r in results:
        if opts.multi:
            _genres = [s.strip() for s in split(r'[,;/]', r.genre)]
        else:
            _genres = [r.genre]

        for g in _genres:
            if g in genres.keys():
                genres[g] += 1
            else:
                genres[g] = 1

    for g in sorted(genres.keys()):
        genre = '<empty>' if g in ['', None] else g
        s = f'{genre} ({genres.get(g)} {items})' if opts.count else genre
        print(s)


class GenresPlugin(BeetsPlugin):
    def __init__(self):
        super(GenresPlugin, self).__init__()

    def commands(self):
        cmd = Subcommand("genres", help="prints a consolidated list of genres of the result of a query")
        cmd.parser.add_album_option()
        cmd.parser.add_option("-c", dest="count", action="store_true", help="count items")
        cmd.parser.add_option(
            "-m", dest="multi", action="store_true",
            help="allow multiple genres (split genre at comma, semicolon or slash and count individually)"
        )
        cmd.func = lambda lib, opts, args: cmd_genres(lib, opts, args, self.config)
        return [cmd]
