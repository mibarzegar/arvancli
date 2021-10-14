from arvancli.common.builder import Builder
class ObjectFactory:
    def __init__(self) -> None:
        self._builders = {}

    def register_builder(self, key: str, builder: Builder) -> None:
        self._builders[key] = builder

    def create(self, key: str) -> None:
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder()
