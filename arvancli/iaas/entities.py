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
        self._receiver = Receiver()
        self._invoker = Invoker()
    def _get_list(self, session: Session) -> None:
        cmd = RegionsListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        regions_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = regions_list[0].keys()
        for region in regions_list:
            pt.add_row(region.values())
        print(pt)
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls' : self._get_list}
    def run(self, command: str, session: Session, arguments: dict) -> None:
        self._arguments = arguments
        if command in self._command_table:
            self._command_table[command](session)
        else:
            raise ValueError(key)

class ServerEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
        self._receiver = Receiver()
        self._invoker = Invoker()
    def _get_id(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        server_id = self._invoker.get_result()
        print(f'Server ID is: {server_id}')
    def _get_status(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerStatusCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        server_status = self._invoker.get_result()
        print(f'Server Status is: {server_status}')
    def _get_list(self, session: Session) -> None:
        cmd = ServersListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        servers_list = self._invoker.get_result()
        pt = PrettyTable()
        pt._max_width = {"IP Address(es)" : 70}
        pt.field_names = servers_list[0].keys()
        for server in servers_list:
            pt.add_row(server.values())
        print(pt)
    def _reboot(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerRebootCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Reboot request sent!')
    def _poweroff(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerPoweroffCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Poweroff request sent!')
    def _prepare_command_table(self) -> None:
        self._command_table = {'id'       : self._get_id,
                               'status'   : self._get_status,
                               'ls'       : self._get_list,
                               'reboot'   : self._reboot,
                               'poweroff' : self._poweroff
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
        self._receiver = Receiver()
        self._invoker = Invoker()
    def _get_list(self, session: Session) -> None:
        cmd = FirewallsListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        firewalls_list = self._invoker.get_result()
        pt = PrettyTable()
        pt._max_width = {"Servers" : 90}
        pt.field_names = firewalls_list[0].keys()
        for firewall in firewalls_list:
            pt.add_row(firewall.values())
        print(pt)
    def _get_id(self, session: Session) -> None:
        self._receiver.set({'firewall_name': self._arguments['name']})
        cmd = FirewallIdCommand(self._receiver, session)
        self._invoker = Invoker()
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        firewall_id = self._invoker.get_result()
        print(f'Firewall Group ID is: {firewall_id}')
    def _create(self, session: Session) -> None:
        self._receiver.set({'firewall_name'        : self._arguments['name']})
        self._receiver.set({'firewall_description' : self._arguments['description']})
        cmd = FirewallCreateCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Firewall Group created successfully')
    def _delete(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        cmd = FirewallIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'firewall_id' : self._invoker.get_result()})
        cmd = FirewallDeleteCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        firewall_name = self._invoker.get_result()
        print(f'Firewall Group deleted successfully')
    def _list_rules(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        cmd = FirewallRulesCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        rules_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = rules_list[0].keys()
        for rule in rules_list:
            pt.add_row(rule.values())
        print(pt)
    def _add_rule(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        cmd = FirewallIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({f'firewall_id' : self._invoker.get_result()})
        for argument in self._arguments:
            if 'firewall' not in argument:
                self._receiver.set({f'rule_{argument}' : self._arguments[argument]})
        cmd = FirewallAddRuleCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Firewall Rule added successfully')
    def _delete_rule(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        self._receiver.set({'rule_number' : self._arguments['number']})
        cmd = FirewallRuleIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({f'rule_id' : self._invoker.get_result()})
        cmd = FirewallDeleteRuleCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Firewall Rule deleted successfully')
    def _attach_server(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        self._receiver.set({'server_name' : self._arguments['server']})
        cmd = FirewallIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({f'firewall_id' : self._invoker.get_result()})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = FirewallAttachServerCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Server attached successfully')
    def _detach_server(self, session: Session) -> None:
        self._receiver.set({'firewall_name' : self._arguments['name']})
        self._receiver.set({'server_name' : self._arguments['server']})
        cmd = FirewallIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({f'firewall_id' : self._invoker.get_result()})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = FirewallDetachServerCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls'            : self._get_list,
                               'id'            : self._get_id,
                               'create'        : self._create,
                               'delete'        : self._delete,
                               'list-rules'    : self._list_rules,
                               'add-rule'      : self._add_rule,
                               'delete-rule'   : self._delete_rule,
                               'attach-server' : self._attach_server,
                               'detach-server' : self._detach_server,
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
        super().__init__(subparsers, {'id'      :      [['"--name"', 'help="Name of the server"'],
                                                 ],
                                      'status'  :  [['"--name"', 'help="Name of the server"'],
                                                 ],
                                      'ls'      :  [[],
                                                 ],
                                      'reboot'  :  [['"--name"', 'help="Name of the server"'],
                                                 ],
                                      'poweroff':  [['"--name"', 'help="Name of the server"'],
                                                 ],
                                     }
                        )
    def __call__(self) -> None:
        self._entity = ServerEntitiy()
        return self._entity

class FirewallEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'ls'            : [[],
                                                        ],
                                      'id'            : [['"--name"'       , 'help="Name of the firewall group"'],
                                                        ],
                                      'create'        : [['"--name"'       , 'help="Name of the firewall group"'],
                                                         ['"--description"', 'help="Description of the firewall group"'],
                                                        ],
                                      'delete'        : [['"--name"'       , 'help="Name of the firewall group"'],
                                                        ],
                                      'list-rules'    : [['"--name"'       , 'help="Name of the firewall group"'],
                                                        ],
                                      'add-rule'      : [['"--name"'       , 'help="Name of the firewall group"'],
                                                         ['"--description"', 'help="Description of the rule"'],
                                                         ['"--direction"'  , 'help="Direction of the rule."'],
                                                         ['"--cidr"'       , 'help="CIDR or list of CIDRs that rule will be applied to. Multiple CIDRs must be seperated with ,"'],
                                                         ['"--protocol"'   , 'help="Protocol of the rule."'],
                                                         ['"--port"'       , 'help="Port or port range of the rule. A range must be specified such as SPORT:DPORT"'],
                                                        ],
                                      'delete-rule'   : [['"--name"'       , 'help="Name of the firewall group"'],
                                                         ['"--number"'     , 'help="The row number of the specified rule"'],
                                                        ],
                                      'attach-server' : [['"--name"'       , 'help="Name of the firewall group"'],
                                                         ['"--server"'     , 'help="Name of the desired server to be attached"'],
                                                        ],
                                      'detach-server' : [['"--name"'       , 'help="Name of the firewall group"'],
                                                         ['"--server"'     , 'help="Name of the desired server to be detached"'],
                                                        ],
                                     } 
                        )
    def __call__(self) -> None:
        self._entity = FirewallEntitiy()
        return self._entity
