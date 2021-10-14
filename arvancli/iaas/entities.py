from arvancli.common.builder import Builder
from arvancli.common.receiver import Receiver
from arvancli.common.invoker import Invoker
from arvancli.iaas.region import *
from prettytable import PrettyTable
from arvancli.common.utils import Session
from argparse import _SubParsersAction

class RegionEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
    def _get_list(self, session: Session, **kwargs) -> None:
        receiver = Receiver()
        cmd = RegionsListCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_commands()
        regions_list = invoker.results[0]
        pt = PrettyTable()
        pt.field_names = regions_list[0].keys()
        for region in regions_list:
            pt.add_row(region.values())
        print(pt)
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls' : self._get_list}
    def run(self, command: str, session: Session, **kwargs) -> None:
        if command in self._command_table:
            self._command_table[command](session, **kwargs)
        else:
            raise ValueError(key)

class RegionEntityBuilder(Builder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'ls':''})
    def __call__(self) -> None:
        self._entity = RegionEntitiy()
        return self._entity
