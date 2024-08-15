from smb.SMBConnection import SMBConnection
import os


def download_smb_file(server_ip, share_name, file_path, local_path, username, password):
    conn = SMBConnection(username, password, "", server_ip, use_ntlm_v2=True)
    assert conn.connect(server_ip, 445)

    files = conn.listPath(share_name, os.path.dirname(file_path))
    for f in files:
        print(f.filename, os.path.basename(file_path))
        if f.filename == os.path.basename(file_path):
            with open(local_path, "wb") as local_file:
                conn.retrieveFile(share_name, file_path, local_file)
            break

    conn.close()


if __name__ == '__main__':
    # 使用示例
    server_ip = '192.168.250.10'
    share_name = 'TestFolder'
    file_path = r'APP\P6SLite\Android\p6slite_v5.9.0\20240730\P6SLite_V5.9.0_240730.apk'  # 在共享目录中的文件路径
    local_path = '../data/test.apk'  # 本地保存路径
    username = 'xi.chen'
    password = '123456'

    download_smb_file(server_ip, share_name, file_path, local_path, username, password)
