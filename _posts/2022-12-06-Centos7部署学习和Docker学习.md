---
layout:     post
title:      Centos7部署学习和Docker学习
subtitle:   Docker安装与一些操作纪要
date:       2022-12-06
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Neural Design
    - Intelligence
---

## Centos部署学习和Docker学习

#### 1. Centos7配置静态ip

```bash
# 编辑/etc/sysconfig/network-scripts/ifcfg-enp0s3为以下内容
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
IPADDR=192.168.56.113
NETMASK=255.255.255.0
GATEWAY=192.168.56.101
DNS1=114.114.114.114
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=048a1173-4820-444e-a66a-ac85e32725c8
DEVICE=enp0s3
ONBOOT=yes
ZONE=public
```

#### 2. Centos7安装Virtualbox增强功能

```bash
# 1. 更新系统
$ yum  makecache
$ yum update

# 2. 安装依赖
$ yum install gcc make kernel-devel kernel-headers bzip2

# 3. 挂载Vbox增强包镜像
$ cd  /media
$ mkdir  cdrom
$ mount  /dev/sr0  /media/cdrom

# 4. 安装Vbox增强包
$ cd  cdrom
$ ./VBoxLinuxAdditions.run
```

执行完毕后重启虚拟机便好.

#### 3. Oracle数据库安装

1. 下载preinstall和oracle数据库rpm安装包

   ```bash
   oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm
   oracle-database-ee-19c-1.0-1.x86_64.rpm
   ```

2. 关闭防火墙和禁用Selinux

   ```bash
   # 1. 查看seliux是否开启,执行getenforce,返回Enforcing,表面Selinux被启动为强制模式
   $ getenforce
   
   # 2. 禁用Selinux
   $ vim  /etc/selinux/config    # 将SELINUX=enforcing改为SELINUX=disabled
   
   # 3. 重启系统生效
   
   # 4. 关闭防火墙
   $ systemctl stop firewalld
   ```

3. 安装preinstall包,下载安装相关依赖包

   ```bash
   $ yum localinstall -y oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm 
   ```

4. 安装oracle数据库

   ```bash
   $ yum localinstall oracle-database-ee-19c-1.0-1.x86_64.rpm
   ```

5. 编辑并启动初始化配置脚本,创建数据库

   ```bash
   $ vim  /etc/init.d/oracledb_ORCLCDB-19c
   
   # 1. 在配置文件中检查以下环境变量是否配置好,字符集是否正确：
   #         export ORACLE_HOME=/opt/oracle/product/19c/dbhome_1
   #         export ORACLE_VERSION=19c
   #         export ORACLE_SID=ORCLCDB
   #         export TEMPLATE_NAME=General_Purpose.dbc
   #         export CHARSET=AL32UTF8
   #        export PDB_NAME=ORCLPDB1
   #        export LISTENER_NAME=LISTENER
   #        export NUMBER_OF_PDBS=1
   #        export CREATE_AS_CDB=true
   
   # 2. 执行初始配置脚本
   $ /etc/init.d/oracledb_ORCLCDB-19c configure
   ```

6. 创建/etc/profile.d/oracle19c.sh文件,或者是/home/oracle/bash_profile文件,文件内容如下所示：

   ```bash
   export ORACLE_HOME=/opt/oracle/product/19c/dbhome_1
   export PATH=$PATH:/opt/oracle/product/19c/dbhome_1/bin
   export ORACLE_SID=ORCLCDB
   ```

7. 修改oracle用户密码

   ```bash
   $ passwd  oracle
   ```

8. 防火墙打开1521端口

   ```bash
   $ firewall-cmd --zone=public --add-port=1521/tcp --permanent
   $ systemctl  restart  firewalld
   ```

安装完成.

#### 4. Redis安装

1. 从Redis官网下载最新的redis安装包(*.tar.gz).

2. 安装gcc和make

3. 解压和编译安装

   ```bash
   $ tar -xzvf redis-5.0.2.tar.gz
   $ cd redis-5.0.2
   $ make
   $ make install
   ```

4. 编辑配置文件./redis-5.0.2/redis.conf

   ```bash
   # 绑定ip地址
   bind 192.168.56.115
   # 设置端口
   port 9803
   # 设置密码, 注释掉便是不需要密码
   requirepass mypassword(mypassword是需要设置的密码)
   # 启动后台运行
   daemonize yes
   # 指定输出日志文件
   logfile "/var/log/redis/6379.log"
   
   # 拷贝配置文件到指定目录
   $ cp /root/redis-5.0.2/redis.conf  /etc/redis/redis.conf
   ```

5. 设置启动服务

   ```bash
   # 编辑/usr/lib/systemd/system/redis.service文件
   [Unit]
   Description=Redis 6379
   After=syslog.target network.target
   [Service]
   Type=forking
   PrivateTmp=yes
   Restart=always
   ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
   ExecStop=/usr/local/bin/redis-cli -h 127.0.0.1 -p 6379 -a jcon shutdown
   User=root
   Group=root
   LimitCORE=infinity
   LimitNOFILE=100000
   LimitNPROC=100000
   [Install]
   WantedBy=multi-user.target
   
   # 使服务自动运行
   systemctl daemon-reload
   systemctl enable redis
   # 启动服务
   systemctl restart redis
   systemctl status redis
   ```

