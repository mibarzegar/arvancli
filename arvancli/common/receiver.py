class Receiver:
    def __init__(self):
        self._arguments = {}
    def set(self, arguments: dict):
        self._arguments.update(arguments)
    def get(self, key) -> None:
        if key in self._arguments:
            return self._arguments[key]
        else:
            return None
