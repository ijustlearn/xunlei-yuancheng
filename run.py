import requests
from http import cookiejar
import time
import base64
import js2py
import hashlib
import re
import json
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
def current_timestamp():
    return int(time.time()*1000)
def md5(s):
    return hashlib.md5(s).hexdigest().lower()
def gen_jsonp_function_name(obj):
        return 'jQuery{}_{}'.format(id(obj), current_timestamp())

def has_cookie(cookiejar, domain, k):
    return domain in cookiejar._cookies and k in cookiejar._cookies[domain]['/']
def get_cookie(cookiejar, domain, k):
    if has_cookie(cookiejar,domain, k):
        return cookiejar._cookies[domain]['/'][k].value
    else:
        return None
def remove_bom(response):
    if response.startswith('\xef\xbb\xbf'):
        response = response[3:]
    return response
def get_response_info(response, jsonp):
    response = remove_bom(response)
    m = re.search(r'%s\((.+)\)' % jsonp, response)
    assert m, 'invalid jsonp response: %s' % response
    # logger.debug('get_response_info:')
    # logger.debug(response)
    parameter = m.group(1)
    # m = re.match(r"^\{process:(-?\d+),msg:'(.*)'\}$", parameter)
    # if m:
    #     return {'process': int(m.group(1)), 'msg': m.group(2)}
    return json.loads(parameter)
def check_device_id(headers):
    # if not self.has_cookie('.xunlei.com', 'deviceid'):
    s = requests.session()
    s.cookies = cookiejar.LWPCookieJar(filename='cookies')
    try:
        # s.cookies.load(ignore_discard=True)
        # print(get_cookie(s.cookies,'.xunlei.com', 'userid'))
        #登录
        url1 = 'https://login.xunlei.com/risk?cmd=algorithm&t=' + str(current_timestamp())
        sign_fun = s.get(url1,verify=False,headers=headers).text
        print(sign_fun)
        xl_al = js2py.eval_js(sign_fun)
        SB = USER_AGENT + "###zh-cn###24###960x1440###-540###true###true###true###undefined###undefined###x86###Win32#########" + md5(
            str(current_timestamp()).encode())
        xl_fp_raw = base64.b64encode(SB.encode()).decode()
        xl_fp = md5(xl_fp_raw.encode())
        xl_fp_sign = xl_al(xl_fp_raw)
        device_data = {'xl_fp_raw': xl_fp_raw, 'xl_fp': xl_fp, 'xl_fp_sign': xl_fp_sign}
        device_url = 'https://login.xunlei.com/risk?cmd=report'
        time.sleep(2)
        response = s.post(device_url,headers=headers,data=device_data)
        print(response.text)
        print(response.cookies.get_dict())
        print(response.cookies['deviceid'][:32])
        time.sleep(2)
        login_page = s.post('https://login.xunlei.com/sec2login/?csrf_token={}'.format(
            hashlib.md5(response.cookies['deviceid'][:32].encode('utf-8')).hexdigest()), headers=headers,
                                  data={'u': '18501357462', 'p': 'as47154545', 'verifycode': '', 'login_enable': '0',
                                        'business_type': '113', 'v': '101', 'cachetime': current_timestamp()})

        print(login_page.cookies.get_dict())
        print(login_page.text)
        s.cookies.save()

        #进入主界面
        callback = gen_jsonp_function_name(s)
        # r = s.get("http://yuancheng.xunlei.com/")
        # r.encoding = 'utf-8'
        # print(r.text)

        url = 'http://homecloud.yuancheng.xunlei.com/listPeer?type=0&v=2&ct=0&callback={}&_={}'.format(callback,current_timestamp())
        r = s.get(url)
        r.encoding = 'utf-8'
        responseJson = get_response_info(r.text,callback)
        print(responseJson)
        selected_peer_id = responseJson['peerList'][0]['pid']
        url = 'http://homecloud.yuancheng.xunlei.com/urlResolve?pid={}&v=2&ct=0&callback=window.parent._POST_CALLBACK_2_'.format(
            selected_peer_id
        )
        data = {
            "json":'{"url":"magnet:?xt=urn:btih:TWRW462U6TVBPDHO75APH5Z2RS4HMY72"}'
        }
        r = s.post(url,data=data)
        print(r.text)
    except Exception as e:
        print('未找到cookies文件')
        raise  e


if __name__ == '__main__':

    # s = requests.Session()
    headers = {
        "Referer":"http://yuancheng.xunlei.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Upgrade-Insecure-Requests":"1",
        "Connection":"close",
    }
    check_device_id(headers)