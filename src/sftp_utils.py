import os.path
import time

import paramiko
from datetime import datetime


def list_remote_directory_as_dict(host, port, username, password, remote_directory):
    """
    Connects to an SFTP server, lists the contents of a remote directory,
    and returns a dictionary with file names as keys and dictionaries containing
    file size and modification time as values. Then, it closes the connection.

    :param host: The hostname or IP address of the SFTP server.
    :param port: The port number to connect on (default is 22).
    :param username: The username for authentication.
    :param password: The password for authentication.
    :param remote_directory: The path of the remote directory to list.
    :return: A dictionary with file metadata.
    """
    file_info_dict = {}

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SFTP server
        ssh.connect(hostname=host, port=port, username=username, password=password)

        # Initialize SFTP session
        sftp_client = ssh.open_sftp()

        try:
            # List files in the remote directory with attributes
            remote_files_attrs = sftp_client.listdir_attr(remote_directory)

            for attr in remote_files_attrs:
                # Convert timestamp to human-readable format
                mod_time = datetime.fromtimestamp(attr.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                # Store the file info in the dictionary
                file_info_dict[attr.filename] = {
                    'size': attr.st_size,
                    'last_modified': mod_time
                }

        finally:
            # Close the SFTP session
            sftp_client.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None in case of an error
    finally:
        # Ensure the SSH connection is closed
        ssh.close()

    return file_info_dict


def download_file_from_sftp(host, port, username, password, remote_directory, remote_filename, local_path):
    """
    Connects to an SFTP server, lists the contents of a remote directory,
    downloads a specified file, and returns a dictionary with file metadata.
    Then, it closes the connection.

    :param host: The hostname or IP address of the SFTP server.
    :param port: The port number to connect on (default is 22).
    :param username: The username for authentication.
    :param password: The password for authentication.
    :param remote_directory: The path of the remote directory.
    :param remote_filename: The name of the remote file to download.
    :param local_path: The local path where the file will be saved.
    :return: A dictionary with file metadata or None in case of an error.
    """
    file_info_dict = list_remote_directory_as_dict(host, port, username, password, remote_directory)

    if file_info_dict and remote_filename in file_info_dict:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the SFTP server
            ssh.connect(hostname=host, port=port, username=username, password=password)

            # Initialize SFTP session
            sftp_client = ssh.open_sftp()

            try:
                # Construct full remote path
                remote_file_path = f"{remote_directory}/{remote_filename}"

                # Download the file
                local_file_path = f"{local_path}/{remote_filename}"
                sftp_client.get(remote_file_path, local_file_path)
                print(f"File '{remote_filename}' downloaded to '{local_file_path}'.")

            finally:
                # Close the SFTP session
                sftp_client.close()

        except Exception as e:
            print(f"An error occurred during download: {e}")
            return None

        finally:
            # Ensure the SSH connection is closed
            ssh.close()

    else:
        print(f"File '{remote_filename}' not found in the remote directory.")
        return None


if __name__ == '__main__':
    from file_operations import rename_file
    from ntp_util import timestamp_to_date
    import schedule


    # SFTP服务器配置信息
    def job():
        host = '139.159.218.144'
        port = 22  # SFTP默认端口
        username = 'root'
        password = 'ZOWELL@123456'  # 或者使用密钥对认证
        remote_directory = '/root/EasyDebug/bin/'  # 你想查看的远程目录
        remote_files = list_remote_directory_as_dict(host, port, username, password, remote_directory)
        filtered_dict = {key: value for key, value in remote_files.items() if
                         '.txt.bz2' in key or 'DID_Dump.log' == key}
        print(filtered_dict)

        # Example usage:
        for remote_filename in filtered_dict.keys():
            local_path = r'C:\Users\Administrator\Desktop\data\sftp\139.159.200.147' + '/'
            if not os.path.exists(local_path + remote_filename):
                download_file_from_sftp(host, port, username, password, remote_directory, remote_filename, local_path)
        DID_Dump = r'C:\Users\Administrator\Desktop\data\sftp\139.159.218.144\DID_Dump.log'
        if os.path.exists(DID_Dump):
            time_str = timestamp_to_date(format="%Y-%m-%d %H-%M-%S")
            rename_file(DID_Dump, DID_Dump + time_str)


    # 使用cron风格的时间设置，每30分钟执行一次，* 表示任意值，因此"*/30"表示每30分钟
    job()
    schedule.every(1).minutes.do(job)

    print("Task scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)
