"""Open media paths with external applications."""

import os
import subprocess

from beets import plugins, ui, util


class OpenPlugin(plugins.BeetsPlugin):
    def commands(self):
        open_cmd = ui.Subcommand(
            "open",
            help="Open media paths with external applications.",
        )
        open_cmd.parser.add_option(
            "-A",
            "--args",
            action="store",
            help="Additional arguments for the system-specific open command.",
        )
        open_cmd.parser.add_option(
            "-R",
            "--reveal",
            action="store_true",
            help="Open the parents of the paths, not the paths themselves.",
        )
        open_cmd.parser.add_all_common_options()
        open_cmd.func = self.open
        return [open_cmd]

    def open(self, lib, opts, args):
        query = ui.decargs(args)

        if opts.album:
            items = lib.albums(query)
        else:
            items = lib.items(query)

        if not items:
            raise ui.UserError("nothing to open")

        cmd = util.open_anything()
        if opts.args:
            cmd += " " + opts.args
        paths = [item.path for item in items]
        if opts.reveal:
            paths = [os.path.dirname(p) for p in paths]
        self._log.debug("invoking command: {} {}", cmd, subprocess.list2cmdline(paths))

        item_type = "album" if opts.album else "track"
        item_type += "s" if len(items) > 1 else ""
        if opts.reveal:
            action = "Revealing"
        else:
            action = "Opening"
        ui.print_(f"{action} {len(items)} {item_type}.")

        try:
            util.interactive_open(paths, cmd)
        except OSError as exc:
            raise ui.UserError(f"failed to invoke {cmd}: {exc}")
