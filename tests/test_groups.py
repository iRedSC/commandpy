import pytest
from commandpy import Engine, Parser, injectcommand, group


@pytest.fixture
def engine():
    return Engine()


def test_single_group(engine: Engine):
    @group("math")
    @engine.command
    @injectcommand
    def calc(self):
        return self.groups

    assert engine.groups["math"]
    assert Parser(engine).parse("calc").groups["math"]
    assert Parser(engine).parse("calc")()["math"] == engine.groups["math"]
