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
            selected_instance_id_json = next(element for element in instance_id_json_array if element['name'] == self._receiver.get('name'))
        except StopIteration:
            print(f'{self._receiver.get("name")} not found!')
            sys.exit(1)
        instance_id = selected_instance_id_json['id']
        return instance_id 

class ServerStatusCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        id = self._receiver.get('id')
        raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/servers/{server_id}'
        url = raw_url.format(server_id=id)
        self._session.send_request('GET', url)
        instance_status = self._session.get_json_response()['data']['status']
        return instance_status
