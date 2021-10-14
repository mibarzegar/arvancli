import json
import arvancli.common.utils as utils
from arvancli.common.command import Command
from arvancli.common.receiver import Receiver
from arvancli.common.utils import Session

class RegionsListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        url = 'https://napi.arvancloud.com/ecc/v1/regions'
        self._session.send_request('GET', url)
        regions_json_array = self._session.get_json_response()["data"]
        regions_list = []
        for region in regions_json_array:
            region_json = {}
            region_json["Country"] = region["country"]
            region_json["City"] = region["city"]
            region_json["Datacenter"] = region["dc"]
            region_json["Code"] = region["code"]
            region_json["Available"] = region["create"]
            region_json["Coming Soon"] = region["soon"]
            regions_list.append(region_json)
        return regions_list
