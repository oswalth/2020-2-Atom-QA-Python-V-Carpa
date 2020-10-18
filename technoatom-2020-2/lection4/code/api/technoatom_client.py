from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


class TechnoAtomClient:
    def __init__(self, user, password):
        self.base_url = 'https://technoatom.mail.ru'

        self.session = requests.Session()
        self.csrf_token = None

        self.user = user
        self.password = password
        self.login()

    def login(self):
        location = 'login'

        csrf_token = self.get_token()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'csrftoken={csrf_token}'
        }

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'login': self.user,
            'password': self.password
        }

        response = self._request('POST', location, headers=headers, data=data, json=False)
        cookies = response.headers['Set-Cookie'].split(';')
        new_csrf_token = [ c for c in cookies if c.startswith('csrftoken=')][0].split('=')[-1]
        session_id_gtp = [c for c in cookies if 'secure, sessionid-gtp=' in c][0].split('=')[-1]

        self.csrf_token = new_csrf_token
        self.session.cookies = cookiejar_from_dict({'csrftoken': new_csrf_token, 'session_id_gtp': session_id_gtp})

        return response.json()

    def _request(self, method, url, location, headers, data, json):
        if location:
            url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data)

        if json:
            return response.json()
        return response

    def get_token(self):
        location = 'pages/index'
        headers = self._request('GET', location, json=False).headers
        return headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def get_feed(self, feed_type='my'):
        location = 'feed/update/stream'
        params = {'type': feed_type}

        return self._request('GET', location)