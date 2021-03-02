import csv

import paramiko


# 获取csv文件中IP
def get_hosts(file_path="ip.csv"):
    with open(file_path, newline="") as f:
        data = csv.reader(f)
        hosts = [host[0] for host in data]
    return hosts


# 方法一
def do_ssh(host):
    # 实例化一个ssh客户端
    client = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接
    client.connect(hostname=host, port=22, username='pi', password='dgzmtfj0769')

    for command in get_commands():
        # 接收标准输入，标准输出和错误
        stdin, stdout, stderr = client.exec_command(command)
        # 解码并打印信息
        print(host)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        with open("log.txt", "a") as file:
            file.write(host + "\n")
            file.write(stdout.read().decode('utf-8'))
            file.write(stderr.read().decode('utf-8'))

    client.close()


# 方法二
def do_sshd(host, new_host):
    t = paramiko.Transport((host, 22))
    t.connect(username='pi', password='dgqxfj0769')

    ssh = paramiko.SSHClient()
    ssh._transport = t
    ssh.exec_command()

def get_commands():
    commands = [
        # "sudo sed -i 's@=.*/24@={}/24@' /etc/dhcpcd.conf".format(new_host),
        # "cat /etc/dhcpcd.conf | grep ip_address"
        # "service identify stop",
        # "rm -f /opt/identify/lib/iaac-identify-4.2.1.jar",
        # "service identify start"
        # "sudo tar -xzvf /home/pi/omxplayer-distV16-2019-08-27.tgz -C /",
        # "sudo reboot",
        "sudo unzip -o /home/pi/one.zip -d /home/pi",
        "sudo cp /home/pi/one/rc.local /etc/",
        "sudo tar -xzvf /home/pi/one/vce-v1.1-clean-20200315.tar.gz -C /",
        "sudo crontab /usr/local/shell/mycron",
        "sudo tar -xzvf /home/pi/one/omxplayer-distV18-2020-03-27.tgz -C /",
        "sudo cp -f /home/pi/one/omxplayer-distV18-2020-03-27.tgz /usr/bin/omxplayer/omxplayer-dist_bak.tgz",
        # "sudo reboot"
        # "ls /usr/local/shell/"
    ]
    return commands


if __name__ == '__main__':
    # ip_file = "ip.csv"
    for host in get_hosts():
        try:
            do_ssh(host)
        except:
            with open("error.txt", "a") as file:
                file.write("{} 异常！\n".format(host))
