import re

from contextlib import contextmanager

from typing import Callable
from typing import List
from typing import Optional

from clikit.api.formatter import Style
from clikit.api.formatter import StyleSet
from clikit.api.command.exceptions import NoSuchCommandException

from .command_config import CommandConfig
from .config import Config


class ApplicationConfig(Config):
    """
    The configuration of a console application.
    """

    def __init__(
        self, name=None, version=None
    ):  # type: (Optional[str], Optional[str]) -> None
        self._name = name
        self._version = version
        self._display_name = None
        self._help = None
        self._command_configs = []  # type: List[CommandConfig]
        self._catch_exceptions = True
        self._terminate_after_run = True
        self._command_resolver = None
        self._io_factory = None
        self._debug = False
        self._style_set = None
        self._pre_resolve_hooks = []  # type: List[Callable]

        super(ApplicationConfig, self).__init__()

    @property
    def name(self):  # type: () -> Optional[str]
        return self._name

    def set_name(self, name):  # type: (Optional[str]) -> ApplicationConfig
        self._name = name

        return self

    @property
    def display_name(self):  # type: () -> str
        """
        Returns the application name as it is displayed in the help.
        """
        if self._display_name is not None:
            return self._display_name

        return self.default_display_name

    def set_display_name(
        self, display_name
    ):  # type: (Optional[str]) -> ApplicationConfig
        self._display_name = display_name

        return self

    @property
    def version(self):  # type: () -> Optional[str]
        return self._version

    def set_version(self, version):  # type: (Optional[str]) -> ApplicationConfig
        self._version = version

        return self

    @property
    def help(self):  # type: () -> Optional[str]
        return self._help

    def set_help(self, help):  # type: (Optional[str]) -> ApplicationConfig
        self._help = help

        return self

    def is_exception_caught(self):  # type: () -> bool
        return self._catch_exceptions

    def set_catch_exceptions(
        self, catch_exceptions
    ):  # type: (bool) -> ApplicationConfig
        self._catch_exceptions = catch_exceptions

        return self

    def is_terminated_after_run(self):  # type: () -> bool
        return self._terminate_after_run

    def set_terminate_after_run(
        self, terminate_after_run
    ):  # type: (bool) -> ApplicationConfig
        self._terminate_after_run = terminate_after_run

        return self

    @property
    def command_resolver(self):  # type: () -> CommandResolver
        if self._command_resolver is None:
            self._command_resolver = self.default_command_resolver

        return self._command_resolver

    def set_command_resolver(
        self, command_resolver
    ):  # type: (CommandResolver) -> ApplicationConfig
        self._command_resolver = command_resolver

        return self

    @property
    def io_factory(self):  # type: () -> Optional[Callable]
        return self._io_factory

    def set_io_factory(
        self, io_factory
    ):  # type: (Optional[Callable]) -> ApplicationConfig
        self._io_factory = io_factory

        return self

    def is_debug(self):  # type: () -> bool
        return self._debug

    def debug(self, debug=True):  # type: (bool) -> ApplicationConfig
        self._debug = debug

        return self

    @property
    def style_set(self):  # type: () -> StyleSet
        if self._style_set is None:
            self._style_set = self.default_style_set

        return self._style_set

    def set_style_set(self, style_set):  # type: (StyleSet) -> ApplicationConfig
        self._style_set = style_set

        return self

    def add_style(self, style):  # type: (Style) -> ApplicationConfig
        self.style_set.add(style)

        return self

    def add_styles(self, styles):  # type: (List[Style]) -> ApplicationConfig
        for style in styles:
            self.add_style(style)

        return self

    def remove_style(self, tag):  # type: (str) -> ApplicationConfig
        self.style_set.remove(tag)

    @contextmanager
    def command(self, name):  # type: (str) -> CommandConfig
        command_config = CommandConfig(name)
        self.add_command_config(command_config)

        yield command_config

    def create_command(self, name):  # type: (str) -> CommandConfig
        command_config = CommandConfig(name)
        self.add_command_config(command_config)

        return command_config

    @contextmanager
    def edit_command(self, name):  # type: (str) -> CommandConfig
        command_config = self.get_command_config(name)

        yield command_config

    def add_command_config(
        self, command_config
    ):  # type: (CommandConfig) -> ApplicationConfig
        self._command_configs.append(command_config)

        return self

    def add_command_configs(
        self, command_configs
    ):  # type: (List[CommandConfig]) -> ApplicationConfig
        for command_config in command_configs:
            self.add_command_config(command_config)

        return self

    def get_command_config(self, name):  # type: (str) -> CommandConfig
        for command_config in self._command_configs:
            if command_config.name == name:
                return command_config

        raise NoSuchCommandException(name)

    @property
    def command_configs(self):  # type: () -> List[CommandConfig]
        return self._command_configs

    def has_command_config(self, name):  # type: (str) -> bool
        for command_config in self._command_configs:
            if command_config.name == name:
                return True

        raise False

    def has_command_configs(self):  # type: () -> bool
        return len(self._command_configs) > 0

    @property
    def default_display_name(self):  # type: () -> Optional[str]
        if self._name is None:
            return

        return re.sub(r"[\s\-_]+", " ", self._name).title()

    @property
    def pre_resolve_hooks(self):  # type: () -> List[Callable]
        return self._pre_resolve_hooks

    def has_pre_resolve_hooks(self):  # type: () -> bool
        return len(self._pre_resolve_hooks) > 0

    def add_pre_resolve_hook(self, hook):  # type: (Callable) -> ApplicationConfig
        self._pre_resolve_hooks.append(hook)

    @property
    def default_style_set(self):  # type: () -> StyleSet
        raise NotImplementedError()

    @property
    def default_command_resolver(self):
        raise NotImplementedError()
