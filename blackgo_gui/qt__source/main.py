# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import hashlib
import requests
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def main__login(usercode, password, city):
    print(usercode, password, city)
    md5s = hashlib.md5()
    md5s.update(password.encode('utf8'))
    hexdigest = md5s.hexdigest()
    url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/login?usercode=' + usercode + '&password=' + hexdigest + '&city=' + city
    headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664087759|1664087489'}
    data = {}

    html = requests.get(url, headers=headers, verify=False, cookies=cookies)
    return html.text

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    # 获取 root 对象.
    window = engine.rootObjects()[0]
    window.main__login.connect(main__login)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
