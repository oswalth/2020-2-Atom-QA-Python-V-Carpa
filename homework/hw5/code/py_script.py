import os
import pathlib
import re
from datetime import datetime
import sys

from orm_client.mysql_orm_client import MySqlOrmConnector
from tests.orm_builder import MySqlBuilder


class Loggggger:
    def __init__(self):
        self.mysql = MySqlOrmConnector(user='root', password='cpu#N7ZvD6', db_name="ORM_LOGGER")
        self.builder = MySqlBuilder(connection=self.mysql)
        self.cwd = self.get_cwd()
        self.output_dir = self.get_output()
        self.log_dir = os.path.join(self.cwd, 'logs')
        self.pattern = re.compile(
            r"^(?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}).*\[(?P<datetime>[0-3][0-9]\/[A-z][a-z]{2}\/\d{4}:[0-2][0-9]:[0-5]["
            r"0-9]:["
            r"0-5][0-9]\s\+\d{4})\]\s\"(?P<method>\S*)\s(?P<url>\S*)\s(?P<req_ver>\S*)\"\s(?P<code_status>[1-5]\d{"
            r"2})\s(?P<size>\S*)\s\"(?P<option_1>.*)\"\s\"("
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
            log['datetime'] = str(datetime.strptime(log['datetime'], "%d/%b/%Y:%H:%M:%S %z"))
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


def main():
    loggggger = Loggggger()
    loggggger.run()


if __name__ == '__main__':
    main()
