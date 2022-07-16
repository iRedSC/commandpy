import pytest
from commandpy import Engine, Command, Parser


@pytest.fixture
def engine():
    return Engine()


def _parse_command(cmd: str, engine: Engine):
    return Parser(engine).parse(cmd)()


def test_create_simple_command(engine: Engine):
    @engine.command
    def greeting() -> str:
        return "hello"

    assert isinstance(greeting, Command)
    assert _parse_command("greeting", engine) == "hello"


def test_create_command_with_args(engine: Engine):
    @engine.command
    def greeting(person: str) -> str:
        return f"hello {person}"

    assert _parse_command("greeting john", engine) == "hello john"
    assert _parse_command('greeting "john doe"', engine) == "hello john doe"


def test_create_command_with_name(engine: Engine):
    @engine.command(name="hi")
    def greeting():
        return "hello"

    assert _parse_command("hi", engine) == "hello"


def test_create_command_with_aliases(engine: Engine):
    @engine.command(aliases=["hi", "greetings", "welcome"])
    def greeting():
        return "hello"

    assert _parse_command("greeting", engine) == "hello"
    assert _parse_command("greetings", engine) == "hello"
    assert _parse_command("hi", engine) == "hello"
    assert _parse_command("welcome", engine) == "hello"


def test_create_subcommand(engine: Engine):
    @engine.command
    def calc(num: int) -> int:
        return 10 + num

    @calc.subcommand
    def add(num1, num2):
        return num1 + num2

    assert _parse_command("calc 1", engine) == 11
    assert _parse_command("calc add 5 10", engine) == 15


def test_subcommand_subcommand(engine: Engine):
    @engine.command
    def calc():
        ...

    @calc.subcommand
    def add(num1, num2):
        return num1 + num2

    @add.subcommand
    def batch(*nums):
        result = 0
        for num in nums:
            result += num
        return result

    assert _parse_command("calc add 1 2", engine) == 3
    assert _parse_command("calc add batch 5 5 5", engine) == 15
