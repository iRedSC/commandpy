from typing import Callable, Protocol
from .command import Command


__all__ = ["DecoratorCommand", "create_decorator_command"]


class Engine(Protocol):
    ...


class DecoratorCommand:
    def __init__(
        self,
        last_engine: Engine,
        command: Command,
        func: Callable,
        passcommand: bool = False,
    ):
        self.last_engine = last_engine
        self.command = command
        self.func = func
        self.__name__ = command.name
        self.name = command.name
        self.passcommand = passcommand

    def __call__(self, *args, **kwargs):
        return self.command(*args, **kwargs)

    def subcommand(
        self,
        func: Callable | "DecoratorCommand" | None = None,
        aliases: list[str] = None,
        name: str = None,
    ):
        """A decorator that creates a subcommand."""

        def decorator(func: Callable) -> Command:
            cmd = create_decorator_command(func, None, name, aliases)
            self.command.children.append(cmd.command)
            return cmd

        if callable(func):
            return decorator(func)
        else:
            return decorator


class PassCommandError(Exception):
    pass


def create_decorator_command(
    func: Callable | DecoratorCommand,
    engine: Engine,
    name: str = None,
    aliases: list[str] = None,
    passcommand: bool = False,
):
    if isinstance(func, DecoratorCommand):
        if passcommand == True:
            raise PassCommandError("@passcommand decorator must be applied first.")
        func.last_engine = engine
        return func
    _name = func.__name__ if not name else name
    command = Command(
        func=func,
        name=_name,
        parent=None,
        aliases=aliases,
        passcommand=passcommand,
    )
    return DecoratorCommand(engine, command, func, passcommand=passcommand)
