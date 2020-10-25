import pytest

from tests.base import BaseCase


class TestAPI(BaseCase):
    def test_simple(self):
        email = "Rey.Padberg@karina.biz"
        users_list = self.api_client.get_users()

        filtered = [u for u in users_list if u['email'] == email]
        user_id = filtered[0]['id']

        posts_list = self.api_client.get_posts()
        filtered_posts = [p for p in posts_list if p['userId'] == user_id]

        assert len(filtered_posts) == 10
