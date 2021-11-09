import json
import sys
import arvancli.common.utils as utils
from arvancli.common.command import Command
from arvancli.common.receiver import Receiver
from arvancli.common.utils import Session

class ImageIdCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        if self._receiver.get('image_type') == 'marketplace':
            url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/images/marketplace'
        elif self._receiver.get('image_type') == 'distributions' or self._receiver.get('image_type') == 'private':
            raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/images?type={image_type}'
            url = raw_url.format(image_type=self._receiver.get('image_type'))
        elif self._receiver.get('image_type') == 'snapshot':
            url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/images?type=server'
        else:
            raise Exception("Type not found")
            sys.exit(1)
        self._session.send_request('GET', url)
        images_json_array = self._session.get_json_response()['data']
        if self._receiver.get('image_type') == "marketplace":
            selected_image_json = next(element for element in images_json_array if element['name'] == self._receiver.get('image_name') and element['image_version'] == self._receiver.get('image_version'))
            image_id = selected_image_json['id']
        elif self._receiver.get('image_type') == "distributions":
            selected_image_json = next(element for element in images_json_array if element['name'] == self._receiver.get('image_name'))
            selected_version_json = next(element for element in selected_image_json['images'] if element['name'] == self._receiver.get('image_version'))
            image_id = selected_version_json['id']
        else:
            selected_image_json = next(element for element in images_json_array if element['name'] == self._receiver.get('image_name'))
            image_id = selected_image_json['id']
        return image_id

class ImagesListCommand(Command):
    def __init__(self, receiver: Receiver, session: Session) -> None:
        self._receiver = receiver
        self._session = session
        self.result = None
    def execute(self) -> None:
        if self._receiver.get('image_type') == 'marketplace':
            url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/images/marketplace'
        elif self._receiver.get('image_type') == 'distributions' or self._receiver.get('image_type') == 'private':
            raw_url = 'https://napi.arvancloud.com/ecc/v1/regions/{{zone}}/images?type={image_type}'
            url = raw_url.format(image_type=self._receiver.get('image_type'))
        elif self._receiver.get('image_type') == 'snapshot':
            url = 'https://napi.arvancloud.com/ecc/v1/regions/{zone}/images?type=server'
        else:
            raise Exception("Type not found")
            sys.exit(1)
        self._session.send_request('GET', url)
        images_json_array = self._session.get_json_response()["data"]
        images_list = []
        if self._receiver.get('image_type') == "marketplace":
            for image in images_json_array:
                 image_json = {}
                 image_json["Name"] = image["name"]
                 image_json["Version"] = image["image_version"]
                 image_json["SSH Key Support"] = image["ssh_key"]
                 image_json["SSH Password Support"] = image["ssh_password"]
                 images_list.append(image_json)
            return images_list
        elif self._receiver.get('image_type') == "distributions":
            for image in images_json_array:
                 for images in image['images']:
                     image_json = {}
                     image_json["Name"] = images["distribution_name"]
                     image_json["Version"] = images["name"]
                     image_json["SSH Key Support"] = images["ssh_key"]
                     image_json["SSH Password Support"] = images["ssh_password"]
                     images_list.append(image_json)
            return images_list
        else:
            for image in images_json_array:
                 image_json = {}
                 image_json["Name"] = image["name"]
                 image_json["SSH Key Support"] = False
                 image_json["SSH Password Support"] = False
                 images_list.append(image_json)
            return images_list
