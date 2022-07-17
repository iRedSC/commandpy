from commandpy import Engine, Parser


engine = Engine()


@engine.command
def boolean():
    return True


string = "boolean 1 2 3"

with Parser(engine) as parse:
    parse(string)()