#### 5. mysql安装

1. 下载[mysql离线安装包](https://dev.mysql.com/downloads/mysql/5.7.html)

   ```bash
   # 安装mysql至少需要安装以下5个包
   mysql-community-client-5.7.34-1.el7.x86_64.rpm
   mysql-community-common-5.7.34-1.el7.x86_64.rpm
   mysql-community-libs-5.7.34-1.el7.x86_64.rpm
   mysql-community-libs-compat-5.7.34-1.el7.x86_64.rpm
   mysql-community-server-5.7.34-1.el7.x86_64.rpm
   ```

2. centos默认安装有mariadb,需要先卸载mariadb包

   ```bash
   sudo rpm -e --nodeps mariadb-libs-5.5.60-1.el7_5.x86_64
   ```

3. 依次安装

   ```bash
   sudo yum localinstall mysql-community-common-5.7.34-1.el7.x86_64.rpm 
   sudo yum localinstall mysql-community-libs-5.7.34-1.el7.x86_64.rpm 
   sudo yum localinstall mysql-community-libs-compat-5.7.34-1.el7.x86_64.rpm 
   sudo yum localinstall mysql-community-client-5.7.34-1.el7.x86_64.rpm 
   sudo yum localinstall mysql-community-server-5.7.34-1.el7.x86_64.rpm 
   ```

4. 获取root临时密码

   ```bash
   grep "temporary password" /var/log/mysqld.log
   ```

5. 修改root密码

   ```bash
   # 启动mysqld服务
   sudo systemctl start mysqld
   # 输入临时密码,登入mysql服务器
   mysql -u root -p   
   # 修改密码
   mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '123334556.';
   mysql> FLUSH PRIVILEGES;
   ```

6. 设置mysql监听地址

   ```bash
   # 编辑/etc/my.cnf配置文件,添加一行配置
   bind-address=127.0.0.1
   # 重启服务
   sudo systemctl restart mysqld
   ```

7. mysql添加一个用户并授权

   ```bash
   # 关闭强密码控制
   validate_password=off
   
   # 1. 创建一个用户soft
   mysql> create user soft identified by '123456';
   
   # 2. 创建数据库nacos
   mysql> create database nacos default character set utf8;
   
   # 3. 将数据库所有权限授予给soft用户
   mysql> grant all privileges on nacos.* to soft@'%' identified by '123456';
   
   # 4. 允许soft用户本地登录mysql服务器
   mysql> grant all privileges on nacos.* to soft@'localhost' identified by '123456';
   
   # 5. 重启权限
   mysql> flush privileges;
   ```

#### 6. 增加一个用户

```bash
# 增加用户组
sudo groupadd soft    # 增加soft组
sudo useradd  -d  /home/soft  -g  soft  -s  /usr/bin/bash  soft    # 添加soft用户
sudo passwd soft    # 修改密码
```

#### 7. Nacos安装

1. 下载nacos-server-1.4.2.tar.gz

2. 解压后进入conf文档，编辑application.properties

   ```bash
   # 设置ip和端口
   # 设置mysql数据源
   ```

   

3. 添加JAVA_HOME环境变量

4. 以单机模式启动

   ```bash
   ./startup.sh -m standalone
   ```

5. 访问控制台查看是否启动成功

   ```bash
   http://192.168.2.11:8802/nacos
   ```


#### 8. Minio部署

1. 下载Minio

   ```bash
   wget https://dl.min.io/server/minio/release/linux-amd64/minio
   ```

2. 增加可执行权限

   ```bash
   chmod 755 minio
   ```

3. 在当前用户的home目录下编辑.bashrc,添加下面的环境变量

   ```bash
   # Set up Minio environment variables
   export MINIO_ROOT_USER=minioadmin
   export MINIO_ROOT_PASSWORD=123445566
   ```

4. 设置执行脚本

   ```bash
   # 设置全局变量
   MINIO_ELF_FILE="/soft/minio"                     # 可执行文件目录
   MINIO_DATA_DIR="/was/minio/data"        # Minio数据目的
   IP_ADDR=`hostname -i`
   PORT="8561"
   
   # 启动minio，nohup为不挂起方式启动进程，即后台进程
   nohup $MINIO_ELF_FILE server $MINIO_DATA_DIR --address $IP_ADDR:$PORT > minio.out 2>&1 &
   ```


#### 9. 安装Docker

**Centos通过在线库安装Docker:**

```bash
# 1. 安装yum工具包
yum install -y yum-utils

# 2. 添加仓库索引
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. 安装docker
yum install docker-ce docker-ce-cli containerd.io

# 4. 启动docker
sudo systemctl start docker
```

**离线安装Docker:**

1. 需要先有一台可以在线安装docker的Centos设备, 下载安装docker所需要的程序包

   ```bash
   # 以root用户登录, 非root需要加sudo, downloaddir指定下载的程序包存放目录, 
   yum install --downloadonly --downloaddir=/root/docker docker-ce docker-ce-cli containerd.io container-selinux
   
   # 下载后的程序包列表
   containerd.io-1.4.12-3.1.el7.x86_64.rpm
   container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
   docker-ce-20.10.12-3.el7.x86_64.rpm
   docker-ce-cli-20.10.12-3.el7.x86_64.rpm
   docker-ce-rootless-extras-20.10.12-3.el7.x86_64.rpm
   docker-scan-plugin-0.12.0-3.el7.x86_64.rpm
   ```

2. 将程序包传送到需要离线安装docker的设备

   ```bash
   # 在/root/docker目录下执行
   scp * deploy@192.168.230.11:~/docker/
   ```

3. 依次执行如下安装命令以安装docker

   ```bash
   sudo rpm -ivh container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
   sudo rpm -ivh containerd.io-1.4.12-3.1.el7.x86_64.rpm
   sudo rpm -ivh docker-scan-plugin-0.12.0-3.el7.x86_64.rpm --nodeps --force   # 解决循环依赖,强制安装
   sudo rpm -ivh docker-ce-cli-20.10.12-3.el7.x86_64.rpm
   sudo rpm -ivh docker-ce-rootless-extras-20.10.12-3.el7.x86_64.rpm --nodeps --force
   sudo rpm -ivh docker-ce-20.10.12-3.el7.x86_64.rpm
   ```

4. 启动docker

   ```bash
   sudo systemctl start docker
   ```

5. 验证docker是否安装成功

   ```bash
   # 查看docker版本号
   sudo docker -v
   
   # 查看docker信息
   sudo docker info
   ```

6. 添加app用户到docker用户组

   ```bash
   sudo usermod -aG docker app
   ```

7. 设置docker镜像的工作目录, 因为docker的默认工作目录在/var/lib/docker下,但/var目录一般在内网虚拟接中分配的空间很少,所以需要设置一下docker的工作目录

   ```bash
   # 1. 编辑/usr/lib/systemd/system/docker.service文件
   vim /usr/lib/systemd/system/docker.service
   
   # 修改或添加如下内容,主要是--graph /backup/dockerInnerImgs, 
   # /backup/dockerInnerImgs是我们设置的新的docker的工作目录
   ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --graph /backup/dockerInnerImgs
   
   # 创建/backup/dockerInnerImgs目录
   mkdir /backup/dockerInnerImgs
   
   # 重启docker,以生效配置
   sudo systemctl stop docker
   sudo systemctl stop docker.socket
   sudo systemctl start docker
   
   # 查看docker的工作目录是否已发生变更
   sudo docker info | grep "Docker Root Dir"
   ```



#### 10. Docker使用

1. 启动容器后,进入容器命令行

   ```bash
   # 启动容器,开启伪终端-t, 打开输入流-i, 后台运行-d
   docker  run -itd  abc/tttccc:1.0.1
   
   # 进入容器, 69d1fdc是容器编号,使用docker ps -a查看
   docker  exec  -it  69d1fdc  bash
   
   ```
   
2. 启动容器时暴露端口到外部环境

   ```bash
   # 1. 首先需要在Dockerfile文件中指定EXPOSE
   
   # 2.在容器运行时指定端口暴露
   docker  run  -p  80:80  镜像名称:tag
   
   # 暴露容器所有端口到主机的随机端口
   docker run -P
   
   ```

3. 迁移容器镜像

   ```bash
   # 1. 迁出容器镜像
   docker save -o outputDir/镜像名.tar 镜像名:tag
   
   # 2. 迁入镜像
   docker  load  --input  镜像名.tar
   ```

4. 停止正在运行的容器和异常状态下的容器并删除这些容器

   ```bash
   docker stop $(docker ps -a | grep "Up" | awk '{print $1 }')
   docker stop $(docker ps -a | grep "Exited" | awk '{print $1 }')
   docker rm $(docker ps -a | grep "Exited" | awk '{print $1 }')
   ```

5. 查看正在运行的容器

   ```bash
   docker ps -a
   ```

6. 查看所有镜像

   ```bash
   docker images
   ```

7. 修改容器后提交修改后的新镜像

   ```bash
   # 1.查看正在运行的容器
   docker  ps -a
   
   # 2. 进入正在运行的容器内
   docker exec –it  3bd0eef03413 bash  
   
   # 3. 进入容器后, 就可以修改镜像了, 比如修改镜像中已经部署的代码或者安装新的软件或包等;
   # 修改完成之后, exit 退出容器
   
   # 4. 提交你刚才修改的镜像, 新的镜像名称为demo, 版本为1.0.3
   docker  commit  3bd0eef03413  demo:1.0.3  
   ```

8. 

