from .command import Command

__all__ = ["Group", "group"]


class Group:
    def __init__(self, name: str = None):
        self.name = name
        self.commands = []


def group(name: Group):
    def decorator(dccmd: Command):
        if not dccmd.last_engine.groups.get(name):
            group = Group(name=name)
            dccmd.last_engine.groups[name] = group
            cmd = dccmd.last_engine.__commands__[dccmd.name]
            if not cmd.groups.get(name):
                cmd.groups[name] = group
        else:
            group = dccmd.last_engine.groups[name]
        group.commands.append(dccmd)
        return dccmd

    return decorator
