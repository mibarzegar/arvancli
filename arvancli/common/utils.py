import requests

class Session:
    def  __init__(self, token: str, zone: str) -> None:
        self._zone = zone
        self._session = requests.Session()
        self._prepare_headers(token)
    def send_request(self, method: str, raw_url: str, **kwargs) -> None:
        url = raw_url.format(zone=self._zone)
        if method == 'GET':
           self._response = self._session.get(url, headers=self._headers)
        elif method == 'POST':
            self._response = self._session.post(url, headers=self._headers, data=kwargs.get('body'))
        elif method == 'DELETE':
            self._response = self._session.delete(url, headers=self._headers)
        elif method == 'PATCH':
            self._response = self._session.patch(url, headers=self._headers, data=kwargs.get('body'))
        else:
           raise ValueError(method)
        self._check_status()
    def _check_status(self):
        try:
            self._response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise Exception(f'Request failed!')
    def get_json_response(self) -> dict:
        return self._response.json()
    def _prepare_headers(self, token: str) -> None:
        self._headers = {'Authorization': f'Apikey {token}', 
                         'Content-Type': 'application/json;charset=utf-8'
                        }
