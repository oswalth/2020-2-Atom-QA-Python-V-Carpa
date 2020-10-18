from tests.base import BaseCase
import pytest
import uuid


class TestTargetAPI(BaseCase):
    @pytest.mark.API
    def test_login(self):
        response = self.api_client._request(method='GET', location='billing')
        assert self.api_client.email in response.text

    @pytest.mark.API
    def test_segment_create(self):
        name = str(uuid.uuid4()) + '__create'
        segment_id = self.api_client.segment_create(name)
        self.api_client.check_if_exists(segment_id)
        assert self.api_client.check_if_exists(segment_id)

    @pytest.mark.API
    def test_segment_delete(self):
        name = str(uuid.uuid4()) + '__delete'
        segment_id = self.api_client.segment_create(name)
        self.api_client.segment_delete(segment_id)
        assert not self.api_client.check_if_exists(segment_id)
