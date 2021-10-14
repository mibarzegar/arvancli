from arvancli.common.command import Command

class Invoker:    
    def __init__(self) -> None:
        self._commands = []
        self.results = []

    def store_command(self, command: Command) -> None:
        self._commands.append(command)

    def execute_commands(self) -> None:
        for command in self._commands:
            self.results.append(command.execute())
