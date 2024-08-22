"""Run external scripts when beets events are fired."""

from __future__ import division, absolute_import, print_function
import abc
import collections

import glob
import os
import subprocess

from beets import config, ui
from beets import util
from beets.plugins import BeetsPlugin
from beets.util import py3_path, bytestring_path, syspath


class HookScriptsPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add({"hookspath": [], "hooks": [], "args": {}})

        self.register_listener("library_opened", self.library_opened)

        paths = self.config["hookspath"].as_str_seq(split=False)
        paths = [py3_path(p) for p in paths]
        self.paths = paths

        self.hookenv = dict(os.environ)

        verbose = config["verbose"].get(int)
        if verbose:
            self.hookenv["BEETS_VERBOSE"] = str(verbose)

        hooks = self.config["hooks"].as_str_seq()
        self.hooks = hooks
        for hook in hooks:

            def hookfunc(hook=hook, **kwargs):
                args = self.get_args(hook, kwargs)
                self.hook(hook, args)

            self.register_listener(hook, hookfunc)

        self.arg_encoding = util.arg_encoding()

    def library_opened(self, lib):
        self.lib = lib
        self.hookenv["BEETS_LIBRARY"] = self.lib.path
        self.hookenv["BEETS_DIRECTORY"] = self.lib.directory

    def get_args(self, hook, kwargs):
        if hook in self.config["args"]:
            argstring = self.config["args"][hook].get()
            if argstring:
                argstring = "[" + argstring + "]"
                args = eval(argstring, globals(), kwargs)
                args = list(flatten(args))
                for i, arg in enumerate(args):
                    if isinstance(arg, bytes):
                        arg = arg.decode("utf-8")
                    elif not isinstance(arg, str):
                        arg = str(arg)
                    args[i] = arg.encode(self.arg_encoding)
                self._log.debug(
                    "Arguments for {} hook processed from {} to {}".format(
                        hook, argstring, repr(args)
                    )
                )
                return args

    def get_hookscripts(self, hook):
        hooks = []
        for path in self.paths:
            if not os.path.isabs(path):
                path = py3_path(os.path.join(self.lib.directory, bytestring_path(path)))

            hookpath = os.path.join(path, hook)
            if os.path.exists(hookpath):
                hooks.append(hookpath)
            elif os.path.exists(hookpath + ".d"):
                hooks.extend(glob.glob(os.path.join(hookpath + ".d", "*")))
        return hooks

    def hook(self, hook, args):
        hooks = self.get_hookscripts(hook)
        for hookscript in hooks:
            self.run_hookscript(hookscript, args)

    def run_hookscript(self, hookscript, args):
        cmd = [hookscript] + args
        cmdstring = subprocess.list2cmdline(ui.decargs(cmd))
        self._log.info(f"Running {cmdstring}")
        try:
            subprocess.check_call(cmd, shell=False, stdin=subprocess.DEVNULL, env=self.hookenv)
        except subprocess.CalledProcessError as exc:
            raise ui.UserError(
                f"hookscripts: command {cmdstring} failed with exit status {exc.returncode}"
            )
        except OSError as exc:
            raise ui.UserError(f"hookscripts: couldn't invoke '{cmdstring}': {exc}")

def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from el
        else:
            yield el
