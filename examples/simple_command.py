from commandpy import Engine
from commandpy.injected_command import InjectedCommand
from commandpy.parse import Parser
from commandpy.passcommand import passcommand

engine = Engine()
engine2 = Engine()


@engine.command
def add(*nums) -> int | float:
    return sum(nums)


@engine.command
@passcommand
def listcommands(self: InjectedCommand):
    for command in self.engine.commands:
        yield command


add(1, 2, 3, 4, 5)
for command in listcommands()(engine):
    print(command)

with Parser(engine) as parse:
    result = parse("add 1 2 3 4 5")

    print(result.execute())
