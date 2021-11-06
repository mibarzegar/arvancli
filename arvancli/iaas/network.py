import json
import arvancli.common.utils as utils
from arvancli.common.command import Command
from arvancli.common.receiver import Receiver
from arvancli.common.utils import Session

class NetworkListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/networks'
        self._session.send_request('GET', url)
        networks_json_array = self._session.get_json_response()["data"]
        networks_list = []
        for network in networks_json_array:
            for subnet in network['subnets']:
                network_json = {}
                network_json['Network Name'] = network['name'] if network['name'].isascii() else "Default network"
                network_json['Network Status'] = network['status'].lower()
                network_json["Network Type"] = "public" if not network['name'].isascii() else "private"
                network_json['Subnet Name'] = subnet['name']
                network_json['Subnet CIDR'] = subnet['cidr']
                network_json['Server(s)'] = ""
                for server in subnet['servers']:
                    network_json['Server(s)'] += f'{server["name"]},'
                network_json['Server(s)'] = network_json['Server(s)'][:-1]
                networks_list.append(network_json)
        return networks_list

class NetworkServersListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/networks'
        self._session.send_request('GET', url)
        networks_json_array = self._session.get_json_response()["data"]
        try:
            selected_network_json = next(element for element in networks_json_array if ((element['name'] == self._receiver.get('network_name')) or (not element['name'].isascii()  and self._receiver.get('network_name') == 'Default network')))
        except StopIteration:
            print(f'{self._receiver.get("network_name")} not found!')
            sys.exit(1)
        servers_list = []
        public_network  = True if self._receiver.get('network_name') == 'Default network' else False
        for subnet in selected_network_json['subnets']:
            for server in subnet['servers']:
                for ip in server['ips']:
                    if ip['public'] == public_network:
                        server_json = {}
                        server_json['Name'] = server['name']
                        server_json['IP Address'] = ip['ip']
                        server_json['MAC Address'] = ip['mac_address']
                        server_json['Port Security'] = 'enabled' if ip['port_security_enabled'] else 'disabled'
                        if ip['public']:
                            server_json['PTR record'] = ip['ptr'] if ip['ptr'] else ''
                        if not ip['public']:
                            server_json['Float IP'] = ip['float_ip'] if ip['float_ip'] else ''
                        servers_list.append(server_json)
        return servers_list

class NetworkAddPtrCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/ptr'
        body = {'domain' : self._receiver.get('ptr_domain'),
                'ip'     : self._receiver.get('ptr_ip'),
               }
        self._session.send_request('POST', url, body=json.dumps(body))

class NetworkDeletePtrCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/ptr/{ptr_ip}'
        url = raw_url.format(ptr_ip=self._receiver.get('ptr_ip'))
        self._session.send_request('DELETE', url)

class NetworkAttachPublicCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}/add-public-ip'
        url = raw_url.format(server_id=self._receiver.get('server_id'))
        body = {}
        self._session.send_request('POST', url, body=json.dumps(body))

class NetworkPortIdCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/networks'
        self._session.send_request('GET', url)
        networks_json_array = self._session.get_json_response()["data"]
        networks_list = []
        for network in networks_json_array:
            for subnet in network['subnets']:
                for server in subnet['servers']:
                    for ip in server['ips']:
                        if ip['ip'] == self._receiver.get('public_ip'):
                            return ip['port_id']

class NetworkDetachPublicCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/networks/{port_id}/detach'
        url = raw_url.format(port_id=self._receiver.get('port_id'))
        body = {}
        body['server_id'] = self._receiver.get('server_id')
        self._session.send_request('PATCH', url, body=json.dumps(body))
