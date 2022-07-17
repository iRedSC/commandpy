from .group import Group
from typing import Callable
from .protocols import CommandRef, Engine

__all__ = ["InjectedCommand", "inject_command"]


class InjectedCommand:
    """
    This will be injected into a command function when the @passcommand
    decorator is used, it is also returned when a command is parsed.
    """

    def __init__(
        self,
        __cmdref__: CommandRef,
        __injectcommand__: bool,
        name: str,
        aliases: list[str],
        engine: Engine,
        groups: dict[str, Group],
        help: str,
    ):
        # the CommandRef that was turned into an InjectedCommand
        self.__cmdref__ = __cmdref__
        self.__injectcommand__ = __injectcommand__
        self.name = name
        self.aliases = aliases
        self.engine = engine
        self.groups = groups
        self.help = help

    @property
    def parent(self):
        """Returns an InjectedCommand version of the parent"""
        return inject_command(self.__cmdref__.childref(self.__cmdref__.command.parent))

    @property
    def children(self):
        """Returns an InjectedCommand version of the children"""
        return [
            inject_command(
                self.__cmdref__.childref(child)
                for child in self.__cmdref__.command.children
            )
        ]

    def __call__(self):
        return self.__execute()

    def retrieve(self, *args, **kwargs):
        """Sets self.execute to a ready-to-execute function."""

        def waiting_to_execute():
            if self.__injectcommand__ == True:
                return self.__cmdref__.command(*args, **kwargs)(self.engine)
            return self.__cmdref__.command(*args, **kwargs)

        self.__execute = waiting_to_execute
        return self

    def execute(self):
        return self()


def inject_command(cmdref: CommandRef):
    cmd = InjectedCommand(
        __cmdref__=cmdref,
        __injectcommand__=cmdref.command.injectcommand,
        name=cmdref.name,
        aliases=cmdref.aliases,
        engine=cmdref.engine,
        groups=cmdref.groups,
        help=cmdref.command.help,
    )
    return cmd
