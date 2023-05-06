#coding:utf-8
from flask import Flask
import requests

app = Flask(__name__)
#中间验证码函数
@app.route("/")
def get_captcha():
  burp0_url = "https://art.fair-meta.com/captcha?r=0.5636469070816139"
  burp0_headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"", "Accept": "application/json, text/plain, */*", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
  requ = requests.get(burp0_url, headers=burp0_headers)
  return requ.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)