import json
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