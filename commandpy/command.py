from typing import Callable, Optional

from .protocols import CommandRef, Engine
from .exceptions import EngineNotRegistered, InjectCommandError
from .injected_command import inject_command

__all__ = ["Command", "create_command"]


class Command:
    """A class that holds some information about a command."""

    def __init__(
        self,
        last_engine: Engine,
        func: Callable,
        name: str,
        parent: "Command",
        aliases: list[str] = None,
        children: Optional[list["Command"]] = None,
        injectcommand: bool = False,
    ) -> None:
        self.__last_engine__ = last_engine
        self.__execute = func

        self.func = func
        self.name = name
        self.__name__ = name
        self.children = children if children else []
        self.aliases = aliases if aliases else []
        self.aliases.append(name)
        self.parent = parent
        self.injectcommand = injectcommand
        self.refs: dict[Engine, CommandRef] = {}
        self.help = "No help desciption provided."

    def __call__(self, *args, **kwargs):
        def __passcmd(engine: Engine):
            try:
                cmdref = self.refs[engine]
            except KeyError:
                raise EngineNotRegistered(
                    "The engine that was passed was not registered to this command."
                )
            return self.__execute(inject_command(cmdref), *args, **kwargs)

        if self.injectcommand:
            return __passcmd
        return self.__execute(*args, **kwargs)

    def subcommand(
        self,
        func: Callable | "Command" = None,
        aliases: list[str] = None,
        name: str = None,
    ):
        """A decorator that creates a subcommand."""

        def decorator(func: Callable) -> Command:
            cmd = create_command(func, None, name, aliases)
            self.children.append(cmd)
            return cmd

        if callable(func):
            return decorator(func)
        else:
            return decorator


def create_command(
    func: Callable | Command,
    engine: Engine,
    aliases: list[str] = None,
    injectcommand: bool = False,
) -> Command:
    if isinstance(func, Command):
        if injectcommand == True:
            raise InjectCommandError("@injectcommand decorator must be applied first.")
        func.__last_engine__ = engine
        return func
    return Command(
        last_engine=engine,
        func=func,
        name=func.__name__,
        parent=None,
        aliases=aliases,
        injectcommand=injectcommand,
    )
