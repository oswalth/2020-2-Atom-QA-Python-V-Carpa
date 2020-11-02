import datetime

import pytest

from models.models import Log
from orm_client.mysql_orm_client import MySqlOrmConnector
from tests.orm_builder import MySqlBuilder


class TestOrm:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MySqlOrmConnector = mysql_orm_client
        self.builder: MySqlBuilder = MySqlBuilder(connection=self.mysql)

    def test_obj_create(self):
        filename = 'TEST_FILE.log'
        log = {
            'ipv4': '134.249.53.185',
            'datetime': datetime.datetime.strptime('27/May/2016:03:32:09 +0200', "%d/%b/%Y:%H:%M:%S %z").
                    replace(tzinfo=None),
            'method': 'POST',
            'url': 'TEST_LOG_URL',
            'req_ver': 'HTTP/1.1',
            'code_status': 200,
            'size': 4498,
            'option_1': '-',
            'option_2': '-',
            'option_3': '-'
        }
        file_id = self.builder.add_file(filename).id
        self.builder.add_log(log, file_id)
        orm_log = (self.mysql.session.query(Log).filter_by(url='TEST_LOG_URL')).one().__dict__
        flag = True
        for key in log.keys():
            if log[key] != orm_log[key]:
                flag = False
                break
        assert flag
