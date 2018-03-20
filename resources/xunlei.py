from flask_restful import Resource,reqparse
from services.xunlei import Xunlei
from common.log import logger
parser = reqparse.RequestParser()
parser.add_argument('u', type=str, required=True, help='用户名字符串，必填')
parser.add_argument('p', type=str, required=True,help='密码字符串，必填')
parser.add_argument('type', type=int)
parser.add_argument('url', type=str)

class XunleiApi(Resource):
    def get(self):
        args = parser.parse_args()
        username = args['u']
        password = args['p']
        type = args['type']
        if  type == None :
            return {"result":500,"message":"类型必须传入，0:正在下载、1:已完成、2:垃圾箱、3:提交失败"}
        try:
            xunlei_serveice = Xunlei(username,password)
            return {"result":200,"obj":xunlei_serveice.get_task_info(type=type),"message":"查询成功"}
        except Exception as e:
            logger.exception("查询任务时发生错误")
            logger.exception(e)
            return {"result":500,"message":e.__str__()}
    def post(self):
        args = parser.parse_args()
        username = args['u']
        password = args['p']
        url = args['url']
        if not url :
            return  {"result":500,"message":"url必须传入"}
        try:
            xunlei_serveice = Xunlei(username, password)
            if xunlei_serveice.pushTask(url):
                return {"result":200,"message":"添加完成"}
        except Exception as e:
            logger.exception("添加任务时发生错误")
            logger.exception(e)
            return {"result":500,"message":e.__str__()}
