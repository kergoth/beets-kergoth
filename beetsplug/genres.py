from optparse import Values

from beets.library import Library
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs

def cmd_genres(lib: Library, opts: Values, args, config):
    query = decargs(args)
    results = lib.albums(query) if opts.album else lib.items(query)
    items = 'albums' if opts.album else 'tracks'

    genres = {}
    for r in results:
        if r.genre in genres.keys():
            genres[r.genre] += 1
        else:
            genres[r.genre] = 1

    for g in sorted(genres.keys()):
        genre = '<empty>' if g in ['',None] else g
        s = f'{genre} ({genres.get(g)} {items})' if opts.count else genre
        print(s)

class GenresPlugin(BeetsPlugin):
    def __init__(self):
        super(GenresPlugin, self).__init__()

    def commands(self):
        cmd = Subcommand("genres", help="prints a consolidated list of genres of the result of a query" )
        cmd.parser.add_album_option()
        cmd.parser.add_option( "-c", dest="count", action="store_true", help="counts items" )
        cmd.func = lambda lib, opts, args: cmd_genres(lib, opts, args, self.config)
        return [cmd]
