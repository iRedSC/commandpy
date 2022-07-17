import pytest
from commandpy import Engine, Parser
from commandpy.exceptions import TooManyArguments


@pytest.fixture
def engine():
    return Engine()


def test_simple(engine: Engine):
    @engine.command
    def boolean():
        return True

    assert boolean() == True
    with Parser(engine) as parse:
        assert parse("boolean")() == True
        with pytest.raises(TooManyArguments):
            parse("boolean 1 2 3")()


def test_multiple_engines(engine: Engine):
    engine2 = Engine()

    @engine.command
    @engine2.command
    def boolean():
        return True

    assert boolean() == True

    def parse(engine: Engine):
        with Parser(engine) as parse:
            assert parse("boolean")() == True
            with pytest.raises(TooManyArguments):
                parse("boolean 1 2 3")()

    parse(engine)
    parse(engine2)


def test_subcommand(engine: Engine):
    @engine.command
    def boolean():
        return True

    @engine.command
    @boolean.subcommand
    def f():
        return False

    @boolean.subcommand(name="false")
    def _f():
        return False

    assert f() == False

    with Parser(engine) as parse:
        assert parse("boolean f")() == False
        assert parse("boolean false")() == False
        assert parse("f")() == False
