class Receiver:
    def __init__(self, arguments: dict):
        self._arguments = arguments

    def get(self, key) -> None:
        if key in self._arguments:
            return self._arguments[key]
        else:
            raise ValueError(key)
