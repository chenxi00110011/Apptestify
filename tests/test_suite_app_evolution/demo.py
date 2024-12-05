import time
import uiautomator2_extended

app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
time.sleep(15)
app.run_parameters['rectangle'] = 1.0
app.go_to_page('首页')
app.go_to_page('设备信息', "370148")
app.title["checked"] = True
app.go_to_page('OSD设置', "春眠不觉晓,ABCabc123", "显示通道名")

assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_name_text")
assert app.driver(resourceId="com.zwcode.p6slite:id/osd_name_text").get_text() == "春眠不觉晓,ABCabc123"
