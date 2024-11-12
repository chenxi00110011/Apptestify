from ssh_client import SSHClient


def reset():
    # 配置SSH连接参数
    hostname = '192.168.1.101'
    port = 22
    username = 'chenxi'
    password = 'cx123456'

    # 创建SSH客户端实例
    ssh_client = SSHClient(hostname, port, username, password)

    try:
        # 建立连接
        ssh_client.connect()

        # 执行命令
        command = 'python3 /home/chenxi/reset_02.py'
        output, error = ssh_client.execute_command(command)
        print(f"Command Output:\n{output}")

        # 执行另一个命令
        command = 'pwd'
        output, error = ssh_client.execute_command(command)
        print(f"Command Output:\n{output}")

    finally:
        # 关闭连接
        ssh_client.close()


if __name__ == '__main__':
    reset()