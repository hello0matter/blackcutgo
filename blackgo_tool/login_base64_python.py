import requests
from functools import partial
import subprocess
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
#https://curlconverter.com/去看
cookies = {
    'uid': 'CgoKS2N5iGwjKBOXQ1XqAg==',
    'to8to_landtime': '1668909166',
    'tracker2019jssdkcross': '%7B%22distinct_id%22%3A%2218492bcf022a09-08221bab4ac68-7d5d5475-1382400-18492bcf023b24%22%7D',
    'to8tocookieid': '18492bcf022a09-08221bab4ac68-7d5d5475-1382400-18492bcf023b24',
    'to8to_tcode': 'sz',
    'to8to_tname': '%E6%B7%B1%E5%9C%B3',
    'to8to_townid': '1130',
    'city_from_ip': 'å¹¿å·ž',
    'to8to_sourcepage': '',
    'to8to_nowpage': 'https%253A%252F%252Fsz.to8to.com%252F',
    'to8to_cook': 'OkOcClPzRWV8ZFJlCIF4Ag==',
    'tender_popup_flag': 'true',
    'visitPage': 'true',
    'agreementRead': 'true',
    'to8to_tbdl_userinfo': '20326634',
    'sourcepath': 'b4',
    'to8to_landpage': 'https%3A//www.to8to.com/new_login.php',
    'tracker2019session': '%7B%22session%22%3A%2218493f2f1a0120c-043e30274b33a6-7d5d5475-1382400-18493f2f1a115c4%22%7D',
    'PHPSESSID': 'lplrsf6tvhsd8rfdlfe58rbb6a',
    'Hm_lvt_dbdd94468cf0ef471455c47f380f58d2': '1668909167,1668929493',
    'to8tosessionid': 's_039df7a567a4b308a5c69b813664edb1',
    'to8to_oo_login_20326634': '84bc5a66a632894119e9ed55fb2d4120',
    'page-num': '2',
    'Hm_lpvt_dbdd94468cf0ef471455c47f380f58d2': '1668940975',
    'act': 'freshen',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'uid=CgoKS2N5iGwjKBOXQ1XqAg==; to8to_landtime=1668909166; tracker2019jssdkcross=%7B%22distinct_id%22%3A%2218492bcf022a09-08221bab4ac68-7d5d5475-1382400-18492bcf023b24%22%7D; to8tocookieid=18492bcf022a09-08221bab4ac68-7d5d5475-1382400-18492bcf023b24; to8to_tcode=sz; to8to_tname=%E6%B7%B1%E5%9C%B3; to8to_townid=1130; city_from_ip=å¹¿å·ž; to8to_sourcepage=; to8to_nowpage=https%253A%252F%252Fsz.to8to.com%252F; to8to_cook=OkOcClPzRWV8ZFJlCIF4Ag==; tender_popup_flag=true; visitPage=true; agreementRead=true; to8to_tbdl_userinfo=20326634; sourcepath=b4; to8to_landpage=https%3A//www.to8to.com/new_login.php; tracker2019session=%7B%22session%22%3A%2218493f2f1a0120c-043e30274b33a6-7d5d5475-1382400-18493f2f1a115c4%22%7D; PHPSESSID=lplrsf6tvhsd8rfdlfe58rbb6a; Hm_lvt_dbdd94468cf0ef471455c47f380f58d2=1668909167,1668929493; to8tosessionid=s_039df7a567a4b308a5c69b813664edb1; to8to_oo_login_20326634=84bc5a66a632894119e9ed55fb2d4120; page-num=2; Hm_lpvt_dbdd94468cf0ef471455c47f380f58d2=1668940975; act=freshen',
    'Origin': 'https://www.to8to.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.to8to.com/new_login.php',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

node = execjs.get()
js_code = open('login_base64_js.js',encoding='utf-8').read()
ctx = node.compile(js_code)
# ctx.eval()
data = {
    'referer': 'https://www.to8to.com/reg/reg_new.php',
    'msgCode': '',
    'val': ctx.call('rsaString', {'a':'17680492987'}),
    'password':  ctx.call('rsaString', {'a':'Gcsdfaksh1'})
}

response = requests.post('https://www.to8to.com/new_login.php', cookies=cookies, headers=headers, data=data)