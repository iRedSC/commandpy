from typing import Callable
from .command import Command, create_command
from .group import Group
from .injected_command import inject_command

__all__ = ["CommandRef", "Engine"]


class CommandRef:
    """
    Holds a reference of a command along with engine-specific
    data, such as aliases and groups.

    CommandRef's are not directly interactable by the end-user,
    and are transformed into the more user friendly InjectedCommand.
    """

    def __init__(
        self,
        command: "Command",
        engine: "Engine",
        name: str = None,
        aliases: list[str] = None,
        groups: dict[str, "Group"] = None,
    ):
        self.command = command
        self.name = name
        self.aliases = aliases if aliases else []
        self.aliases.append(name)
        self.engine = engine
        self.groups = groups if groups else {}

    def copy_ref(self, child: Command) -> "CommandRef":
        return CommandRef(
            command=child,
            engine=self.engine,
            name=child.name,
            aliases=child.aliases,
            groups=self.groups,
        )

    def find_child(self, args: list[str | list[str]]):
        if not len(args) > 0:
            return inject_command(self).retrieve()
        arg = args[0]

        for child in self.command.children:
            if arg in child.aliases:
                args.pop(0)
                return self.copy_ref(child).find_child(args)
        return inject_command(self).retrieve(*args)


class Engine:
    """
    The Engine holds a group of base commands,
    and can be passed to a parser to search commands
    registered under itself.

    Creating an Engine is as simple as creating a new object.
    >>> engine = Engine()

    Then use the command method decorator to register a function as
    a command.
    >>> @engine.command
    ... def greeting() -> str:
    ...    ...

    Commands can be registers to multiple Engines.
    >>> engine_2 = Engine()

    >>> @engine_2.command
    ... @engine.command
    ... def greeting() -> str:
    ...     ...

    """

    def __init__(self):
        self.__commands__: dict[str, CommandRef] = {}
        self.groups: dict[str, Group] = {}

    @property
    def commands(self):
        return {name: inject_command(cmd) for name, cmd in self.__commands__.items()}

    def command(
        self,
        func: Callable = None,
        name: str = None,
        aliases: list[str] = None,
    ) -> Command:
        def decorator(func) -> Command:
            command = create_command(func, self, aliases)
            cmdref = CommandRef(
                command=command,
                engine=self,
                name=name if name else command.name,
                aliases=aliases,
            )
            cmdref.command.refs[self] = cmdref

            self.__commands__[name if name else command.name] = cmdref
            return command

        if callable(func):
            return decorator(func)
        else:
            return decorator
