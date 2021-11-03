from arvancli.common.builder import EntityBuilder
from arvancli.common.receiver import Receiver
from arvancli.common.invoker import Invoker
from arvancli.iaas.region import *
from arvancli.iaas.server import *
from arvancli.iaas.firewall import *
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
    def _get_status(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = ServerIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        arguments = {}
        arguments['id'] = invoker.get_result()
        receiver = Receiver(arguments)
        cmd = ServerStatusCommand(receiver, session)
        invoker.store_command(cmd)
        invoker.execute_command()
        server_status = invoker.get_result()
        print(f'Server Status is: {server_status}')
    def _prepare_command_table(self) -> None:
        self._command_table = {'id'     : self._get_id,
                               'status' : self._get_status,
                              }
    def run(self, command: str, session: Session, arguments: dict) -> None:
        self._arguments = arguments
        if command in self._command_table:
            self._command_table[command](session)
        else:
            raise ValueError(key)

class FirewallEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
    def _get_list(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallsListCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        firewalls_list = invoker.get_result()
        pt = PrettyTable()
        pt._max_width = {"Servers" : 90}
        pt.field_names = firewalls_list[0].keys()
        for firewall in firewalls_list:
            pt.add_row(firewall.values())
        print(pt)
    def _get_id(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        firewall_id = invoker.get_result()
        print(f'Firewall Group ID is: {firewall_id}')
    def _create(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallCreateCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        firewall_name = invoker.get_result()
        print(f'Firewall Group "{firewall_name}" created successfully')
    def _delete(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        arguments = {}
        arguments['id'] = invoker.get_result()
        receiver = Receiver(arguments)
        cmd = FirewallDeleteCommand(receiver, session)
        invoker.store_command(cmd)
        invoker.execute_command()
        firewall_name = invoker.get_result()
        print(f'Firewall Group deleted successfully')
    def _list_rules(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallRulesCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        rules_list = invoker.get_result()
        pt = PrettyTable()
        pt.field_names = rules_list[0].keys()
        for rule in rules_list:
            pt.add_row(rule.values())
        print(pt)
    def _add_rule(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        self._arguments['id'] = invoker.get_result()
        receiver = Receiver(self._arguments)
        cmd = FirewallAddRuleCommand(receiver, session)
        invoker.store_command(cmd)
        invoker.execute_command()
        print(f'Firewall Rule added successfully')
    def _delete_rule(self, session: Session) -> None:
        receiver = Receiver(self._arguments)
        cmd = FirewallRuleIdCommand(receiver, session)
        invoker = Invoker()
        invoker.store_command(cmd)
        invoker.execute_command()
        arguments = {}
        arguments['id'] = invoker.get_result()
        receiver = Receiver(arguments)
        cmd = FirewallDeleteRuleCommand(receiver, session)
        invoker.store_command(cmd)
        invoker.execute_command()
        print(f'Firewall Rule deleted successfully')
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls'          : self._get_list,
                               'id'          : self._get_id,
                               'create'      : self._create,
                               'delete'      : self._delete,
                               'list-rules'  : self._list_rules,
                               'add-rule'    : self._add_rule,
                               'delete-rule' : self._delete_rule,
                              }
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
        super().__init__(subparsers, {'id':      [['"--name"', 'help="Name of the server"'],
                                                 ],
                                      'status':  [['"--name"', 'help="Name of the server"'],
                                                 ],
                                     }
                        )
    def __call__(self) -> None:
        self._entity = ServerEntitiy()
        return self._entity

class FirewallEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'ls'          : [[],
                                                      ],
                                      'id'          : [['"--name"'       , 'help="Name of the firewall group"'],
                                                      ],
                                      'create'      : [['"--name"'       , 'help="Name of the firewall group"'],
                                                       ['"--description"', 'help="Description of the firewall group"'],
                                                      ],
                                      'delete'      : [['"--name"'       , 'help="Name of the firewall group"'],
                                                      ],
                                      'list-rules'  : [['"--name"'       , 'help="Name of the firewall group"'],
                                                      ],
                                      'add-rule'    : [['"--name"'       , 'help="Name of the firewall group"'],
                                                       ['"--description"', 'help="Description of the rule"'],
                                                       ['"--direction"'  , 'help="Direction of the rule."'],
                                                       ['"--cidr"'       , 'help="CIDR or list of CIDRs that rule will be applied to. Multiple CIDRs must be seperated with ,"'],
                                                       ['"--protocol"'   , 'help="Protocol of the rule."'],
                                                       ['"--port"'       , 'help="Port or port range of the rule. A range must be specified such as SPORT:DPORT"'],
                                                      ],
                                      'delete-rule' : [['"--name"'       , 'help="Name of the firewall group"'],
                                                       ['"--number"'     , 'help="The row number of the specified rule"'],
                                                      ]
                                     } 
                        )
    def __call__(self) -> None:
        self._entity = FirewallEntitiy()
        return self._entity
