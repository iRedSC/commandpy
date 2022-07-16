from typing import Any, Callable, Optional

from commandpy.protocols import CommandRef, Engine

__all__ = ["Command"]


class Command:
    """A class that holds some information about a command."""

    def __init__(
        self,
        func: Callable,
        name: str,
        parent: "Command",
        aliases: list[str] = None,
        children: Optional[list["Command"]] = None,
        passcommand: bool = False,
    ) -> None:
        self.func = func
        self.name = name
        self.__name__ = name
        self.children = children if children else []
        self.aliases = aliases if aliases else []
        self.aliases.append(name)
        self.parent = parent
        self.passcommand = passcommand
        self.refs: dict[Engine, CommandRef] = {}
        self.help = "No help desciption provided."

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Return called function when the object is called"""
        return self.func(*args, **kwargs)

    def addref(self, engine: Engine, ref: CommandRef):
        self.refs[engine] = ref

    def retrieve(self, *args: Any, **kwargs: Any) -> Any:
        """Sets self.execute to a ready to execute function."""

        def waiting_to_execute():
            return self.func(*args, **kwargs)

        self.execute = waiting_to_execute
        return self
