import paramiko


class SSHClient:
    def __init__(self, hostname, port=22, username='pi', password='raspberry'):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        """建立SSH连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, self.port, self.username, self.password)
        print(f"Connected to {self.hostname}")

    def execute_command(self, command):
        """执行SSH命令并返回结果"""
        if self.client is None:
            raise Exception("SSH connection is not established. Call connect() first.")

        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if error:
            print(f"Error executing command: {error}")
        return output, error

    def close(self):
        """关闭SSH连接"""
        if self.client:
            self.client.close()
            print(f"Connection to {self.hostname} closed.")
            self.client = None


# 示例使用
if __name__ == "__main__":
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
