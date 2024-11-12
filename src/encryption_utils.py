from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


def generate_key_and_iv():
    # 生成一个随机的256位密钥和一个随机的128位IV
    key = os.urandom(32)  # AES-256需要32字节的密钥
    iv = os.urandom(16)  # IV长度通常是块大小，AES的块大小是128位/16字节
    return key, iv


def encrypt_data(key, iv, data):
    # 创建一个加密器对象
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 使用PKCS7填充
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # 加密数据
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data


def decrypt_data(key, iv, encrypted_data):
    # 创建一个解密器对象
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密数据
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # 移除PKCS7填充
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


if __name__ == '__main__':
    # 示例
    key, iv = generate_key_and_iv()
    print(key, iv)
    data = b"Hello, this is a secret message!"

    # 加密
    encrypted = encrypt_data(key, iv, data)
    # print(f"Encrypted: {encrypted}")

    # 解密
    decrypted = decrypt_data(key, iv, encrypted)
    # print(f"Decrypted: {decrypted.decode('utf-8')}")
