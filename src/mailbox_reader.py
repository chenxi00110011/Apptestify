import configparser
import poplib
import email
from email.header import decode_header
import re

# 创建ConfigParser对象
config = configparser.ConfigParser()
debug_mode = False
# 读取INI文件
try:
    config.read(r'C:\Users\Administrator\P2pServerTest\Apptestify/data/config.ini')
except configparser.Error as e:
    print(f"配置文件读取错误: {e}")
    exit(1)

# 获取配置项
try:
    email_account = config.get('Email', 'account')
    email_password = config.get('Email', 'password')
    pop_server = config.get('Email', 'pop_server')

except (configparser.NoSectionError, configparser.NoOptionError) as e:
    print(f"配置项读取错误: {e}")
    exit(1)

# 打印配置项
# print(f"Email Account: {email_account}")
# print(f"Email Password: {email_password}")
# print(f"POP Server: {pop_server}")


def connect_to_pop_server():
    """连接到POP3服务器"""
    try:
        mail = poplib.POP3_SSL(pop_server)  # 使用SSL
        if debug_mode:
            mail.set_debuglevel(1)  # 启用调试模式
        mail.user(email_account)
        mail.pass_(email_password)
        return mail
    except poplib.error_proto as e:
        print(f"POP3连接错误: {e}")
        return None


def fetch_emails(mail):
    """获取所有邮件"""
    try:
        num_messages = len(mail.list()[1])
        emails = []
        for i in range(num_messages):
            raw_email = b'\n'.join(mail.retr(i + 1)[1])
            email_message = email.message_from_bytes(raw_email)
            emails.append(email_message)
        return emails
    except poplib.error_proto as e:
        print(f"邮件获取错误: {e}")
        return []


def parse_email(email_message):
    """解析邮件内容"""
    subject, encoding = decode_header(email_message['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')

    from_ = email.utils.parseaddr(email_message['From'])[1]

    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        body = email_message.get_payload(decode=True).decode()

    return {
        'subject': subject,
        'from': from_,
        'body': body
    }


def main():
    # 连接到POP3服务器
    mail = connect_to_pop_server()

    if mail is None:
        exit(1)

    # 获取并解析每封邮件
    emails = fetch_emails(mail)
    for email_message in emails:
        parsed_email = parse_email(email_message)
        print(f"主题: {parsed_email['subject']}")
        print(f"发件人: {parsed_email['from']}")
        # print(f"内容: {parsed_email['body']}...")  # 显示前50个字符
        print("-" * 50)

    # 关闭连接
    mail.quit()


def get_verification_code():
    # 连接到POP3服务器
    mail = connect_to_pop_server()

    # 验证码列表
    verification_codes = []

    if mail is None:
        exit(1)

    # 获取并解析每封邮件
    emails = fetch_emails(mail)
    for email_message in emails:
        parsed_email = parse_email(email_message)
        if parsed_email['subject'] == "邮件验证码" and parsed_email['from'] == "service-noreply@mailq.zwcloud.wang":
            # print(parsed_email['body'], type(parsed_email['body']))
            # 使用正则表达式匹配6位数字验证码
            pattern = r'\d{6}'
            match = re.search(pattern, parsed_email['body'])

            if match:
                verification_code = match.group()
                verification_codes.append(verification_code)
                # print(f"提取到的验证码是: {verification_code}")
    return verification_codes[-1]


if __name__ == "__main__":
    print(get_verification_code())
    print(type(get_verification_code()))
