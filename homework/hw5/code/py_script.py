import os
import pathlib
import re
from datetime import datetime
import sys

from homework.hw5.code.models.models import File, Log
from homework.hw5.code.orm_builder import MySqlBuilder
from homework.hw5.code.orm_client.mysql_orm_client import MySqlOrmConnector


def count_requests(log_table):
    return log_table.shape[0]


def count_requests_by_type(log_table):
    request_type_count = log_table.groupby(by="Method")['IPv4'].count().to_dict()
    return {k: v for k, v in request_type_count.items() if re.match(r"^[A-Z]{3,}", k)}


def biggest_requests(log_table):
    log_table['Size'] = log_table['Size'].replace('-', 0)
    log_table['Size'] = log_table['Size'].astype(int)
    return log_table.sort_values(by='Size', ascending=False).iloc[:10, [3, 5, 6]].values.tolist()


def biggest_client_error(log_table):
    client_error = log_table[log_table['Code_status'].str.startswith("4")]
    group_count = client_error.groupby(by=['Url', 'Code_status', 'IPv4']).size().reset_index(name="Count")
    return group_count.sort_values(by='Count', ascending=False).iloc[:10, [0, 1, 2, 3]].values.tolist()


def biggest_server_error(log_table):
    server_error = log_table[log_table['Code_status'].str.startswith("5")]
    return server_error.sort_values(by="Size", ascending=False).iloc[:, [0, 3, 6]][:10].values.tolist()




class Loggggger:
    def __init__(self):
        self.mysql = MySqlOrmConnector(user='root', password='cpu#N7ZvD6', db_name="ORM_LOGGER")
        self.builder = MySqlBuilder(connection=self.mysql)
        self.cwd = self.get_cwd()
        self.output_dir = self.get_output()
        self.log_dir = os.path.join(self.cwd, 'logs')
        self.pattern = re.compile(
            r"^(?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}).*\[(?P<datetime>[0-3][0-9]\/[A-z][a-z]{2}\/\d{4}:[0-2][0-9]:[0-5][0-9]:["
            r"0-5][0-9]\s\+\d{4})\]\s\"(?P<method>\S*)\s(?P<url>\S*)\s(?P<req_ver>\S*)\"\s(?P<code_status>[1-5]\d{2})\s(?P<size>\S*)\s\"(?P<option_1>.*)\"\s\"("
            r"?P<option_2>.*)\"\s\"(?P<option_3>.*)\"")

        self.run()

    def get_output(self):
        output_dir = os.path.join(self.cwd, 'python_output')

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        return output_dir

    @staticmethod
    def get_cwd():
        if len(sys.argv) > 1:
            if os.path.isdir(sys.argv[1]):
                return sys.argv[1]
            else:
                print(f'Invalid path: {sys.argv[1]}')
                return None
        else:
            return pathlib.Path.cwd()

    def get_log_values(self, line):
        try:
            log = self.pattern.match(line).groupdict()
            log['datetime'] = datetime.strptime(log['datetime'], "%d/%b/%Y:%H:%M:%S %z")
            log['code_status'] = int(log['code_status'])
            if log['size'].isdigit():
                log['size'] = int(log['size'])
            else:
                log['size'] = 0
            return log
        except AttributeError:
            return None

    def run(self):
        for filename in os.listdir(self.log_dir):
            if filename.endswith('.log'):
                file_id = self.builder.add_file(filename=filename).id
                with open(os.path.join(self.log_dir, filename)) as f_obj:
                    try:
                        for line in f_obj:
                            log = self.get_log_values(line)
                            if not log:
                                continue
                            self.builder.add_log(log, file_id)
                    except AttributeError:
                        return
            # files = self.mysql.session.query(File).all()
            # logs = self.mysql.session.query(Log).all()

def main():
    loggggger = Loggggger()
    loggggger.run()


if __name__ == '__main__':
    main()
