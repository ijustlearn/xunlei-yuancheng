import requests

class Xunlei(object):
    request = ""
    def __init__(self):
        self.request = requests.get()
        pass
    def __login(self,username: str,password: str)->bool:
        """
        登录
        :param username:
        :param password:
        :return:
        """
        pass
    def getTaskingList(self):
        """
        获取下载中的任务列表
        :return:
        """
        pass
    def getTaskingCount(self):
        """
        获取下载中的任务数量
        :return:
        """
        pass
    def getDoneTaskList(self):
        """
        获取完成的任务列表
        :return:
        """
        pass
    def getDoneTaskCount(self):
        """
        获取完成的任务数量
        :return:
        """
        pass
    def pushTask(self,url:str):
        """
        推送新任务
        :param url:
        :return:
        """
        pass