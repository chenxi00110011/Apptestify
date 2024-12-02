import time

import uiautomator2_extended

app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
time.sleep(15)
app.run_parameters['rectangle'] = 1.0
app.go_to_page('首页')
app.go_to_page('设备设置', '000086')