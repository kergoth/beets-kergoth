from optparse import Values

from beets.dbcore.db import Results
from beets.library import Library
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs
from confuse import ConfigError, Configuration
from rich import box
from rich.console import Console
from rich.table import Table

# from shlex import split

console = Console()

default_item_fmt = '$id $track $title $length $artist $album $year "$disc/$disctotal"'
default_album_fmt = "$id $albumartist $album $year $genre $mb_albumid"


def cmd_tablelist(lib: Library, opts: Values, args, config):
    query = decargs(args)
    results = lib.albums(query) if opts.album else lib.items(query)

    table = make_table(results, config, use_album_format=opts.album)
    console.print(table)


def make_style(config: Configuration) -> dict:
    cfg = {}

    try:
        cfg["box"] = getattr(box, config["style"]["box"].get(str).upper())
    except AttributeError:
        print("warning: invalid box style")
        cfg["box"] = box.MINIMAL

    cfg["show_header"] = config["style"]["show_header"].get(bool)
    cfg["row_styles"] = ["", "dim"]

    return cfg


def make_table(
    results: Results, config: Configuration, use_album_format: bool = False
) -> Table:
    table_style = make_style(config)
    table = Table(**table_style)

    fields = (
        config["album_columns"].get(str)
        if use_album_format
        else config["item_columns"].get(str)
    )
    fields = [f for f in fields.split()]
    fields_tmpl = ["${}".format(f) for f in fields]

    # add header
    if table_style["show_header"]:
        if use_album_format:
            cfg = config["album_heading"]
        else:
            cfg = config["item_heading"]

        if cfg.exists():
            heading = cfg.as_str_seq()
            if len(heading) != len(fields):
                prefix = "album_" if use_album_format else "item_"
                raise ConfigError(
                    f"{prefix}columns and {prefix}heading must have the same number of elements"
                )
            [table.add_column(c) for c in heading]
        else:
            [table.add_column(c) for c in fields]

    # make actual table
    [
        table.add_row(*[r.evaluate_template(tmpl) for tmpl in fields_tmpl])
        for r in results
    ]

    return table


class TableListPlugin(BeetsPlugin):
    def __init__(self):
        super(TableListPlugin, self).__init__()

        # default config
        self.config.add(
            {
                "album_columns": "albumartist album year",
                "item_columns": "track title artist album year",
                "style": {
                    "box": "minimal",
                    "show_header": True,
                },
            }
        )

    def commands(self):
        cmd = Subcommand("tablelist", help="lists items in a table", aliases="tls")
        cmd.parser.add_all_common_options()
        cmd.func = lambda lib, opts, args: cmd_tablelist(lib, opts, args, self.config)
        return [cmd]
