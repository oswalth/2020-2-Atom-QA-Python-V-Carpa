from models.models import Base, File, Log
from orm_client.mysql_orm_client import MySqlOrmConnector


class MySqlBuilder:
    def __init__(self, connection: MySqlOrmConnector):
        self.connection = connection
        self.engine = self.connection.connection.engine

        self.create_files()
        self.create_logs()

    def create_files(self):
        if not self.engine.dialect.has_table(self.engine, 'file'):
            Base.metadata.tables['file'].create(self.engine)

    def create_logs(self):
        if not self.engine.dialect.has_table(self.engine, 'log'):
            Base.metadata.tables['log'].create(self.engine)

    def add_file(self, filename):
        file = File(filename=filename)
        self.connection.session.add(file)
        self.connection.session.commit()
        return file

    def add_log(self, log, file_id):
        log = Log(
            file_id=file_id,
            **log
        )
        self.connection.session.add(log)
        self.connection.session.commit()
        return log
