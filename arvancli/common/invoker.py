from arvancli.common.command import Command

class Invoker:    
    def __init__(self) -> None:
        self._command = None
        self._result = None
    def store_command(self, command: Command) -> None:
        self._command = command
    def execute_command(self) -> None:
        self._result = self._command.execute()
    def get_result(self) -> str:
        return self._result
