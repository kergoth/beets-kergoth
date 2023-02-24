
from optparse import Values

from rich import box
from rich.console import Console
from rich.table import Table

from beets.dbcore.db import Results
from beets.library import Library
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs

from shlex import split

console = Console()

default_item_fmt = '$id $track $title $length $artist $album $year "$disc/$disctotal"'
default_album_fmt = '$id $albumartist $album $year $genre $mb_albumid'

def tablelist( lib: Library, opts: Values, args ):
    query = decargs( args )
    results = lib.albums( query=query ) if opts.album else lib.items( query=query )
    table = make_table( results, True ) if opts.album else make_table( results, False )
    console.print( table )

def make_table( results: Results, use_album_format: bool = False ) -> Table:
    table = Table( box=box.MINIMAL, show_header=False )
    field_list = split( default_album_fmt ) if use_album_format else split( default_item_fmt )
    for r in results:
        evaluated_field_list = [ r.evaluate_template( tmpl ) for tmpl in field_list ]
        table.add_row( *evaluated_field_list )
    return table

class TableListPlugin( BeetsPlugin ):

    def __init__(self):
        super(TableListPlugin, self).__init__()

    def commands(self):
        cmd = Subcommand( 'tablelist', help='lists items in a table', aliases='tls' )
        cmd.parser.add_all_common_options()
        cmd.func = tablelist
        return [cmd]
