import json
import sys
import arvancli.common.utils as utils
from arvancli.common.command import Command
from arvancli.common.receiver import Receiver
from arvancli.common.utils import Session

class ServerIdCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/servers'
        self._session.send_request('GET', url) 
        instance_id_json_array = self._session.get_json_response()['data']
        try:
            selected_instance_id_json = next(element for element in instance_id_json_array if element['name'] == self._receiver.get('server_name'))
        except StopIteration:
            print(f'{self._receiver.get("server_name")} not found!')
            sys.exit(1)
        instance_id = selected_instance_id_json['id']
        return instance_id 

class ServerStatusCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}'
        url = raw_url.format(server_id=self._receiver.get('server_id'))
        self._session.send_request('GET', url)
        instance_status = self._session.get_json_response()['data']['status']
        return instance_status

class ServersListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/servers'
        self._session.send_request('GET', url)
        servers_json_array = self._session.get_json_response()["data"]
        servers_list = []
        for server in servers_json_array:
            server_json = {}
            server_json["Name"] = server["name"]
            server_json["Status"] = server["status"]
            server_json["Operating System"] = server["image"]["name"]
            resouce_desc = server["flavor"]["id"].split("-")
            server_json["Resource"] = resouce_desc[2] + " vCPU - " + resouce_desc[1] + " GB RAM - " + resouce_desc[3] + " GB Disk"
            server_json["Username"] = server["image"]["metadata"]["username"]
            addresses_json_array = server ["addresses"]
            ips_list = []
            for network in addresses_json_array:
                network_ips = addresses_json_array[network]
                for ip in network_ips:
                    server_ip = ip["addr"]
                    if "public" in network:
                        ips_list.append(f'public:{server_ip}')
                        string = ",".join(ips_list)
                        server_json["IP Address(es)"] = string
                    else:
                        ips_list.append(f'private:{server_ip}')
                        string = ",".join(ips_list)
                        server_json["IP Address(es)"] = string
            servers_list.append(server_json)
        return servers_list

class ServerRebootCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}/reboot'
        url = raw_url.format(server_id=self._receiver.get('server_id'))
        self._session.send_request('POST', url)

class ServerPoweroffCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}/power-off'
        url = raw_url.format(server_id=self._receiver.get('server_id'))
        self._session.send_request('POST', url)
