import base64
import os
from http import cookiejar

import js2py
import requests

from common.common import *
from common.log import logger

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
class Xunlei(object):

    username = ""
    password = ""
    def __init__(self,username,password):
        self.username=username
        self.password = password
        self.request = requests.session()
        self.request.cookies = cookiejar.LWPCookieJar(filename=os.path.join(os.path.abspath("."),"cookies",username))
        self.request.verify = False
        self.selected_peer_id = ""
        self.default_target_dir = ""
        self.id = ""
        self.verify_code = ''
        self.request.headers = {
        "Referer":"http://yuancheng.xunlei.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Upgrade-Insecure-Requests":"1",
        "Connection":"close",
        }
        if self.__loadCookies() and self.__hasLogin():
            logger.info("使用cookies正常登录")
        else:
            if  self.__login() == False or  self.__hasLogin() == False:
                raise Exception("账号密码无法正常登录")
        peer_id = self.__get_peer_id()
        self.selected_peer_id = peer_id #获取默认的设备id，这里预期就是1个设备
        self.default_target_dir = self.__get_peer_setting_default_path(peer_id) #获取默认下载文件夹，直接使用默认的文件夹用户存储下载任务
    @retry(3)
    def __login(self)->bool:
        """
        登录
        :param username:
        :param password:
        :return:
        """
        logger.info("尝试账号密码登录")
        server_domain =  'login.xunlei.com'
        url1 = 'https://{}/risk?cmd=algorithm&t={}'.format(server_domain,str(current_timestamp()))
        sign_fun = self.request.get(url1,verify=False).text
        xl_al = js2py.eval_js(sign_fun)
        SB = USER_AGENT + "###zh-cn###24###960x1440###-540###true###true###true###undefined###undefined###x86###Win32#########" + md5(
            str(current_timestamp()).encode())
        xl_fp_raw = base64.b64encode(SB.encode()).decode()
        xl_fp = md5(xl_fp_raw.encode())
        xl_fp_sign = xl_al(xl_fp_raw)
        device_data = {'xl_fp_raw': xl_fp_raw, 'xl_fp': xl_fp, 'xl_fp_sign': xl_fp_sign}
        device_url = 'https://{}/risk?cmd=report'.format(server_domain)
        time.sleep(1)
        self.request.post(device_url,data=device_data,verify=False)
        time.sleep(1)
        cookies = self.request.cookies._cookies

        login_page = self.request.post('https://{}/sec2login/?csrf_token={}'.format(server_domain,
            hashlib.md5(cookies['.xunlei.com']["/"]["deviceid"].value[:32].encode('utf-8')).hexdigest()),
                                  data={'u': self.username, 'p': self.password, 'verifycode': self.verify_code, 'login_enable': '0',
                                        'business_type': '113', 'v': '101', 'cachetime': current_timestamp()})
        login_cookies = login_page.cookies.get_dict()
        logger.info("登录后获取到cookies : {}".format(login_cookies))
        logger.info("整个request的cookies : {}".format(self.request.cookies._cookies))
        verify_type = self.get_cookie('.xunlei.com', "verify_type")
        if self.get_cookie(server_domain,"logindetail",path='/sec2login')=='412:passwd':
            logger.error("登录失败，账号密码错误")
        if self.get_cookie(server_domain,"logindetail",path='/sec2login')=='403:checkverify:nil':
            logger.error("登录失败，验证码输入错误")
        if verify_type =='MVA':
            logger.info("需要验证码登录")
            #暂时先不开启验证码登录功能
            # self.__get_verify_img()
            # self.verify_code = input("please input verifycode")
            return False
        if login_cookies.get("userid"):
            self.id = login_cookies.get("userid")
            self.request.cookies.save(ignore_discard=True)  # 保存cookies
            return True
        return False

    def __get_verify_img(self):
        url = 'http://verify1.xunlei.com/image?t=MVA&cachetime={}'.format(current_timestamp())
        r = self.request.get(url)
        with open('verify.png', 'wb') as file:  # 以byte形式将图片数据写入
            file.write(r.content)
            file.flush()
    def __loadCookies(self):
        try:
            self.request.cookies.load(ignore_discard=True)
            self.id = self.get_cookie('.xunlei.com', 'userid')
            return True
        except Exception as e:
            logger.info("加载不到cookies文件,错误信息：{} ".format(e))
            return False
    def get_cookie(self, domain, k,path = '/'):
        if self.has_cookie(domain, k,path):
            return self.request.cookies._cookies[domain][path][k].value
        else:
            return None
    def has_cookie(self, domain, k,path):
        return domain in self.request.cookies._cookies and k in self.request.cookies._cookies[domain][path]
    def __hasLogin(self):
        callback = self.gen_jsonp_function_name()
        url = 'http://hub.yuancheng.xunlei.com/check/vipcache?callback={}&_={}'.format(callback, current_timestamp())
        resp = self.request.get(url, headers={'User-Agent': USER_AGENT}).text
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            logger.info('response is not jsonp when double_check_login')
            return False

        if resp.get('userid') and resp.get('userid') == self.id and resp.get('rtn') != 101:
            logger.info("用户已经登录")
            return True
        return False
    @retry(3)
    def __get_peer_id(self):
        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.yuancheng.xunlei.com/listPeer?type=0&v=2&ct=0&callback={}&_={}'.format(callback,current_timestamp())
        r = self.request.get(url)
        r.encoding = 'utf-8'
        responseJson = get_response_info(r.text,callback)
        try:
            return responseJson['peerList'][0]['pid']
        except Exception as e :
            logger.info("获取设备ID时发生错误")
            raise e


    # 获取配置信息，主要是要拿到设备目录
    @retry(3)
    def __get_peer_setting_default_path(self, pid):

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.yuancheng.xunlei.com/settings?pid={}&v=2&ct=0&callback={}&_={}'.format(
            pid, callback, current_timestamp()
        )
        resp = self.request.get(url).text
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when get_peer_setting'
            raise Exception(msg)

        result = {}
        if resp.get('rtn') == 0:
            result = resp
        try:
            return result.get('defaultPath')
        except Exception as e:
            logger.info("获取默认路径时发生错误")
            raise e
    @retry(2)
    def __resolve_url(self, url):

        callback = self.gen_jsonp_function_name()
        payload = dict(url=url)
        payload = dict(json=json.dumps(payload))
        url = 'http://homecloud.yuancheng.xunlei.com/urlResolve?pid={}&v=2&ct=0&callback={}'.format(
            self.selected_peer_id, callback
        )
        resp = self.request.post(url, data=payload).text
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when resolve_url'
            raise Exception(msg)

        result = dict(url="", infohash="", size=0, name="")
        if resp.get('rtn') == 0 and "taskInfo" in resp:
            result['infohash'] = resp.get('infohash', '')
            result['url'] = resp.get('taskInfo').get('url')
            result['size'] = resp.get('taskInfo').get('size')
            result['name'] = resp.get('taskInfo').get('name')
        logger.info("解析种子完成")
        return result
    def getTaskingList(self):
        """
        获取下载中的任务列表
        :return:
        """
        return self.get_task_info(type=0)['tasks']
    def getTaskingCount(self):
        """
        获取下载中的任务数量
        :return:
        """
        return self.get_task_info(type=0)['dlNum']
    def get_task_info(self,type=0,pageNum=50):
        """
        获取任务信息，包括进行的任务列表，失败数量、成功数量、回收站数量、进行中任务数量
        :param type 查询类型  0：正在下载 1：已完成 2：垃圾箱 3：提交失败 默认0
        :param pageNum 每页显示多少条，默认50条
        :return: 任务dict 见代码result
        """
        callback = self.gen_jsonp_function_name()
        url = "http://homecloud.yuancheng.xunlei.com/list?pid={}&type={}&pos=0&number={}&needUrl=1&v=2&ct=0&callback={}&_={}".format(
            self.selected_peer_id,type,pageNum,callback,current_timestamp())
        resp  = self.request.get(url).text
        resp = get_response_info(resp,callback)
        result = dict(completeNum=0,dlNum=0,recycleNum=0,serverFailNum=0,sync=0,tasks=[])
        if resp.get('rtn') == 0 :
            result['completeNum'] = resp.get('completeNum') #完成任务数量
            result['dlNum'] = resp.get('dlNum') #下载中任务数量
            result['recycleNum'] = resp.get('recycleNum') #回收站任务数量
            result['serverFailNum'] = resp.get('serverFailNum')#提交失败数量
            result['sync'] = resp.get('sync')
            result['tasks'] = resp.get('tasks')#任务详情列表
        return result
    def getDoneTaskList(self):
        """
        获取完成的任务列表
        :return:
        """
        return self.get_task_info(type=1)['tasks']
    def getDoneTaskCount(self):
        """
        获取完成的任务数量
        :return:
        """
        return self.get_task_info(type=1)['completeNum']
    def getFailTaksCount(self):
        """
        获取失败的任务数量
        :return:
        """
        return self.get_task_info()['serverFailNum']
    def getFailTaksList(self):
        """
        获取失败的任务列表
        :return:
        """
        return self.get_task_info(type=3)['tasks']
    def __addTask(self,url_info:str):
        """
        增加任务
        :param url_info:解析后的url_info
        :return:
        """
        # resolve the url first
        size = url_info.get('size')
        if size == 0:
            raise Exception('Invalid URL provided')
        hash = url_info.get('infohash')
        name = url_info.get('name')
        url = url_info.get('url')

        # get the target dir
        target_path = self.default_target_dir
        # 默认就是默认路径，下面代码可用于后来选择默认下载目录
        # if path_index != None:
        #     if path_index >= len(self.user_define_target_dirs):
        #         raise Exception('path_index out of range')
        #     target_path = self.user_define_target_dirs[path_index]

        callback = "window.parent._POST_CALLBACK_2_"
        if hash:
            payload = dict(path=target_path, infohash=hash, name=name, btSub=[0])
            payload = dict(json=json.dumps(payload))
            url = 'http://homecloud.yuancheng.xunlei.com/createBtTask?pid={}&v=2&ct=0&callback={}'.format(
                self.selected_peer_id, callback
            )
            resp = self.request.post(url, data=payload).text
            try:
                resp = get_response_info(resp, callback)
            except AssertionError as e:
                msg = 'response is not jsonp when create_task'
                raise Exception(msg)

            if resp.get('rtn') == 202:
                raise Exception('正在下载或者已经下载')
            if resp.get('rtn') != 0:
                raise Exception(resp.get('msg'))
            logger.info("完成添加任务")
            return resp.get('rtn') == 0
        else:
            task = dict(url=url, name=name, gcid="", cid="", filesize=size, ext_json={"autoname": 1})
            payload = dict(path=target_path, tasks=[task])
            payload = dict(json=json.dumps(payload))
            url = 'http://homecloud.yuancheng.xunlei.com/createTask?pid={}&v=2&ct=0&callback={}'.format(
                self.selected_peer_id, callback
            )
            resp = self.request.post(url, data=payload).text
            try:
                resp = get_response_info(resp, callback)
            except AssertionError as e:
                msg = 'response is not jsonp when create_task'
                raise Exception(msg)

            if resp.get('tasks')[0].get('result') == 202:
                raise Exception('Already downloading/downloaded')
            logger.info("完成添加任务")
            return resp.get('rtn') == 0 and resp.get('tasks')[0].get('result') == 0
    def pushTask(self,url):
        """
        推送新任务
        :param url:
        :return:
        """
        url_info = self.__resolve_url(url) #先解析种子
        # 添加任务
        logger.info("添加成功" if self.__addTask(url_info) == True else "添加失败" )
        return True
    def gen_jsonp_function_name(self):
        return 'jQuery{}_{}'.format(id(self), current_timestamp())