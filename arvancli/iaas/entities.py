from arvancli.common.builder import EntityBuilder
from arvancli.common.receiver import Receiver
from arvancli.common.invoker import Invoker
from arvancli.iaas.region import *
from arvancli.iaas.server import *
from arvancli.iaas.firewall import *
from arvancli.iaas.network import *
from arvancli.iaas.image import *
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
    def _poweron(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerPoweronCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Poweron request sent!')
    def _delete(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerDeleteCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'server deleted successfully!')
    def _resize(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        self._receiver.set({'resource'   : self._arguments['resource']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerResizeCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Resize request sent!')
    def _rename(self, session: Session) -> None:
        self._receiver.set({'server_name': self._arguments['name']})
        self._receiver.set({'new_server_name': self._arguments['new_name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id': self._invoker.get_result()})
        cmd = ServerRenameCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Rename request sent!')
    def _prepare_command_table(self) -> None:
        self._command_table = {'id'       : self._get_id,
                               'status'   : self._get_status,
                               'ls'       : self._get_list,
                               'reboot'   : self._reboot,
                               'poweroff' : self._poweroff,
                               'poweron'  : self._poweron,
                               'delete'   : self._delete,
                               'resize'   : self._resize,
                               'rename'   : self._rename
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
        print(f'Server detached successfully')
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

class NetworkEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
        self._receiver = Receiver()
        self._invoker = Invoker()
    def _get_list(self, session: Session) -> None:
        cmd = NetworkListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        networks_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = networks_list[0].keys()
        for network in networks_list:
            pt.add_row(network.values())
        print(pt)
    def _get_servers(self, session: Session) -> None:
        self._receiver.set({'network_name': self._arguments['name']})
        cmd = NetworkServersListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        servers_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = servers_list[0].keys()
        for server in servers_list:
            pt.add_row(server.values())
        print(pt)
    def _add_ptr(self, session: Session) -> None:
        self._receiver.set({'ptr_ip'  : self._arguments['ip'],
                            'ptr_domain' : self._arguments['domain'],
                           }
                          )
        cmd = NetworkAddPtrCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('PTR record added successfully')
    def _delete_ptr(self, session: Session) -> None:
        self._receiver.set({'ptr_ip'  : self._arguments['ip']})
        cmd = NetworkDeletePtrCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('PTR record removed successfully')
    def _attach_public(self, session: Session) -> None:
        self._receiver.set({'server_name' : self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = NetworkAttachPublicCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Public IP attached successfully')
    def _detach_public(self, session: Session) -> None:
        self._receiver.set({'ip'   : self._arguments['ip']})
        self._receiver.set({'server_name' : self._arguments['name']})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = NetworkPortIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'port_id' : self._invoker.get_result()})
        cmd = NetworkDetachPublicCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Public IP detached successfully')
    def _add_float_ip(self, session: Session) -> None:
        self._receiver.set({'float_ip_description' : self._arguments['description']})
        cmd = NetworkAddFloatIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Float IP created successfully')
    def _delete_float_ip(self, session: Session) -> None:
        self._receiver.set({'float_ip' : self._arguments['ip']})
        cmd = NetworkFloatIpIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'float_ip_id' : self._invoker.get_result()})
        cmd = NetworkDeleteFloatIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print(f'Float IP deleted successfully')
    def _list_float_ip(self, session: Session) -> None:
        cmd = NetworkListFloatIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        float_ips_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = float_ips_list[0].keys()
        for float_ip in float_ips_list:
            pt.add_row(float_ip.values())
        print(pt)
    def _attach_float_ip(self, session: Session) -> None:
        self._receiver.set({'float_ip'    : self._arguments['float_ip'],
                            'ip'          : self._arguments['private_ip'],
                            'server_name' : self._arguments['name'],
                           }
                          )
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = NetworkSubnetIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'subnet_id' : self._invoker.get_result()})
        cmd = NetworkPortIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'port_id' : self._invoker.get_result()})
        cmd = NetworkFloatIpIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'float_ip_id' : self._invoker.get_result()})
        cmd = NetworkAttachFloatIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Float IP attached successfully')
    def _detach_float_ip(self, session: Session) -> None:
        self._receiver.set({'ip' : self._arguments['ip']})
        cmd = NetworkPortIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'port_id' : self._invoker.get_result()})
        cmd = NetworkDetachFloatIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Float IP detached successfully')
    def _create_private_network(self, session: Session) -> None:
        self._receiver.set({'private_network_name' : self._arguments['name']})
        self._receiver.set({'private_network_cidr' : self._arguments['cidr']})
        cmd = NetworkCreatePrivateCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Private network created successfully')
    def _delete_private_network(self, session: Session) -> None:
        self._receiver.set({'subnet_name' : self._arguments['name']})
        cmd = NetworkSubnetIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'subnet_id' : self._invoker.get_result()})
        cmd = NetworkDeletePrivateCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Private network deleted successfully')
    def _attach_private_ip(self, session: Session) -> None:
        self._receiver.set({'network_name'  : self._arguments['name']})
        self._receiver.set({'server_name'   : self._arguments['server']})
        self._receiver.set({'private_ip'    : self._arguments['private_ip']})
        cmd = NetworkIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'network_id' : self._invoker.get_result()})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = NetworkAttachPrivateIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Private IP attached successfully')
    def _detach_private_ip(self, session: Session) -> None:
        self._receiver.set({'network_name'  : self._arguments['name']})
        self._receiver.set({'server_name'   : self._arguments['server']})
        self._receiver.set({'ip'            : self._arguments['private_ip']})
        cmd = NetworkPortIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'port_id' : self._invoker.get_result()})
        cmd = ServerIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        self._receiver.set({'server_id' : self._invoker.get_result()})
        cmd = NetworkDetachPrivateIpCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        print('Private IP detached successfully')
    def _prepare_command_table(self) -> None:
        self._command_table = {'ls'             : self._get_list,
                               'list-servers'   : self._get_servers,
                               'add-ptr'        : self._add_ptr,
                               'delete-ptr'     : self._delete_ptr,
                               'attach-public'  : self._attach_public,
                               'detach-public'  : self._detach_public,
                               'add-float'      : self._add_float_ip,
                               'list-float'     : self._list_float_ip,
                               'delete-float'   : self._delete_float_ip,
                               'attach-float'   : self._attach_float_ip,
                               'detach-float'   : self._detach_float_ip,
                               'create-network' : self._create_private_network,
                               'delete-network' : self._delete_private_network,
                               'attach-private' : self._attach_private_ip,
                               'detach-private' : self._detach_private_ip,
                              }
    def run(self, command: str, session: Session, arguments: dict) -> None:
        self._arguments = arguments
        if command in self._command_table:
            self._command_table[command](session)
        else:
            raise ValueError(key)

