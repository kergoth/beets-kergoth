from optparse import Values

from beets.library import Library
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs

def cmd_genres(lib: Library, opts: Values, args, config):
    query = decargs(args)
    results = lib.albums(query) if opts.album else lib.items(query)

    genres = set()
    [genres.add(r.genre) for r in results]

    for g in sorted(genres):
        print( '<empty genre>' ) if g == '' else print(g)

class GenresPlugin(BeetsPlugin):
    def __init__(self):
        super(GenresPlugin, self).__init__()

    def commands(self):
        cmd = Subcommand("genres", help="prints a consolidated list of genres of the result of a query" )
        cmd.parser.add_album_option()
        cmd.func = lambda lib, opts, args: cmd_genres(lib, opts, args, self.config)
        return [cmd]
