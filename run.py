import requests
from http import cookiejar
import time
import base64
import js2py
import hashlib

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
def current_timestamp():
    return int(time.time()*1000)
def md5(s):
    return hashlib.md5(s).hexdigest().lower()


def has_cookie(cookiejar, domain, k):
    return domain in cookiejar._cookies and k in cookiejar._cookies[domain]['/']
def get_cookie(cookiejar, domain, k):
    if has_cookie(cookiejar,domain, k):
        return cookiejar._cookies[domain]['/'][k].value
    else:
        return None
def check_device_id(headers):
    # if not self.has_cookie('.xunlei.com', 'deviceid'):
    s = requests.session()
    s.cookies = cookiejar.LWPCookieJar(filename='cookies')
    try:
        s.cookies.load(ignore_discard=True)
        print(get_cookie(s.cookies,'.xunlei.com', 'userid'))
    except:
        print('未找到cookies文件')
        print(s.cookies.get_dict())
        # url1 = 'https://login.xunlei.com/risk?cmd=algorithm&t=' + str(current_timestamp())
        # sign_fun = s.get(url1,verify=False,headers=headers).text
        # print(sign_fun)
        # xl_al = js2py.eval_js(sign_fun)
        # SB = USER_AGENT + "###zh-cn###24###960x1440###-540###true###true###true###undefined###undefined###x86###Win32#########" + md5(
        #     str(current_timestamp()).encode())
        # xl_fp_raw = base64.b64encode(SB.encode()).decode()
        # xl_fp = md5(xl_fp_raw.encode())
        # xl_fp_sign = xl_al(xl_fp_raw)
        # device_data = {'xl_fp_raw': xl_fp_raw, 'xl_fp': xl_fp, 'xl_fp_sign': xl_fp_sign}
        # device_url = 'http://login.xunlei.com/risk?cmd=report'
        # time.sleep(2)
        # response = s.post(device_url,headers=headers,data=device_data)
        # print(response.text)
        # print(response.cookies.get_dict())
        # print(response.cookies['deviceid'][:32])
        # time.sleep(2)
        # login_page = s.post('https://login.xunlei.com/sec2login/?csrf_token={}'.format(
        #     hashlib.md5(response.cookies['deviceid'][:32].encode('utf-8')).hexdigest()), headers=headers,
        #                           data={'u': '18501357462', 'p': 'as47154545', 'verifycode': '', 'login_enable': '0',
        #                                 'business_type': '113', 'v': '101', 'cachetime': current_timestamp()})
        #
        # print(login_page.cookies.get_dict())
        # print(login_page.text)
        # s.cookies.save()
if __name__ == '__main__':

    # s = requests.Session()
    headers = {
        "Referer":"http://yuancheng.xunlei.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Upgrade-Insecure-Requests":"1",
        "Connection":"close",
    }
    check_device_id(headers)
    # s.cookies = cookiejar.LWPCookieJar(filename='cookies')
    # r = requests.get('http://yuancheng.xunlei.com/login.html',headers=headers)
    # print(r.ok)
    # print(r.text)
    # print(r.cookies.get_dict())