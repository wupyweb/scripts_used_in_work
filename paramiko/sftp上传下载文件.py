import csv

import paramiko



# 获取csv文件中IP
def get_hosts(file_path="ip.csv"):
    with open(file_path, newline="") as f:
        data = csv.reader(f)
        hosts = [host[0] for host in data]
    return hosts



def sftp_upload_file(host, server_path, local_path):
    try:
        # 实例化一个传输对象
        t = paramiko.Transport((host, 22))
        # 连接
        t.connect(username="pi", password="dgzmtfj0769")
        
        # 实例化一个sftp对象
        sftp = paramiko.SFTPClient.from_transport(t)

        # 上传文件
        sftp.put(local_path, server_path)
        t.close()
        print(host + " upload success!!")
    except Exception as e:
        print(e)
        # with open("upload_error.log", "a") as file:
        #     file.write("{} 异常！\n".format(host))


def sftp_download_file(host, server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username="iaac", password="iaac@1234!")
        sftp = paramiko.SFTPClient.from_transport(t)
        # 下载文件
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    local_file_path = r"one.zip"
    server_file_path = r"/home/pi/one.zip"
    for host in get_hosts():
        # local_file_path = r"./log/{}log.txt".format(host)
        # sftp_download_file(host=host,server_path=server_file_path,local_path=local_file_path)
        sftp_upload_file(host=host, server_path=server_file_path,local_path=local_file_path)

