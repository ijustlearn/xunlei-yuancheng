import hashlib
import json
import re
import time
import random
def current_timestamp():
    return int(time.time()*1000)
def md5(s):
    return hashlib.md5(s).hexdigest().lower()

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
def retry(num=2):
    def decorator(func):
        def wrapper(*args,**kwargs):
            for i in range(num):
                try:
                    ret = func(*args,**kwargs)
                    if ret == False :
                        time.sleep(round(random.uniform(0, 2), 2))  # 随机睡眠一段时间
                        print("执行函数结果为false正在重试")
                        continue
                    return ret
                except Exception as e :
                    if i == num-1:
                        raise e
                    print("执行函数遇到一些问题正在重试")
                    time.sleep(round(random.uniform(0, 2), 2))
        return wrapper
    return decorator