import requests
from urllib.parse import urljoin


class ApiClient:
    def __init__(self, config):
        self.base_url = config.URL

    def get_users(self):
        users_url = urljoin(self.base_url, 'users')
        users_list = requests.get(users_url).json()

        return users_list

    def get_posts(self):
        posts_url = urljoin(self.base_url, 'posts')
        posts_list = requests.get(posts_url).json()

        return posts_list