from arvancli.common.builder import EntityBuilder
from arvancli.common.receiver import Receiver
from arvancli.common.invoker import Invoker
from arvancli.iaas.region import *
from arvancli.iaas.server import *
from prettytable import PrettyTable
from arvancli.common.utils import Session
from argparse import _SubParsersAction

class RegionEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
    def _get_list(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = RegionsListCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        regions_list = invoker.get_result()
        pt = PrettyTable()
        pt.field_names = regions_list[0].keys()
        for region in regions_list:
            pt.add_row(region.values())
        print(pt)
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls' : self._get_list}
    def run(self, command: str, session: Session, arguments: dict) -> None:
        if command in self._command_table:
            self._command_table[command](session)
        else:
            raise ValueError(key)

class ServerEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
    def _get_id(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = ServerIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        server_id = invoker.get_result()
        print(f'Server ID is: {server_id}')
    def _prepare_command_table(self) -> None:
        self._command_table = {'id' : self._get_id}
    def run(self, command: str, session: Session, arguments: dict) -> None:
        self._arguments = arguments
        if command in self._command_table:
            self._command_table[command](session)
        else:
            raise ValueError(key)

class RegionEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'ls': [[]]})
    def __call__(self) -> None:
        self._entity = RegionEntitiy()
        return self._entity

class ServerEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'id': [['"--name"', 'help="Name of the server"']] })
    def __call__(self) -> None:
        self._entity = ServerEntitiy()
        return self._entity
