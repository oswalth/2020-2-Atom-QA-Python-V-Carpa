import os
import pathlib
import re
import json
import pandas as pd
import sys


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


def preprocess(filename):
    table = []
    columns = ['IPv4', 'Datetime', 'Method', 'Url', 'Req_ver', 'Code_status', 'Size', 'O1', 'O2', '03']
    pattern = re.compile(r"(^\d{1,3}(?:\.\d{1,3}){3}).*\[([0-3][0-9]\/[A-z][a-z]{2}\/\d{4}:[0-2][0-9]:[0-5][0-9]:["
                         r"0-5][0-9]\s\+\d{4})\]\s\"(\S*)\s(\S*)\s(\S*)\"\s([1-5]\d{2})\s(\S*)\s\"(.*)\"\s\"("
                         r".*)\"\s\"(.*)\"")

    with open(filename) as f_obj:
        try:
            for line in f_obj:
                table.append(pattern.match(line).groups())
        except AttributeError:
            return

    table = pd.DataFrame(table, columns=columns)
    return table


def process_log(filename, output_dir):
    output = {}
    log_table = preprocess(filename)
    functions = [count_requests, count_requests_by_type, biggest_requests, biggest_client_error, biggest_server_error]
    if log_table is None:
        print(f"{filename} can not be processed")
        return

    for func in functions:
        output[func.__name__] = func(log_table)

    file = filename.split("/")[-1]
    with open(os.path.join(output_dir, f"{file.split('.')[0]}.result"), 'w') as f_obj:
        json.dump(output, f_obj)


def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            cwd = sys.argv[1]
        else:
            print(f'Invalid path: {sys.argv[1]}')
            return
    else:
        cwd = pathlib.Path.cwd()

    output_dir = os.path.join(cwd, 'python_output')

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    log_dir = os.path.join(cwd, 'logs')

    for file in os.listdir(log_dir):
        if file.endswith('.log'):
            process_log(os.path.join(log_dir, file), output_dir)


if __name__ == '__main__':
    main()

