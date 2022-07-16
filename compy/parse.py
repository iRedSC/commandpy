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
        return parse(TokenStream(string))

    def parse(self, string):
        return find_command(self.engine, self.clean(string))

    def __call__(self, string):
        return self.parse(string)


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


def parse_list(stream: TokenStream):
    with stream.syntax(
        comma=r",\s*", number=r"\d+", entry=r"[^\"\[\],]+"
    ), stream.ignore("comma"):
        match stream.expect_any("entry", "string", "number", ("brace", "[")):
            case Token(type="brace"):
                return [(parse_list(stream)) for _ in stream.peek_until(("brace", "]"))]
            case Token(type="number") as number:
                return int(number.value)
            case Token(type="entry") as entry:
                return entry.value
            case Token(type="string") as string:
                return unquote_string(string)


def parse_token(token: Token, stream: TokenStream):
    print(stream.current.value)
    match token:
        case Token(type="brace"):
            return [(parse_list(stream)) for _ in stream.peek_until(("brace", "]"))]
        case Token(type="string") as string:
            return unquote_string(string)
        case Token(type="number") as number:
            return int(number.value)
        case Token(type="word") as word:
            return word.value


def parse(stream: TokenStream):
    with stream.syntax(
        brace=r"\[|\]",
        number=r"\d+",
        word=r"[^\"\[\]\s]+",
        string=r'"(?:\\.|[^"\\])*"',
    ):
        return [
            parse_token(token, stream)
            for token in stream.collect_any(("brace", "["), "number", "word", "string")
        ]