class ImageEntitiy:
    def __init__(self) -> None:
        self._prepare_command_table()
        self._arguments = None
        self._receiver = Receiver()
        self._invoker = Invoker()
    def _get_id(self, session: Session) -> None:
        self._receiver.set({'image_name': self._arguments['name']})
        self._receiver.set({'image_type': self._arguments['type']})
        self._receiver.set({'image_version': self._arguments['version']})
        cmd = ImageIdCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        image_id = self._invoker.get_result()
        print(f'Image ID is: {image_id}')
    def _get_list(self, session: Session) -> None:
        self._receiver.set({'image_type': self._arguments['type']})
        cmd = ImagesListCommand(self._receiver, session)
        self._invoker.store_command(cmd)
        self._invoker.execute_command()
        images_list = self._invoker.get_result()
        pt = PrettyTable()
        pt.field_names = images_list[0].keys()
        for image in images_list:
            pt.add_row(image.values())
        print(pt)
    def _prepare_command_table(self) -> None:
        self._command_table = {'id' : self._get_id,
                               'ls' : self._get_list
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
        super().__init__(subparsers, {'id'      :  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'status'  :  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'ls'      :  [[],
                                                 ],
                                      'reboot'  :  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'poweroff':  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'poweron' :  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'delete'  :  [['"--name"'   , 'help="Name of the server"'],
                                                 ],
                                      'resize'  :  [['"--name"'   , 'help="Name of the server"'],
                                                   ['"--resource"', 'help="New resources of the desired server"'],
                                                 ],
                                      'rename'  :  [['"--name"'   , 'help="Name of the server"'],
                                                   ['"--new-name"', 'help="New name of the desired server"'],
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

class NetworkEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'ls'              : [[],
                                                          ],
                                      'list-servers'    : [['"--name"'            , 'help="Name of the network"'],
                                                          ],
                                      'add-ptr'         : [['"--ip"'              , 'help="IP address that the PTR record will be assigned to"'],
                                                           ['"--domain"'           , 'help="Domain of the PTR record"'],
                                                          ],
                                      'delete-ptr'      : [['"--ip"'              , 'help="IP address that the PTR record will be removed from"'],
                                                          ],
                                      'attach-public'   : [['"--name"'            , 'help="Name of desired server"'],
                                                          ],
                                      'detach-public'   : [['"--ip"'              , 'help="Public IP address that will be detached from server"'],
                                                           ['"--name"'            , 'help="Name of desired server"']
                                                          ],
                                      'add-float'       : [['"--description"'     , 'help="Description of the new float IP"'],
                                                          ],
                                      'list-float'      : [[],
                                                          ],
                                      'delete-float'    : [['"--ip"'              , 'help="Desired float IP to be removed"'],
                                                          ],
                                      'attach-float'    : [['"--float-ip"'        , 'help="Desired float IP to be attached"'],
                                                           ['"--private-ip"'      , 'help="Desired private IP"'],
                                                           ['"--name"'            , 'help="Desired server"'],
                                                          ],
                                      'detach-float'    : [['"--ip"'              , 'help="Desired private IP"'],
                                                          ],
                                      'create-network'  : [['"--name"'            , 'help="Name of the private network"'],
                                                           ['"--cidr"'            , 'help="CIDR of the private network"'],
                                                          ],
                                      'delete-network'  : [['"--name"'            , 'help="Name of the private network"'],
                                                          ],
                                      'attach-private'  : [['"--name"'            , 'help="Name of the private network"'],
                                                           ['"--server"'          , 'help="Name of desired server"'],
                                                           ['"--private-ip"'              , 'help="Desired private IP to be attached to the server"'],
                                                          ],
                                      'detach-private'  : [['"--name"'            , 'help="Name of the private network"'],
                                                           ['"--server"'          , 'help="Name of the server"'],
                                                           ['"--private-ip"'      , 'help="Desired Private IP to be detached"'],
                                                          ]
                                     }
                        )
    def __call__(self) -> None:
        self._entity = NetworkEntitiy()
        return self._entity

class ImageEntityBuilder(EntityBuilder):
    def __init__(self, subparsers: _SubParsersAction) -> None:
        super().__init__(subparsers, {'id': [['"--name"'   , 'help="Name of the image"'],
                                             ['"--type"'   , 'help="type of the desired image"'],
                                             ['"--version"', 'help="version of the desired image"'],
                                            ],
                                      'ls': [['"--type"'   , 'help="type of the desired image"'],
                                            ],
                                     }
                        )
    def __call__(self) -> None:
        self._entity = ImageEntitiy()
        return self._entity
