"""Run external scripts when beets events are fired."""

from __future__ import division, absolute_import, print_function

import glob
import os
import subprocess

from beets import config
from beets.plugins import BeetsPlugin
from beets.util import py3_path, bytestring_path


class HookScriptsPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add({
            'hookspath': [],
            'hooks': [],
            'args': {}
        })

        self.register_listener('library_opened', self.library_opened)

        paths = self.config['hookspath'].as_str_seq(split=False)
        paths = [py3_path(p) for p in paths]
        self.paths = paths

        self.hookenv = dict(os.environ)

        verbose = config['verbose'].get(int)
        if verbose:
            self.hookenv['BEETS_VERBOSE'] = str(verbose)

        hooks = self.config['hooks'].as_str_seq()
        self.hooks = hooks
        for hook in hooks:
            def hookfunc(hook=hook, **kwargs):
                args = self.get_args(hook, kwargs)
                self.hook(hook, args)
            self.register_listener(hook, hookfunc)

    def library_opened(self, lib):
        self.lib = lib

    def get_args(self, hook, kwargs):
        if hook in self.config['args']:
            argstring = self.config['args'][hook].get()
            if argstring:
                argstring = '[' + argstring + ']'
                args = eval(argstring, kwargs)
                self._log.debug(u'Arguments for {} hook processed from {} to {}'.format(hook, argstring, repr(args)))
                return args

    def get_hookscripts(self, hook):
        hooks = []
        for path in self.paths:
            if not os.path.isabs(path):
                path = py3_path(os.path.join(self.lib.directory, bytestring_path(path)))

            hookpath = os.path.join(path, hook)
            if os.path.exists(hookpath):
                hooks.append(hookpath)
            elif os.path.exists(hookpath + '.d'):
                hooks.extend(glob.glob(os.path.join(hookpath + '.d', '*')))
        return hooks

    def hook(self, hook, args):
        hooks = self.get_hookscripts(hook)
        for hookscript in hooks:
            cmd = [hookscript]
            if args:
                cmd.extend(args)
            self._log.info(u'Running {}'.format(subprocess.list2cmdline(cmd)))
            subprocess.check_call(cmd, shell=False, stdin=subprocess.DEVNULL, env=self.hookenv)
