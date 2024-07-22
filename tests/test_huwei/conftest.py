# 模块名称：conftest
# 模块内容：fixture函数集合
# 作者: 陈 熙
# -*- coding: utf-8 -*-
import pytest
import os
import time
from uiautomator2_manager import uiautomator2_extended

@pytest.fixture(scope="function")
def setup_ruiboshi():
    """初始化测试环境"""
    # 在这里进行测试环境的初始化操作
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('AEUN9X1721G07755', 'com.zwcode.p6slite')
    return app

