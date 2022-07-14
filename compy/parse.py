import re
from tokenstream import Token, TokenStream
from .engine import Engine

__all__ = ["Parser", "find_command"]


class Parser:
    def __init__(self, engine: Engine = None):
        self.engine = engine

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def clean(self, string):
        return _parse(TokenStream(f"[{string}]"))

    def parse(self, string):
        return find_command(self.engine, self.clean(string))


def find_command(engine: Engine, args: list[str]) -> ...:
    if not len(args) > 0:
        return
    arg = args.pop(0)
    for key, command in engine.__commands__.items():
        if arg in command.aliases:
            return engine.__commands__[key].find_child(args)


ESCAPE_REGEX = re.compile(r"\\.")

ESCAPE_SEQUENCES = {
    r"\n": "\n",
    r"\"": '"',
    r"\\": "\\",
}


def unquote_string(token: Token) -> str:
    return ESCAPE_REGEX.sub(lambda match: ESCAPE_SEQUENCES[match[0]], token.value[1:-1])


def _parse(stream: TokenStream):
    with stream.syntax(
        brace=r"\[|\]", number=r"\d+", word=r"[^\"\[\]\s]+", string=r'"(?:\\.|[^"\\])*"'
    ):
        brace, number, word, string = stream.expect(
            ("brace", "["), "number", "word", "string"
        )
        if brace:
            return [_parse(stream) for _ in stream.peek_until(("brace", "]"))]
        elif string:
            return unquote_string(string)
        elif number:
            return int(number.value)
        elif word:
            return word.value
