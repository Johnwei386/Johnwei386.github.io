---
layout:     post
title:      Ubuntu系统安装Samba服务器
subtitle:   Ubuntu18.04安装配置Samba服务器
date:       2021-02-18
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Ubuntu
    - Samba
---


## 1. 安装Samba服务器
```bash
sudo apt update
sudo apt install samba
```

## 2. 创建共享目录
```bash
mkdir /home/abc/share
chmod 777 /home/abc/share
```

## 3. 设置samba用户密码
```bash
sudo smbpasswd -a abc
# 输入密码
# 再次输入密码
```

## 4. 编辑配置文件
```bash
sudo nano /etc/samba/smb.conf

# 在smb.conf的最后添加如下内容:
[share]
   comment = share folder
   browseable = yes
   path = /home/abc/share
   create mask = 0700
   directory mask = 0700
   valid users = abc    
   force user = abc    
   force group = abc    
   public = yes
   available = yes
   writable = yes

```

## 5. 重启Samba服务
```bash
sudo service smbd restart
```