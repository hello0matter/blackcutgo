# 导入webdriver
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# 初始化参数
desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '12',  # 手机安卓版本
    'deviceName': 'RMX2202',  # 设备名，adb devices获取
    'appPackage': 'com.taobao.taobao',  # 启动APP Package名称com.qdmetro.xahl.ar.eye  com.hyh.suianyun.app
    'appActivity': 'com.taobao.search.searchdoor.SearchDoorActivity',  #aapt dump badging  xx.apk
    'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App，如果为False的话，执行完脚本后，app的数据会清空 ，比如你原本登录了，执行完脚本后就退出登录了
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2'
}
# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 设置等待时间，如果不给时间的话可能会找不到元素
driver.implicitly_wait(3)
# 点击搜索框
driver.find_element(AppiumBy.ID,'com.taobao.taobao:id/searchEdit').click()
driver.find_element(AppiumBy.ID,'com.taobao.taobao:id/searchEdit').send_keys("小星")
driver.find_element(AppiumBy.ID,'com.taobao.taobao:id/searchbtn').click()

# 退出程序，记得之前没敲这段报了一个错误 Error: socket hang up 啥啥啥的忘记了，有兴趣可以try one try
# driver.quit()

