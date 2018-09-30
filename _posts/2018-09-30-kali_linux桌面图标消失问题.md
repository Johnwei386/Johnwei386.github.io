---
layout:     post
title:      kali_linux桌面图标问题
subtitle:   找回消失的图标
date:       2018-09-30
author:     JW
header-img: img/jwblog/post-kali-linux.jpg
catalog: true
tags:
    - kali 
    - linux 
    - gnome
---

## 前言

Gnome的桌面图标一直由Nautilus项目支持，Nautilus是Gnome图形界面里用来管理文件的文件管理器。桌面
图标从Gnome3开始就不在被支持了，Nautilus项目一直在支持这个项目，但是随着项目的不断发展，它对桌
面图标的支持开始变成自身发展的瓶颈，超过10000行用来实现桌面功能的代码，其所使用的技术是1999年
开发的(确实有点老哈)，Nautilus从3.28版本开始就不在支持桌面图标实现了，它将这部分陈旧的代码从
自身的开发树中迁出，不在对其进行维护和支持。
参考：[Nautilus Desktop Plans](https://csorianognome.wordpress.com/2017/12/21/nautilus-desktop-plans/)


## Kali_linux桌面图标消失

在更新Kali linux到最新的版本后(2018.4)，桌面图标突然不见了，但是还是可以通过命令行和文件管理器
对桌面目录的文件进行管理和相关操作，具体原因如上，是因为Nautilus项目不在支持其日渐苍老的桌面端
代码。

### 解决方案 

Gnome社区提出了一个替代方案，使用Gnome扩展来实现这一功能。该扩展的下载地址及安装方法见:
> [desktop-icons](https://gitlab.gnome.org/World/ShellExtensions/desktop-icons)
具体操作，需要将下载回来的插件文件解压到~/.local/share/gnome-shell/extensions目录下，并且需要将
解压后的文件目录改名为该目录中的metadata.json文件中的UUID对应的name。比如为
desktop-icons@csoriano。

### 总结 

该方法确实能实现桌面图标的正常使用，但是和从前的相比，性能还有体验都不如从前的好，期望将来能有
一个专门的开源项目，用于实现Gnome桌面图标的使用。
