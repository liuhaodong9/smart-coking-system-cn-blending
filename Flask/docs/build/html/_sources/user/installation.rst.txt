安装指南
========

本指南提供了设置和运行项目前端、后端和数据库的步骤，以及使用 TensorFlow 进行 GPU 加速所需的 CUDA 安装方法。

前端运行
--------

1. **Vue 环境**：
   项目不需要单独安装 Vue.js，`node_modules` 目录中已包含所有必要的依赖，依赖项已在 `package.json` 文件中列出。

2. **运行前端**：
   导航到项目的根目录smart-coking-system-newpc_2。打开终端并运行以下命令启动前端：

   .. code-block:: bash

      npm run serve

   .. image:: ../_images/前端运行结果1.png
            :alt: 前端运行结果1
   .. image:: ../_images/前端运行结果2.png
            :alt: 前端运行结果2
--------

后端运行
--------
1. **创建虚拟环境**：
   推荐使用 Anaconda 创建 Python 3.8 虚拟环境，并安装所需的依赖项。运行以下命令：

   .. code-block:: bash

      conda create -n coke python=3.8
      conda activate coke
      pip install cudatoolkit=11.2
      pip install tensorflow-gpu==2.10
      conda install cudnn=8.1 -c conda-forge

   **注意**：如果您没有 GPU，可以完全忽略 `tensorflow-gpu` 的安装。

2. **安装依赖项**：
   进入虚拟环境后，运行以下命令安装 Flask 和其他必要依赖：

   .. code-block:: bash
      
      pip install Flask==2.2.2 Flask-Cors==3.0.10 Flask-SQLAlchemy==3.0.2 geatpy==2.7.0 numpy==1.23.4 pandas==1.5.1 PyMySQL==1.0.2 scikit-learn==0.24.2 SQLAlchemy==1.4.44 Werkzeug==2.2.2 memory-profiler==0.61.0

3. **启动后端**：
   通过运行 `login.py` 启动后端，5000端口表示成功启动 Flask 应用：
   
   .. code-block:: bash

      python login.py

   .. image:: ../_images/后端运行结果.png
            :alt: 后端运行结果
--------  

数据库安装
--------
1. **安装 MySQL 数据库**：
   下载并安装 MySQL。有关配置的指南，请参考以下教程：https://www.jb51.net/database/324331zkx.htm。确保将 MySQL 添加到系统环境变量中。

2. **安装 Navicat Premium Lite**：
   Navicat Premium Lite 是一个免费的 MySQL 可视化工具。可从以下链接下载：https://www.navicat.com.cn/download/navicat-premium-lite。

3. **创建数据库**：
   - 在 Navicat 中，新建一个 MySQL 连接，填写用户名和密码。
   - 创建一个新数据库，例如 `CoalData_table.csv`。
   - 导入提供的示例 CSV 数据，选择 "csv" 格式。
   - 在导入过程中，选择 **高级选项** 并勾选 **使用 NULL 替换空字符串**。

   .. image:: ../_images/数据库设置1.png
      :alt: 数据库设置1
   .. image:: ../_images/数据库设置2.png
      :alt: 数据库设置2
   .. image:: ../_images/数据库设置3.png
      :alt: 数据库设置3
   .. image:: ../_images/数据库设置4.png
      :alt: 数据库设置4
   .. image:: ../_images/数据库设置5.png
      :alt: 数据库设置5
   .. image:: ../_images/数据库设置6.png
      :alt: 数据库设置6
   .. image:: ../_images/数据库设置7.png
      :alt: 数据库设置7

4. **更新 Flask 中的 MySQL的连接信息**：
   为了确保 Flask 应用程序能够成功连接到 MySQL 数据库，需要在 coalData.py 文件中更新 MySQL 的连接信息。定位代码段：

   .. code-block:: python
      
      # url格式 mysql://<用户名>:<密码>@127.0.0.1:3306/coaldata?charset=utf8
      app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/coaldata?charset=utf8'
      
      # 开启 SQLAlchemy 的事件监听功能
      app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


SSH远程服务器运行网站(可选)
--------
   开发环境：运行后端python算法命令：
   通过ssh运行服务器上的前端：
   
   .. code-block:: bash   

      ssh -L5000:localhost:5000 liuhaodong@211.68.155.21
      conda activate coke
      cd smart-coking/smart-coking-system-newpc_2/Flask
      python login.py
   
   再新建一个命令窗口运行前端网页：

   .. code-block:: bash
      
      ssh -L 8080:localhost:8080 liuhaodong@211.68.155.21
      cd smart-coking/smart-coking-system-newpc_2/Flask
      npm run serve
   
   用 http://localhost:8080 在本地访问服务器

   生产环境：
   Nginx + 打包后静态文件

   .. code-block:: bash

      npm run build
      sudo systemctl reload nginx

   后端使用 Gunicorn常驻后台

   .. code-block:: bash

      pkill -f gunicorn
      gunicorn -w 4 -b 0.0.0.0:5000 login:app

--------
