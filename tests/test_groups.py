import pytest
from commandpy import Engine, Parser, passcommand, group


@pytest.fixture
def engine():
    return Engine()


def test_single_group(engine: Engine):
    @group("math")
    @engine.command
    @passcommand
    def calc(self):
        return self.groups

    assert engine.groups["math"]
    assert Parser(engine).parse("calc").groups["math"]
    assert Parser(engine).parse("calc").execute()["math"] == engine.groups["math"]
