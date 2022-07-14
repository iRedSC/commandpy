from typing import Callable
from .command import Command
from .group import Group
from .decorator import create_decorator_command
from .injected_command import inject_command

__all__ = ["CommandRef", "Engine"]


class CommandRef:
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

    def __call__(self, *args, **kwargs):
        return self.command(*args, **kwargs)

    def retrieve(self):
        return self.command.retrieve

    def find_child(self, args: list[str | list[str]]):
        if not len(args) > 0:
            return inject_command(self).retrieve()
        arg = args[0]

        for child in self.command.children:
            if arg in child.aliases:
                args.pop(0)
                return self.childref(child).find_child(args)
        return inject_command(self).retrieve(*args)

    def childref(self, child: Command) -> "CommandRef":
        return CommandRef(
            command=child,
            engine=self.engine,
            name=child.name,
            aliases=child.aliases,
            groups=self.groups,
        )


class Engine:
    """
    The Engine holds a group of base commands,
    and can be passed to a parser to search commands
    registered under itself.

    Creating an Engine is as simple as creating a new object.
    >>> engine = Engine()

    Then use the command decorator to register a function as
    a command.
    >>> @engine.command
    ... def greeting() -> str:
    ...    ...

    Commands can be registers to multiple Engines.
    >>> engine_2 = Engine()

    >>> @engine_2.command
    ... @engine.command
    ... def greeting() -> str:
    ...     ...s

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
    ) -> Callable:
        def decorator(func):
            cmd = create_decorator_command(func, self, name, aliases)
            cmdref = CommandRef(
                command=cmd.command,
                engine=self,
                name=name if name else cmd.name,
                aliases=aliases,
            )

            self.__commands__[name if name else cmd.name] = cmdref
            return cmd

        if callable(func):
            return decorator(func)
        else:
            return decorator
