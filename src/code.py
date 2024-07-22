import random
import string

def generate_complex_password(length=16):
    """生成一个指定长度的复杂密码，包含大小写字母和特殊字符"""
    if length < 16:
        print("警告: 密码长度至少为16位以确保安全性，但将按请求长度生成。")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# 生成一个16位的复杂密码
password = generate_complex_password(16)
print("生成的密码:", password)