---
layout:     post
title:      shadowsocks命令行启动
subtitle:   配置shadowsocks
date:       2018-10-11
author:     JW
header-img: img/jwblog/post-shadowsocks.png
catalog: true
tags:
    - linux
	- shadowsocks
---

## 前言
习惯于使用图形界面操作shadowsocks，然而，在某些情况下，需要在命令行下打开本地隧道代理服务器，因此，需要在本地安装和配置shadowsocks。

## shadowsocks安装和配置
在/etc下，新建一个文件shadowsocks.json，内容如下：
> {
> "server":"shadowsocks服务端的ip地址",
> "server_port":服务端的端口号,
> "local_address": "127.0.0.1",
> "local_port":4096,
> "password":"你的密码",
> "timeout":600,
> "method":"aes-256-cfb"
> }

## 启动shadowsocks客户端
由于更新了linux系统，基于debian9的最新版Kali-linux，导致原来pip库的shadowsocks包无法启动，因此下载最新的软件版本：
> pip install -U git+https://github.com/shadowsocks/shadowsocks.git@master
启动本地客户端：
sslocal -c /etc/shadowsocks.json -d start
