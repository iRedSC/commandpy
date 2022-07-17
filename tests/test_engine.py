import pytest
from commandpy import Engine


@pytest.fixture
def engine():
    return Engine()


def test_register_command(engine: Engine):
    @engine.command
    def greeting():
        return True

    assert engine.groups == {}
    assert engine.__commands__["greeting"]
