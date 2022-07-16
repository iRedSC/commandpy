import pytest
from commandpy import (
    Engine,
    DecoratorCommand,
    PassCommandError,
    Parser,
    passcommand,
    InjectedCommand,
)


@pytest.fixture
def engine():
    return Engine()


def parse_command(string, engine):
    return Parser(engine).parse(string)


def test_decorator(engine: Engine):
    @passcommand
    def greeting(cmd):
        return "hello"

    assert isinstance(greeting, DecoratorCommand)
    assert greeting.passcommand == True


def test_passcommand_command(engine: Engine):
    @engine.command
    @passcommand
    def about(self):
        return self.name

    assert parse_command("about", engine).__passcommand__ == True
    assert isinstance(parse_command("about", engine), InjectedCommand)
    assert parse_command("about", engine).execute() == "about"


def test_passcommand_exception(engine: Engine):

    with pytest.raises(PassCommandError):

        @passcommand
        @engine.command
        def greeting():
            return "hello"
