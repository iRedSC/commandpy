from .command import Command, create_command

__all__ = ["injectcommand"]


def injectcommand(func) -> Command:
    return create_command(func, None, None, True)
