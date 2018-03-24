# xunlei-yuancheng
  **该程序基于python3.4开发，理论支持3.4以及以上版本,主要使用了 requests、cookiejar 第一次登陆使用账号密码，下次登陆使用cookie**
## 功能介绍
  用于[迅雷远程](http://yuancheng.xunlei.com/)账号自动登录,自动添加下载任务,自动查询下载任务进度列表
## 截图
  ![](https://github.com/ijustlearn/xunlei-yuancheng/blob/master/image1.png) ![](https://github.com/ijustlearn/xunlei-yuancheng/blob/master/image3.png)
## windows安装使用
1. 下载zip包
2. 解压后 cd xunlei-yuancheng
3. 安装虚拟环境 virtualenv -p python3 --no-sit-packages venv
4. 安装依赖 venv\Scripts\activate.bat 然后  pip3 install -r requirements.txt 
5. 运行 python run.py -u 迅雷用户名 -p 密码 -c 命令参数
## 命令详解
  python run.py -h 用户名必填 -p 密码必填 -c 命令操作可选，如果没有则进入交互模式，交互模式可以多次输入-c命令的参数
### -c 参数：
1. doneTaskList 获取已完成的任务列表，返回json对象，具体含义需要自行理解（主要包括已下载数量，下载中数量，回收站数量，tasks列表）
2. pushTask 推送url下载任务，执行后需要输入需要添加的url地址
3. taskingList 获取下载中任务列表，返回json对象，具体含义需要自行理解（主要包括已下载数量，下载中数量，回收站数量，tasks列表）
