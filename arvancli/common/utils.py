import requests

class Session:
    def  __init__(self, token: str, zone: str) -> None:
        self._zone = zone
        self._session = requests.Session()
        self._prepare_headers(token)
    def send_request(self, method: str, raw_url: str) -> None:
        url = raw_url.format(zone=self._zone)
        if method == 'GET':
           self._response = self._session.get(url, headers=self._headers)
        else:
           raise ValueError(method)
    def get_json_response(self) -> dict:
        return self._response.json()
    def _prepare_headers(self, token: str) -> None:
        self._headers = {'Authorization': f'Apikey {token}', 
                         'Content-Type': 'application/json;charset=utf-8'
                        }
