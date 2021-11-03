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

class FirewallRulesCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = "https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities"
        self._session.send_request('GET', url)
        rules_list = []
        firewalls_json_array = self._session.get_json_response()["data"]
        try:
            selected_firewall_json = next(element for element in firewalls_json_array if element['name'] == self._receiver.get('name'))
        except StopIteration:
            print(f'{self._receiver.get("name")} not found!')
            sys.exit(1)
        number = 0
        for rule in selected_firewall_json["rules"]:
            rule_json = {}
            number += 1
            rule_json["#"] = number
            rule_json["Type"] = rule["ether_type"]
            rule_json["Direction"] = rule["direction"]
            rule_json["Protocol"] = rule["protocol"] if rule["protocol"] != "" else "All"
            rule_json["Ports"] = "All" if (rule["port_start"] == None and rule["port_end"] == None) else str(rule["port_start"]) + "-" + str(rule["port_end"])
            rule_json["Origin/Destination"]  = rule["ip"] if rule["ip"] != "" else "All"
            rule_json["Access Type"] = "Available"
            rules_list.append(rule_json)
        return(rules_list)

class FirewallAddRuleCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('id')
        raw_url = "https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/securities/security-rules/{firewall_id}"
        url = raw_url.format(firewall_id=id)
        self._session.send_request('GET', url)
        body = {"description":"",
                "direction":"",
                "ips":["any"],
                "port_from":"",
                "port_to":"",
                "protocol":""
        }
        body["description"] = self._receiver.get('description')
        body["direction"] = self._receiver.get('direction')
        if self._receiver.get('cidr'):
            cidrs = [cidr.strip() for cidr in self._receiver.get('cidr').split(",")]
            body["ips"] = cidrs
        if self._receiver.get('port'):
            ports = [port.strip() for port in self._receiver.get('port').split(":")]
            body["port_from"] = ports[0]
            if len(ports) == 2:
                body["port_to"] = ports[1]
            else:
                body["port_to"] = ports[0]
        body["protocol"] = self._receiver.get('protocol')
        self._session.send_request('POST', url, body=json.dumps(body))

class FirewallRuleIdCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = "https://napi.arvancloud.com/ecc/v1/regions/{zone}/securities"
        self._session.send_request('GET', url)
        firewalls_json_array = self._session.get_json_response()['data']
        selected_firewall_json = next(element for element in firewalls_json_array if element['name'] == self._receiver.get('name'))
        rule_id = selected_firewall_json["rules"][int(self._receiver.get('number'))-1]["id"]
        return rule_id

class FirewallDeleteRuleCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('id')
        raw_url = "https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/securities/security-rules/{rule_id}"
        url = raw_url.format(rule_id=id)
        self._session.send_request('DELETE', url)

class FirewallAttachServerCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('server_id')
        raw_url = "https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}/add-security-group"
        url = raw_url.format(server_id=id)
        body = {"security_group_id":""}
        body["security_group_id"] = self._receiver.get('firewall_id')
        self._session.send_request('POST', url, body=json.dumps(body))

class FirewallDetachServerCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('server_id')
        raw_url = "https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}/remove-security-group"
        url = raw_url.format(server_id=id)
        body = {"security_group_id":""}
        body["security_group_id"] = self._receiver.get('firewall_id')
        self._session.send_request('POST', url, body=json.dumps(body))
