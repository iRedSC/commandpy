from typing import Any, Callable, Protocol


class Command(Protocol):
    func: Callable
    name: str
    __name__: str
    children: list["Command"]
    aliases: list[str]
    parent: "Command"
    help: str
    refs: dict["Engine", "CommandRef"]

    def retrieve(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def addref(self, engine: "Engine", ref: "CommandRef") -> None:
        ...


class DecoratorCommand(Protocol):
    last_engine: "Engine"
    command: Command
    func: Callable
    name: str
    __name__: str
    passcommand: bool

    def subcommand(
        self,
        func: Callable | "DecoratorCommand" | None = None,
        aliases: list[str] = None,
        name: str = None,
    ) -> Callable[[Callable], "DecoratorCommand"]:
        ...


class CommandRef(Protocol):
    command: Command
    name: str
    aliases: list[str]
    engine: "Engine"
    groups: dict[str, "Group"]
    __passcommand__: bool

    def retrieve(self):
        ...

    def find_child(self, args: list[str]) -> "CommandRef":
        ...

    def childref(self, child: Command) -> "CommandRef":
        ...


class InjectedCommand(Protocol):
    ...


class Engine(Protocol):
    __commands__: dict[str, CommandRef]
    groups: dict[str, "Group"]
    commands: dict[str, InjectedCommand]

    def command(
        self, func: Callable = None, name: str = None, aliases: list[str] = None
    ) -> DecoratorCommand:
        ...


class Group(Protocol):
    ...
