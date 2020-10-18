import time
from urllib.parse import urljoin
import requests
import json


class ApiClient:
    def __init__(self, config):
        self.base_url = 'https://target.my.com/'
        self.session = requests.Session()
        self.csrf_token = None
        self.email = config.email
        self.password = config.password
        self.login()

    def login(self):
        auth_url = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'email': self.email,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email'
        }

        self._request(method='POST', url=auth_url, data=data, headers=headers)
        self.get_token()

    def _request(self, method, url=None, location=None, headers=None, data=None, json=None):
        if location:
            url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data)

        if json:
            return response.json()
        return response

    def get_token(self):
        headers = {
            'Referer': 'https://target.my.com/auth/mycom?state=target_login%3D1',
        }
        self._request(method='GET', location='csrf', headers=headers)
        self.csrf_token = self.session.cookies.get('csrftoken')

    def check_if_exists(self, segment_id):
        segment_list_url = f"""https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,
        relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,
        flags&limit=500&_={time.time()}"""
        response = self._request(method='GET', url=segment_list_url, json=True)
        item = [item for item in response.get('items') if item.get('id') == segment_id]
        return item or False

    def segment_create(self, name):
        create_url = """https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,
        relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,
        flags """

        data = json.dumps({
            "name": name,
            "pass_condition": 1,
            "logicType": "or",
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }
            ]
        })

        headers = {
            "Content-Type": "application/json",
            "Referer": "https://target.my.com/segments/segments_list/new",
            'X-CSRFToken': self.csrf_token
        }
        response = self._request(method="POST", url=create_url, data=data, headers=headers, json=True)
        return response.get('id')

    def segment_delete(self, segment_id):
        segment_delete_url = """https://target.my.com/api/v2/remarketing/segments/{}.json"""

        headers = {
            "Referer": "https://target.my.com/segments/segments_list",
            'X-CSRFToken': self.csrf_token
        }

        self._request(method="DELETE", url=segment_delete_url.format(segment_id), headers=headers)