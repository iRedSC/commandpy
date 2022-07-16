# Commandpy - Create Commands with Ease.

Commandpy lets you easily create commands that can be parsed from a string.

```py
from commandpy import Engine, Parser

engine = Engine()

@engine.command
def greeting(person: str):
    return f"Hello there, {person}!"

command_input = "greeting John"

with Parser(engine) as parse:
    command = parse(command_input)
    result = command.execute()
    print(result)
```

```Output: "Hello there, John"```

---
## **Getting Started**

Commands are just functions, so to make a command just make a function:
```py
def greeting(person: str) -> str:
    return f"Hello there, {person}!"
```
So that does- that, but it's not a command yet. To make it a command, we need to add it to an **Engine**.

To make an Engine, we just import `Engine` and make a new instance.
```py
from commandpy import Engine

engine = Engine()
```

Now that we have an Engine, we can use its `command` method to register the function as a command and add it to our Engine.

```py
from commandpy import Engine

engine = Engine()

@engine.command
def greeting(person: str) -> str:
    return f"Hello there, {person}!"
```

Congrats! You made your first command. Now if you want to parse and run this command, you need to import the `Parser`.

```py
from commandpy import Parser
```
The Parser can be used as a context manager and accepts an Engine as it's only parameter.
```py
with Parser(engine) as parse:
    parse("greeting John")
```
Calling the Parser directly will call its `parse()` method, which takes a string and will return an `InjectedCommand` that has data about the returned command, as well as an `execute()` method to execute the function.
```py
with Parser(engine) as parse:
    command = parse("greeting John")
    result = command.execute()
    print(result)
```

---
## Engines

You can register a command to multiple engines by stacking the decorators:
```py
from commandpy import Engine

engine1 = Engine()
engine2 =  Engine()

@engine1.command
@engine2.command
def greeting(...):
    ...
```
The name of the command is the name of the function by default, but it can be changed per Engine with the `name=` parameter:
```py

@engine1.command(name="hello")
@engine2.command(name="welcome")
def greeting(...):
    ...
```

Commands can also have a list of aliases using the `aliases=` parameter (This will not override the command's name):
```
@engine1.command(aliases=["hi", "sup", "hey"])
```

---
## Subcommands

Commands can have subcommands connected to them, using the `subcommand` method decorator:
```py
from commandpy import Engine

engine = Engine()

@engine.command
def greeting(person: str) -> str:
    return f"Hello there, {person}!"

@greeting.subcommand
def many(*people: str) -> str:
    return "\n".join([f"Hello there, {person}!" for person in people])
```
The above would be trigger with `greeting many John Jane Joe`
```
Output:
Hello there, John!
Hello there, Jane!
Hello there, Joe!
```
When a string is sent to a `Parser`, the parser will look for subcommands until none are found, then all remaining arguments are passed to the function.

Subcommands also have `name=` and `aliases=` parameters just like engines:
```py

@greeting.subcommand(name="many", aliases=["alot", "bunch", "batch"])
def __many(...):
    ...
```

---
## Parser

Commandpy uses a very simple parser that outputs based on a few simple rules:

 - Arguments are split by spaces.
 - "Quotes" will keep everything inside of them intact.
 - [lists, will, be transformed, into a list.]

Example:
```
this is an example of what "inputting something like this" [would, get you,", alright?"]
```
```
Output:
["this", "is", "an", "example", "of", "what", "inputting something like this", ["would", "get you", ", alright?"]]
```

When finding a command, the parser will just look for any command/subcommand name or alias that matches the argument, and if one is found it'll do the same with the next argument etc.

---
## Groups

You can add commands to groups by using the `group` decorator:
```py

from commandpy import Engine, group

engine = Engine()

@group("math")
@group("stuff")
@engine.command
def calc(...):
    ...
```
Groups will be added to the engine that is below them, and a dictionary of `{"group_name": Group}` can be accessed via `Engine.groups`.

---
## Injectcommand

You can get the command as a parameter in your function by using the `injectcommand` decorator:
```py
from commandpy import injectcommand

@engine.command
@injectcommand
def list_commands(self):
    return [command for command in self.engine.commands]
```
An `InjectedCommand` will be injected into the first parameter of the function.

**The injectcommand decorator must be applied directly above the function** else an exception will be raised.

---
## InjectedCommand

This is mainly how you interact with commands, it's a user-friendly class that lets you access all of a commands data, including the Engine it was accessed from as well as Groups it's a part of etc.

Attributes you have access to include:

`InjectedCommand.`
 - `name: str` — The name of the command.
 - `aliases: list[str]` — List of aliases.
 - `engine: Engine` — The engine the command was called from.
 - `groups: dict[str, Group]` — A dictionary of the groups the command if registered to.
 - `help: str` — Access to the command's help text.
 - `parent: InjectedCommand` — An InjectedCommand version of the parent command.
 - `children: list[InjectedCommand]` — A list of Injected children of the command.