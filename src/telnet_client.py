# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
# telnet_client.py
import telnetlib
import time
from my_decorator import exception_handler, printer


@printer
@exception_handler
def telnet_connect(host, username, password, command):
    tn = telnetlib.Telnet(host, 23)
    tn.read_until(b"login: ")
    tn.write(username.encode("ascii") + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")
    if type(command) == type('str'):
        tn.write(command.encode("ascii") + b"\n")
    elif type(command) == type([]):
        for com in command:
            tn.write(com.encode("ascii") + b"\n")
            time.sleep(1)
    time.sleep(1)
    output = tn.read_very_eager()
    res = output.decode("utf-8")
    tn.close()
    return res


if __name__ == "__main__":
    host = "192.168.20.39"
    username = "root"
    password = "zviewa5s"
    command = "uptime"
    telnet_connect(host, username, password, command)

