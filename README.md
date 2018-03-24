# xunlei-yuancheng
  **该程序基于python3.4开发，理论支持3.4以及以上版本,主要使用了 requests、cookiejar 第一次登陆使用账号密码，下次登陆使用cookie**
  **该分支是迅雷远程登录功能使用flask resultFull api 封装的版本，安装后可以直接使用http rest方式管理远程迅雷下载任务**
## 功能介绍
  用于[迅雷远程](http://yuancheng.xunlei.com/)账号自动登录,自动添加下载任务,自动查询下载任务进度列表
## 截图
  ![](https://github.com/ijustlearn/xunlei-yuancheng/blob/master/image1.png)
## centos安装使用
1. 下载zip包 wget 
2. 解压后 unzip  cd 
3. 安装虚拟环境 virtualenv -p python3 --no-sit-packages venv
4. 安装依赖 source venv/bin/activate 然后  pip3 install -r requirements.txt 
5. 运行 python app.py
6. 测试运行 curl 127.0.0.1:5000 会有404返回（默认只是监听本机的5000端口）
## rest API
1. 获取任务列表：
- url:http://127.0.0.1:5000/xunlei
- method: GET
- 参数: u 用户名
        p 密码 
        type 类型 0：正在下载 1:已下载 2:回收箱 3:提交失败
2. 推送任务:
- url:http://127.0.0.1:5000/xunlei
- method: POST
- 参数: u 用户名
        p 密码 
        url 种子或者链接地址
