from ssh_client import SSHClient


def reset(did):
    dev_gpio = {
        'IOTFAA-000086-MRNRJ': "reset_02.py",
        'BOTDBB-007004-YHUHG': "reset_13.py",
        'IOTFAA-705280-EDGCR': "reset_04.py"
    }
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
        command = f'python3 /home/chenxi/{dev_gpio[did]}'
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
    reset("IOTFAA-000086-MRNRJ")