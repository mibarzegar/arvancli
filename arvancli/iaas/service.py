from arvancli.common.builder import Builder
from arvancli.common.provider import Provider
from arvancli.iaas.entities import RegionEntityBuilder
from argparse import _SubParsersAction

class IaasService(Provider):
    def __init__(self) -> None:
        super(Provider, self).__init__()

class IaasServiceBuilder(Builder):
    def __init__(self, parser: _SubParsersAction) -> None:
        super().__init__(parser, {'region': RegionEntityBuilder})
    def __call__(self) -> IaasService:
        self._provider = IaasService()
        self._service_registrar()
        return self._provider
