---
layout:     post
title:      Raspberry Pi 开机自动连接主机开启的wifi热点
subtitle:   主机可通过ssh连接到客户机
date:       2017-10-19
author:     JW
header-img: img/post-bg-unix-linux.jpg
catalog: true
tags:
    - raspberry
    - pi
---

raspberry pi B+板的无线网卡网上就有卖的，可以在购买板子的时候就咨询卖家有没有匹配的无线网卡卖，应该是有的，只是要另外加钱。好了，废话少说，其实要让树莓派连接上wifi热点，现在想想其实蛮简单的，主要就是要改两个文件，首先是/etc/network/interfaces文件，我的例子如下，亲测有效：

```c
auto lo
iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa.conf
iface default inet dhcp
```

之后就是创建/etc/wpa.conf这个文件，文件内容编辑如下：

```c
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="your hotpot ssid name"
	psk="your hotpot password"
	priority=1 #连接优先级定义，数字越大，越被优先连接
}
```

priority的值越大表示优先级越高。wpasupplicant这个程序必须要提前安装，树莓派官方系统已经预装这个程序，通过它系统可以管理wifi连接，在桌面上有相关的GUI界面，但是通过定义相关文件，也可以实现在命令行界面下管理wifi连接(^_^)。
