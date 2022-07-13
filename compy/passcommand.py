from .decorator import create_decorator_command


def passcommand(func):
    return create_decorator_command(func, None, func.__name__, None, True)
