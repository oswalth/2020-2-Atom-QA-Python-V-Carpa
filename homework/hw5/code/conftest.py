import pytest

from orm_client.mysql_orm_client import MySqlOrmConnector


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MySqlOrmConnector(user='root', password='cpu#N7ZvD6', db_name="ORM_LOGGER")