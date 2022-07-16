import pytest
from commandpy import (
    Engine,
    Command,
    InjectCommandError,
    Parser,
    injectcommand,
    InjectedCommand,
)


@pytest.fixture
def engine():
    return Engine()


def parse_command(string, engine):
    return Parser(engine).parse(string)


def test_decorator(engine: Engine):
    @injectcommand
    def greeting(cmd):
        return "hello"

    assert isinstance(greeting, Command)
    assert greeting.injectcommand == True


def test_passcommand_command(engine: Engine):
    @engine.command
    @injectcommand
    def about(self):
        return self.name

    assert parse_command("about", engine).__injectcommand__ == True
    assert isinstance(parse_command("about", engine), InjectedCommand)
    assert parse_command("about", engine)() == "about"


def test_passcommand_exception(engine: Engine):

    with pytest.raises(InjectCommandError):

        @injectcommand
        @engine.command
        def greeting():
            return "hello"
