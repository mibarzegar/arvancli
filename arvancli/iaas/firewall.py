import json
import sys
import arvancli.common.utils as utils
from arvancli.common.command import Command
from arvancli.common.receiver import Receiver
from arvancli.common.utils import Session

class FirewallsListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities'
        self._session.send_request('GET', url)
        firewalls_json_array = self._session.get_json_response()["data"]
        firewalls_list = []
        for firewall in firewalls_json_array:
            firewalls_json = {}
            firewalls_json["Name"] = firewall["name"]
            firewalls_json["Description"] = firewall["description"]
            firewalls_json["Real Name"] = firewall["real_name"]
            if firewall["abraks"] != None:
                firewalls_json["Servers"] = ",".join([ (server["name"]) for server in firewall["abraks"] ])
            else:
                firewalls_json["Servers"] = ""
            firewalls_list.append(firewalls_json)
        return(firewalls_list)

class FirewallIdCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities'
        self._session.send_request('GET', url)
        firewalls_json_array = self._session.get_json_response()["data"]
        try:
            selected_firewall_json = next(element for element in firewalls_json_array if element['name'] == self._receiver.get('name'))
        except StopIteration:
            print(f'{self._receiver.get("name")} not found!')
            sys.exit(1)
        firewall_id = selected_firewall_json['id']
        return(firewall_id)

class FirewallCreateCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        if self._receiver.get('name') == "arCDN":
            url = "https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities/cdn"
        else:
            url = "https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities"
        if self._receiver.get('name') != "arCDN":
            body = { "name": "",
                     "description": ""
                   }
            body["name"] = self._receiver.get('name')
            body["description"] = self._receiver.get('description')
            self._session.send_request('POST', url, body=json.dumps(body))
            firewall_details = self._session.get_json_response()["data"]
            if firewall_details["id"] == None:
                raise Exception("Security group creation failed")
                sys.exit(1)
        else:
            self._session.send_request('POST', url)
        return(self._receiver.get('name'))

class FirewallDeleteCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('id')
        raw_url = "https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/securities/{firewall_id}"
        url = raw_url.format(firewall_id=id)
        self._session.send_request('DELETE', url)
