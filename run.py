from log import logger

from xunlei import Xunlei
import sys
import getopt
import json
def usage():
    print("""
    -u : 用户名 必填
    -p : 密码 必填
    -c : 操作  taskInfo 获取任务信息
    """)
def action(cmd,xunlei):
    if cmd == 'doneTaskList':  # 获取完成任务列表
        return json.dumps(xunlei.getDoneTaskList())
    elif cmd == 'pushTask':
        raw = input("push url > ")  # 推送任务
        return json.dumps(xunlei.pushTask(raw))
    elif cmd == 'taskInfo':  # 获取任务信息
        return json.dumps(xunlei.get_task_info())
    elif cmd == 'taskingList':  # 获取下载中任务列表
        return json.dumps(xunlei.getTaskingList())
    elif cmd == 'exit':
        return sys.exit()
    else:
        return """
        unknown commond ,please input the fllowing cmd:
        doneTaskList
        pushTask
        taskInfo
        taskingList
        exit
        """
if __name__ == '__main__':
    if len(sys.argv) ==1:
        usage()
        sys.exit()
    username = None
    password = None
    cmdStr = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:p:c:", ["help"])
        for cmd, arg in opts:  # 使用一个循环，每次从opts中取出一个两元组，赋给两个变量。cmd保存选项参数，arg为附加参数。接着对取出的选项参数进行处理。
            if cmd in ("-u", "--username"):
                username = arg
            elif cmd in ("-p", "--password"):
                password = arg
            elif cmd in ("-c", "--cmd"):
                cmdStr  = arg
        if not username or not password:
            print("user and pass is required")
            sys.exit()
        xunlei = Xunlei(username, password)
        if cmdStr is not None  and username and password:
            print(action(cmdStr,xunlei))
            sys.exit()
        while True:
            raw = input("xunlei > ")
            print(action(raw, xunlei))
    except getopt.GetoptError:
        print("argv error,please input")
    except Exception as e :
        logger.exception(e)