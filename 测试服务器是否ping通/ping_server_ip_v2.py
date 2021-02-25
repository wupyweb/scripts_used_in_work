import re
import os
import csv


# 获取csv文件中IP
def get_hosts(file_path="ip.csv"):
    with open(file_path, newline="") as f:
        data = csv.reader(f)
        hosts = [host[0] for host in data]
    return hosts


def true_false(host):
    output = os.popen("ping {} -n 1".format(host)).read()
    result = re.findall(r"(\d+)% 丢失", output)
    if result[0] == '0':
        return True
    else:
        return False


def ping_ip(host):
    for i in range(3):
        flag = true_false(host)
        if flag:
            print(host, "ok")
            break
        else:
            print(host, "fail")


if __name__ == '__main__':
    for host in get_hosts():
        ping_ip(host)
