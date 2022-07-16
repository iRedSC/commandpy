from .protocols import DecoratorCommand

__all__ = ["Group", "group"]


class Group:
    def __init__(self, name: str = None):
        self.name = name
        self.commands = []


def group(name: str):
    def decorator(cmd: DecoratorCommand):
        if not cmd.last_engine.groups.get(name):
            group = Group(name=name)
            cmd.last_engine.groups[name] = group
            cmd = cmd.last_engine.__commands__[cmd.name]
            if not cmd.groups.get(name):
                cmd.groups[name] = group
        else:
            group = cmd.last_engine.groups[name]
        group.commands.append(cmd)
        return cmd

    return decorator
