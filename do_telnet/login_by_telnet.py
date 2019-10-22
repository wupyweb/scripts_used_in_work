import csv
import telnetlib


def do_telnet(host, username, password, finish, bash_file):
    # 连接telnet服务器
    tn = telnetlib.Telnet(host, port=23, timeout=10)
    tn.set_debuglevel(2)

    # 输入登陆用户名
    tn.read_until(match=b"(none) login: ")
    tn.write(username.encode('ascii') + b"\n")

    # 输入登陆密码
    tn.read_until(match=b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

    # 登陆完毕后执行命令
    tn.read_until(finish)
    # 把bash.txt中的脚本写入到/tmp/test.sh文件
    # 然后执行test.sh脚本
    with open(bash_file, "rb") as f:
        commands = f.readlines()
        tn.write(b"echo '#!/bin/sh' > /tmp/test.sh\n")
        for command in commands:
            tn.write(b'echo "%s" >> /tmp/test.sh\n' % command.strip())
    tn.write(b"sh /tmp/test.sh\n")

    # 执行完毕后，终止telnet连接
    tn.write(b"exit\n")
    print(host + " finished")
    print(tn.read_all().decode('utf8'))


# 获取csv文件中IP
def get_hosts(file_path):
    with open(file_path, newline="") as f:
        data = csv.reader(f)
        hosts = [host[0] for host in data]
    return hosts


def main():
    username = "root"
    passwd = "123"
    finish = b"~ # "
    ip_file = "ip.csv"
    bash_file = "bash.txt"

    for host in get_hosts(ip_file):
        do_telnet(host, username, passwd, finish, bash_file)


if __name__ == '__main__':
    main()
