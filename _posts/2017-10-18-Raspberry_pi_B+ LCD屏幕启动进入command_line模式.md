---
layout:     post
title:      Raspberry Pi B+ LCD屏幕启动进入command line模式
subtitle:   自己总结的一些Raspberry玩机技巧
date:       2017-10-18
author:     JW
header-img: img/post-bg-unix-linux.jpg
catalog: true
tags:
    - raspberry
    - pi
---

Raspberry pi B+的原生系统是基于Debian7.5开发的一款系统，自己买了一块LCD小屏幕，厂商送带屏幕驱动的image系统镜像，但是，它默认启动进入桌面，我想让它启动后进入命令行，桌面比较占用内存。所以开始在网上找资料，首先，通过进入系统后打开命令行，执行raspi-config可以进入树莓派系统配置界面，找到start X server boot之类的选项，选择disable可以禁用开机进入命令行，但是不启动桌面服务器。但是，这个方法不适用于我，因为，我找了好久也没找到这个选项。

最后找到一个方法，是通过修改/etc/inittab这个文件中的启动项来引导系统进入相关界面，类unix系统在电源开机后，由boot引导镜像导入OS镜像，执行权交给OS后执行的第一个程序是init，然后由init去启动server管理器，由server来开启要随boot过程而启动的服务程序。在这个过程中，/etc/inittab文件是init要访问的第一个文件，借助一个实例文件来说明：
```c
 # inittab This file describes how the INIT process should set up

 # Default runlevel. The runlevels used by RHS are:
 
 #   0 - halt (Do NOT set initdefault to this)
 
 #   1 - Single user mode
 
 #   2 - Multiuser, without NFS (The same as 3, if you do not have networking)
 
 #   3 - Full multiuser mode
 
 #   4 - unused
 
 #   5 - X11
 
 #   6 - reboot (Do NOT set initdefault to this)

1) id:3:initdefault:

 # System initialization.
 
2) si::sysinit:/etc/init.d/rcS

3) l0:0:wait:/etc/rc.d/rc 0
4) l1:1:wait:/etc/rc.d/rc 1
5) l2:2:wait:/etc/rc.d/rc 2
6) l3:3:wait:/etc/rc.d/rc 3
7) l4:4:wait:/etc/rc.d/rc 4
8) l5:5:wait:/etc/rc.d/rc 5
9) l6:6:wait:/etc/rc.d/rc 6
```

每一行前的数字只是为了更好的说明问题而加上的，源文件中并没有。最重要的是第1行，它决定了系统启动后进入什么运行界面，关于linux的运行级别的介绍，可参考相关文章，其中3是字符命令行多用户界面，5是桌面模式；initdefault表示这个启动级别是默认的，然后到第2行系统boot引导过程中执行的一些初始化操作，然后由前面的运行级别设置在3到9行选择一个并进入相关目录执行初始化操作。

在选择3作为启动界面的运行级别设置后，重启树莓派，但是结果出乎人所料，系统依旧进入桌面操作系统，将运行级别改为1，即启动后进入单用户模式，默认不开启网络支持，之后重启系统后进入的就是命令行模式的登录界面，但是，它不能在启动后自动开启wlan连接我用主机搭建的wifi热点，因为它默认在单用户模式就是不开启网络支持，ifplugd这个守护进程会阻断所有网络连接，有线网没试过，但是无线网卡即便是在开机时就通过DHCP获取了IP，但是开机登录之后还是必须要手动 ifdown wlan0；ifup wlan0。

之后探索了很长时间，其间被各种事情耽误，不能安心寻找对应方法，直到最近又重新拾起我的树莓派机器，寻找新的方法来实现我的初心，不妥协每次开机都要手动开启wifi。其实最后的原因其实很简单，我原本想在/etc/rc.local中手动写入一条开启无线网卡的命令来解决这个问题，但是在实验之后，这条命令并未执行，原因如前所述，单用户运行模式下会阻断网络连接；之后就只有换运行模式，就是标称的运行模式3，字符界面，但是它依旧进入桌面环境；通过 update-rc.d  lightdm disable 来禁用X Server的显示管理器，禁用之后重启系统依旧进入桌面环境。

 本来要放弃了，但是仔细一想，突然明白是怎么回事了。在单例模式中，系统启动后并未启动/etc/rc.local中的定义的命令，但是在其他的运行模式中，系统在初始化的最后会启动/etc/rc.local中的命令；然后，我去查看这个文件，发现在文件的下面有这么一行内容：
 
	su -l pi -c "env FRAMEBUFFER=/dev/fb1 startx  -- -dpi 60 &"
	
一切豁然开朗，注释掉这行内容之后，重启系统，就出现了久违的字符登录界面(^_^)。

![](/img/jwblog/raspberry/figure1.png)
