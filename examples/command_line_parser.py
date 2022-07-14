import sys
from compy import Engine, Parser


engine = Engine()


@engine.command
def quit():
    sys.exit()


@engine.command(name="file")
def _file(_file):
    try:
        with open(_file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("That file doesn't exist.")


@_file.subcommand
def create(_file, *contents):
    try:
        with open(_file, "x") as f:
            f.write(" ".join(contents))
    except FileExistsError:
        print("That file already exists.")


def main():
    while True:
        with Parser(engine) as parser:
            parser.parse(input(" ? ")).execute()


if __name__ == "__main__":
    main()
