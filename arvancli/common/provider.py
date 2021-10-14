from arvancli.common.object_factory import ObjectFactory
from arvancli.common.builder import Builder

class Provider(ObjectFactory):
    def __init__(self) -> None:
        super().__init__()
    def get(self, builder: Builder) -> None:
        if builder in self._builders:
            return self.create(builder)
        else:
            raise Exception(f'The System does not support specified service! ({builder})')
