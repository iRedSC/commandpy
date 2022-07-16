from .protocols import Command

__all__ = ["Group", "group"]


class Group:
    def __init__(self, name: str = None):
        self.name = name
        self.commands = []


def group(name: str):
    def decorator(cmd: Command):
        if not cmd.__last_engine__.groups.get(name):
            group = Group(name=name)
            cmd.__last_engine__.groups[name] = group
            cmd = cmd.__last_engine__.__commands__[cmd.name]
            if not cmd.groups.get(name):
                cmd.groups[name] = group
        else:
            group = cmd.__last_engine__.groups[name]
        group.commands.append(cmd)
        return cmd

    return decorator
