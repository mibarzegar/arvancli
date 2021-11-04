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
