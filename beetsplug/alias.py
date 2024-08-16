"""Support for beets command aliases, not unlike git.

By default, also checks $PATH for beet-* and makes those available as well.

Example:

    alias:
      from_path: yes # Default
      aliases:
        singletons: ls singleton:true
        external-cmd-test: '!echo'
        sh-c-test: '!sh -c "echo foo bar arg1:$1, arg2:$2" sh-c-test'
        with-help-text:
          command: ls -a
          help: do something or other
"""

from __future__ import division, absolute_import, print_function

import confuse
import glob
import optparse
import os
import shlex
import six
import subprocess
import sys

from beets import config, plugins, ui
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, print_
from beets.ui.commands import default_commands

if sys.version_info >= (3, 3):
    from collections import abc
else:
    import collections as abc


class NoOpOptionParser(optparse.OptionParser):
    def parse_args(self, args=None, namespace=None):
        if args is None:
            args = sys.argv[1:]
        return [], args


class AliasCommand(Subcommand):
    def __init__(self, alias, command, log=None, help=None):
        super(AliasCommand, self).__init__(alias, help=help or command, parser=NoOpOptionParser(add_help_option=False, description=help or command))

        self.alias = alias
        self.log = log
        self.command = command

    def func(self, lib, opts, args=None):
        if args is None:
            args = []

        split_command = shlex.split(self.command)
        command = split_command[0]
        command_args = split_command[1:]

        # loop through beet arguments, starting from behind
        for i in range(len(args) - 1, -1, -1):
            # replace all occurences of token {X} with parameter (if it exists)
            token = "{i}".replace("i", str(i))
            token_replaced = False
            for j in range(0, len(command_args), 1):
                if token in command_args[j]:
                    command_args[j] = command_args[j].replace(token, args[i])
                    token_replaced = True
            # remove parameter if it has been used for a replacement
            if token_replaced:
                del args[i]

        # search for token {} and replace it with the rest of the arguments, if it exists or append otherwise
        if '{}' in command_args:
            for i in range(len(command_args) - 1, -1, -1):
                if command_args[i] == '{}':
                    command_args[i:i + 1] = args
        else:
            command_args = command_args + args

        args = command_args

        if command.startswith('!'):
            command = command[1:]
            argv = [command] + args

            if self.log:
                self.log.debug('Running {}', subprocess.list2cmdline(argv))

            try:
                return subprocess.check_call(argv)
            except subprocess.CalledProcessError as exc:
                if self.log:
                    self.log.debug(u'command `{0}` failed with {1}', subprocess.list2cmdline(argv), exc.returncode)
                plugins.send('cli_exit', lib=lib)
                lib._close()
                sys.exit(exc.returncode)
        else:
            argv = [command] + args
            cmdname = argv[0]

            subcommands = list(default_commands)
            subcommands.extend(plugins.commands())
            for subcommand in subcommands:
                if cmdname == subcommand.name or cmdname in subcommand.aliases:
                    break
            else:
                raise ui.UserError(u"unknown command '{0}'".format(cmdname))

            if self.log:
                self.log.debug('Running {}', subprocess.list2cmdline(argv))

            suboptions, subargs = subcommand.parse_args(argv[1:])
            return subcommand.func(lib, suboptions, subargs)


class AliasPlugin(BeetsPlugin):
    """Support for beets command aliases, not unlike git."""

    def __init__(self):
        super(AliasPlugin, self).__init__()

        self.config.add({
            'from_path': True,
            'aliases': {},
        })

    def get_command(self, alias, command, help=None):
        """Create a Subcommand instance for the specified alias."""
        return AliasCommand(alias, command, log=self._log, help=help)

    def get_path_commands(self):
        """Create subcommands for beet-* scripts in $PATH."""
        for path in os.getenv('PATH', '').split(':'):
            cmds = glob.glob(os.path.join(path, 'beet-*'))
            for cmd in cmds:
                if os.access(cmd, os.X_OK):
                    command = os.path.basename(cmd)
                    alias = command[5:]
                    yield (alias, self.get_command(alias, '!' + command, u'Run external command `{0}`'.format(command)))

    def cmd_alias(self, lib, opts, args, commands):
        """Print the available alias commands."""
        for alias, command in sorted(commands.items()):
            print_(u'{0}: {1}'.format(alias, command))

    def commands(self):
        """Add the alias commands."""
        if self.config['from_path'].get(bool):
            commands = dict(self.get_path_commands())
        else:
            commands = {}

        for path, subview in [('alias.aliases', self.config['aliases']), ('aliases', config['aliases'])]:
            for alias in subview.keys():
                if alias in commands:
                    raise confuse.ConfigError(u'alias {1} was specified multiple times'.format(alias))

                command = subview[alias].get()
                if isinstance(command, six.text_type):
                    commands[alias] = self.get_command(alias, command)
                elif isinstance(command, abc.Mapping):
                    command_text = command.get('command')
                    if not command_text:
                        raise confuse.ConfigError(u'{0}.{1}.command not found'.format(path, alias))
                    help_text = command.get('help', command_text)
                    commands[alias] = self.get_command(alias, command_text, help_text)
                else:
                    raise confuse.ConfigError(u'{0}.{1} must be a string or single-element mapping'.format(path, alias))

        if 'alias' in commands:
            raise ui.UserError(u'alias `alias` is reserved for the alias plugin')

        alias = Subcommand('alias',
                           help=u'Print the available alias commands.')
        alias_commands = dict((a, c.command) for a, c in commands.items())
        alias.func = lambda lib, opts, args: self.cmd_alias(lib, opts, args, alias_commands)
        commands['alias'] = alias
        return commands.values()
