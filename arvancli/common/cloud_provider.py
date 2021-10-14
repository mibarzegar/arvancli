from arvancli.common.builder import Builder
from arvancli.common.provider import Provider
from arvancli.iaas.service import IaasServiceBuilder
from argparse import _SubParsersAction

class CloudProvider(Provider):
    def __init__(self) -> None:
        super().__init__()

class CloudProviderBuilder(Builder):
    def __init__(self, parser: _SubParsersAction) -> None:
        super().__init__(parser, {'iaas': IaasServiceBuilder})
    def __call__(self) -> CloudProvider:
        self._provider = CloudProvider()
        self._service_registrar()
        return self._provider
