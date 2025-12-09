---
layout:     post
title:      Ubuntu与Windows10双系统安装
subtitle:   在Ubuntu18.04安装CUDA
date:       2021-02-18
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Ubuntu
    - Windows10
    - 双系统
---


## 1. 硬件基本情况
1. intel Core i7-11700F;
2. 微星 B650M主板;
3. 内存32G;
4. 技嘉3060魔鹰显卡;
5. 1T固态硬盘;

## 2. 硬盘分区
1. efi分区：512M, 挂载点/boot/efi
2. SWAP分区：4G, 内存够用的情况下可酌情设置
3. 系统分区：100G, 挂载点/
4. home分区：500G, 挂载点/home
5. Windows系统分区：300G 
安装系统前，需要进入BIOS，在BIOS->Settings->Security下禁用Secure Boot.

## 3. 先安装Windows10系统
#### 3.1 制作USB启动盘镜像
Windows10 1903版本之后的Windows的ISO镜像刻录到U盘是不可以实现UEFI启动的，因为UEFI引导要求引导盘格式必须为FAT32，而FAT32格式的U盘单个文件不允许大于4GB，而ISO镜像中有一个名叫install.wim的单文件，其大小超过了4G. 只能借助微软官方的工具——MediaCreationTool，去制作支持UEFI引导的安装U盘.

使用rufus工具将Windows10-21h版系统ISO镜像写入U盘，使用的是win7系统的虚拟机，在[rufus下载地址](https://rufus.ie/downloads/)下载rufus-3.8，经测试3.8版本在win7系统能正常运行，高版本的如3.15会报错，然后还会遇到一个设备被占用的问题，是windows的explorer.exe还在使用着设备，打开任务管理器，直接停止该程序后，再次运行rufus，就可以避免设备被占用的问题，大约等待十几分钟后，镜像写入成功，U盘启动盘就可以了.

使用[wepe工具](http://www.wepe.com.cn/download.html)制作启动PE工具，经测试，界面清爽，无广告，多分区使用，既可以当启动盘，又可以当优盘，且兼容UEFI和Legecy多种启动方式，完美兼容新旧机器的装机.

#### 3.2 安装Windows10系统
使用制作好的win10启动盘启动电脑，进入安装界面，安装win10系统. 使用windows的安装器，若没有事前分好区，则安装器会在空闲空间上进行分区，分为一个16M大小的保留分区和系统盘两个分区，若不想生成这个保留分区，则需要通过使用另一个磁盘分区工具（gparted或diskGenius）来创建消耗所有未分配空间的新分区，而不是从Windows安装程序中在未分配的空间中创建新分区. 不可以在安装完系统之后再删除保留分区.

系统安装完成后，在控制面板 -> 电源选项 -> 系统设置 里面取消“启动快速启动(推荐)”，以关闭Windows快速启动.

如果是安装的1607这样的旧版本的win10，可以在安装系统完成后下载win10易升(Windows10Upgrade9252.exe)，升级win10系统到最新版.

#### 3.3 激活Windows10
使用[云萌Windows 10激活工具](https://cmwtat.cloudmoe.com/cn.html)激活win10，云萌Windows 10激活工具采用数字权利激活手段激活系统，凡通过**Win10数字权利激活工具激活**的系统，可以获得和正版⼀模⼀样的服务，可以登录自己的微软账户，重装之后联⽹就能⾃动激活，可以更新系统等等。当你用数字权利激活工具激活了这台电脑的系统之后，你这台电脑的激活信息将会与你的电脑主板绑定，以后不管你这台电脑重装多少次系统，哪怕你格式化全盘重装，只要进入系统后一联网，系统就能自动激活。因为你这台电脑的主板ID已经被微软上传到他们的激活服务器了，下次重装系统后只要联网微软的激活服务器就能识别到你的主板ID并立即将系统激活；数字权利激活工具激活是目前最合适win10的激活方法。该激活方法不适用于Win7.

#### 3.4 安装nvidia驱动
在[nvidia驱动高级搜索](https://www.nvidia.cn/Download/Find.aspx?lang=cn)搜索3060显卡的驱动，GeForce, RTX 30 Series, 3060, Win10 64bit, 标准, 中文, all，下载最新版的显卡驱动后安装即可.

## 4. 安装Ubuntu18.04
使用预先制作好的Ubuntu18.04启动盘启动电脑，按按程序安装系统. 

1. 在安装类型处选择其他选项，设置分区与挂载点. efi分区是UEFI启动专用系统分区，因为前面已经安装了win10，所以这里会显示Windows的启动引导. 
2. 选择根目录和home目录的挂载点并勾选格式化，之前已经在U盘系统中用分区工具(Gparted)进行了分区操作.
3. 继续按安装程序操作，直至安装完成.

## 5. 安装GRUB,实现双系统引导
先安装Windows10, 后安装Ubuntu18.04时, Ubuntu的安装程序会自动搜索各磁盘下的系统引导, 所以一般第5步并不需要执行.

1. 使用Ubuntu优盘启动盘，在BIOS调好引导顺序后，启动U盘系统，点击”试用“，进入Ubuntu系统.

2. 将系统连上网络，确定是能上网的网络.

3. 执行如下命令:

   ```bash
   # 添加boot-repair的安装源, 并更新软件源缓存
   sudo add-apt-repository ppa:yannubuntu/boot-repair && sudo apt-get update
   
   # 安装boot-repair
   sudo apt-get install -y boot-repair 
   
   # 执行
   sudo boot-repair
   ```

4. 在boot-repair程序界面点击"推荐修复", 选择不上传日志到pastebin网站.

5. 程序执行完成会打开一个运行日志文件,可以在此文件中查看运行情况, 日志文件是/var/log/boot-repair/日期目录下的boot-repair.log(见附件1).

6. 关机，拔出启动盘，重启电脑，由于还没有调整UEFI的启动顺序，重启后还会进入Win10系统.

7. 在Win10系统，按Win+S打开搜索界面，搜索"cmd"，选择"以管理员权限运行"，执行如下命令:

   ```bash
   bcdedit  /set  {bootmgr}  path  \EFI\ubuntu\shimx64.efi
   ```

   调整UEFI启动项顺序以ubuntu系统为首项.

8. 重启进入已安装完成的Ubuntu系统，联网，执行如下命令：

   ```bash
   sudo update-grub
   ```

** 卸载并重装GRUB: **
```bash
# 卸载Grub, chroot:将执行目录切换到特定的目录下
sudo chroot "/mnt/boot-sav/nvme0n1p3" apt-get purge --allow-remove-essential -y grub*-common shim-signed

# 重装Grub
sudo chroot "/mnt/boot-sav/nvme0n1p3" apt-get install -y grub-efi
```

## 6. Ubunntu18.04系统优化
1. 卸载Ubuntu预置的桌面环境

   ```bash
   sudo apt remove gnome-shell-extension-ubuntu-dock
   sudo apt remove ubuntu-desktop
   ```

2. 安装Gnome桌面，安装完成后重启

   ```bash
   sudo apt install vanilla-gnome-desktop
   ```

3. 更新Grub

   ```bash
   sudo update-grub
   ```

4. 解决鼠标滑动到左上角时Activities不弹出活动问题

   ```bash
   # 1. 火狐浏览器打开https://extensions.gnome.org/extension/358/activities-configurator/
   
   # 2. 安装Gnome插件，安装chrome-gnome-shell系统插件
   sudo apt install chrome-gnome-shell
   
   # 3. 激活并安装Activities插件
   ```

5. 以代理模式启动Chrome浏览器

   ```bash
   chromium-browser --proxy="socks5://127.0.0.1:1080"
   # chrome浏览器安装
   google-chrome --proxy-server="socks5://127.0.0.1:1080"
   ```

6. 解决Ubuntu 18.04与Win10系统时间不一致问题

   ```bash
   sudo timedatectl set-local-rtc 1 --adjust-system-clock
   ```

7. 添加应用程序到桌面

   ```bash
   # 执行如下命令，然后将应用程序桌面图标复制到桌面，并赋予可执行权限即可
   nautilus /usr/share/applications
   ```

8. 卸载libreoffice, 然后安装wps-office

   ```bash
   # 1. 卸载libreoffice
   sudo apt-get remove --purge libreoffice*
   sudo apt-get clean
   sudo apt-get autoremove
   
   # 2. 安装字体
   sudo  mkdir  /usr/share/fonts/adobe
   sudo  mkdir /usr/share/fonts/wps
   sudo  cp  adobefonts/*  /usr/share/fonts/adobe/
   sudo  cp  wps_symbol_fonts/*  /usr/share/fonts/wps/
   
   # 安装wps
   sudo dpkg -i wps-office_11.1.0.10161_amd64.deb
   ```

9. 安装音乐播放器

   ```bash
   sudo apt install audacious
   ```

10. 安装vlc播放器

    ```bash
    sudo apt install vlc
    ```

11. 安装wireshark

    ```bash
    sudo apt install wireshark
    ```

12. 安装Gnome Tweaks

    ```bash
    sudo apt install gnome-tweaks
    ```

13. 安装net-tools，使可以使用ifconfig命令

    ```bash
    sudo apt install net-tools
    ```

14. 安装sogou拼音输入法

    ```bash
    # 1. 卸载并清除预置的ibus
    sudo apt-get purge ibus
    
    # 2. 卸载右上角顶部的键盘指示器
    sudo  apt-get remove indicator-keyboard
    
    # 3. 安装fcitx
    sudo apt install fcitx-table-wbpy fcitx-config-gtk
    
    # 4. 下载最新版的sogou拼音输入法
    
    # 5. 安装sogou拼音输入法
    sudo dpkg -i sogoupinyin_2.2.0.0108_amd64.deb
    
    # 解决依赖问题, 再次执行sogou拼音的安装程序
    sudo apt-get install -f
    sudo dpkg -i sogoupinyin_2.2.0.0108_amd64.deb
    
    # 6. 重启生效
    ```

## 7. Ubuntu18.04安装CUDA
1. 编辑/etc/modprobe.d/blacklist-nouveau.conf文件, 文件不存在则新建之, 文件内容如下：

   ```bash
   # generated by nvidia-installer
   blacklist nouveau
   options nouveau modeset=0
   ```

2. 更新当前kernel的initramfs, 此命令更新需要载入内核的模块

   ```bash
   sudo update-initramfs -u
   
   # 在centos系, 没有initramfs工具, 使用dracut工具替换
   sudo  dracut  -f
   ```

   Dracut是一款Linux系统下的initramfs生成器。在Linux启动过程中，initramfs作为一个虚拟的根文件系统存在于内存中，它的作用是提供启动所需的驱动程序和文件系统模块。dracut命令可以用来创建或更新initramfs， 参数说明：

   > 1. -f, --force: 强制生成initramfs，即使已经存在；
   > 2. -H, --hostonly: 仅添加主机上已加载模块的驱动程序到initramfs中；
   > 3. -N, --nomdadmconf: 不在initramfs中包含mdadm.conf文件；
   > 4. -o, --omit: 省略指定的模块或驱动程序；
   > 5. -m, --add: 添加指定的模块或驱动程序；
   > 6. -v, --verbose: 显示详细的日志信息；
   > 7. -k, --kver: 指定内核版本号；

3. 安装基本编译组件

   ```bash
   sudo  apt-get  install  build-essential
   
   # centos系使用下面命令进行安装
   sudo  yum  install  make  automake  gcc  gcc-c++  kernel-devel
   ```

4. 下载适配Ubuntu 18.04的Cuda和适配该Cuda的cuDNN, 这里下载cuda_11.4.2_470.57.02_linux和cuDNN_8.2.4, cuDNN下载"[cuDNN Library for Linux (x86_64)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.2.4/11.4_20210831/cudnn-11.4-linux-x64-v8.2.4.15.tgz)".

5. 由于CUDA自带驱动,所以不用提前下载NVIDIA显卡驱动安装,再说安装的版本号也不一定能和Cuda的版本号对上, 这里cuda_11.4.2_470.57.02_linux中的470.57就是显卡驱动的版本号, 这个需要对的上, 所以不用预先安装显卡驱动; 

6. 将下载好的cuda和cudnn安装文件放在指定目录,如/home/abc/preInstalledSoft目录下,避免目录名不要出现中文;

7. 重启, 在Ubuntu引导界面,选择“高级选项 -> recovery mode”, 进入recovery模式, 选择root, 以root用户开启一个命令行窗口, 执行以下命令, 在这里执行cuda和显卡驱动的安装可以规避由于在没有完全禁用掉nouveau模块的情况下, 安装显卡驱动后会出现重启后循环登录,黑屏等问题, 在recovery模式下安装驱动,不会预加载nouveau模块.

   ```bash
   cd  /home/abc/preInstalledSoft
   chmod  755  cuda_11.4.2_470.57.02_linux.run
   # 执行cuda安装程序
   ./cuda_11.4.2_470.57.02_linux.run
   
   # 在安装配置项中更改一下samples, 即样例的安装地址, 改为常用用户的工作目录
   ```

   安装成功后, 返回如下摘要信息:

   ```bash
   ============
   =  Summary  =
   ============
   
   Driver:    Installed
   Toolkit:    Installed in /usr/local/cuda-11.4/
   Samples:    Installed in /home/abc/, but missing recommended libraries
   
   please make sure that
       -        PATH includes /usr/local/cuda-11.4/bin
       -        LD_LIBRARY_PATH includes /usr/local/cuda-11.4/lib64, or, add /usr/local/cuda-11.4/lib64 to /etc/ld.so.conf and run ldconfig as root
   
   To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-11.4/bin
   To uninstall the NVDIA Driver, run nvidia-uninstall
   Logfile is /var/log/cuda-installer.log
   ```

8. 编辑/etc/profile文件, 在profile文件的最后增加以下内容, 重启生效.

   ```bah
   export  PATH=$PATH:/usr/local/cuda-11.4/bin
   export  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.4/lib64
   ```

9. 查看nvidia驱动是否安装成功

   ```bash
   nvidia-smi
   ```

10. 编译cuda附带的一个样例

    ```bash
    cd  /home/abc/NVIDIA_CUDA-11.4_Samples/1_Utilities/deviceQuery 
    make
    ./deviceQuery
    ```

    返回以下信息:

    ```bash
    ./deviceQuery Starting...
    
     CUDA Device Query (Runtime API) version (CUDART static linking)
    
    Detected 1 CUDA Capable device(s)
    
    Device 0: "NVIDIA GeForce RTX 3060"
      CUDA Driver Version / Runtime Version          11.4 / 11.4
      CUDA Capability Major/Minor version number:    8.6
      Total amount of global memory:                 12045 MBytes (12630491136 bytes)
      (028) Multiprocessors, (128) CUDA Cores/MP:    3584 CUDA Cores
      GPU Max Clock rate:                            1837 MHz (1.84 GHz)
      Memory Clock rate:                             7501 Mhz
      Memory Bus Width:                              192-bit
      L2 Cache Size:                                 2359296 bytes
      Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
      Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
      Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
      Total amount of constant memory:               65536 bytes
      Total amount of shared memory per block:       49152 bytes
      Total shared memory per multiprocessor:        102400 bytes
      Total number of registers available per block: 65536
      Warp size:                                     32
      Maximum number of threads per multiprocessor:  1536
      Maximum number of threads per block:           1024
      Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
      Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
      Maximum memory pitch:                          2147483647 bytes
      Texture alignment:                             512 bytes
      Concurrent copy and kernel execution:          Yes with 2 copy engine(s)
      Run time limit on kernels:                     Yes
      Integrated GPU sharing Host Memory:            No
      Support host page-locked memory mapping:       Yes
      Alignment requirement for Surfaces:            Yes
      Device has ECC support:                        Disabled
      Device supports Unified Addressing (UVA):      Yes
      Device supports Managed Memory:                Yes
      Device supports Compute Preemption:            Yes
      Supports Cooperative Kernel Launch:            Yes
      Supports MultiDevice Co-op Kernel Launch:      Yes
      Device PCI Domain ID / Bus ID / location ID:   0 / 1 / 0
      Compute Mode:
         < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >
    
    deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 11.4, CUDA Runtime Version = 11.4, NumDevs = 1
    Result = PASS
    ```
    则cuda安装成功！

    

## 8. 安装cuDNN
```bash
# 在nvidia官网下载cudnn到preInstalledSoft目录
cd  /home/abc/preInstalledSoft
tar  xvzf  cudnn-11.4-linux-x64-v8.2.4.15.tgz

# 安装cudnn
sudo cp cuda/include/cudnn.h /usr/local/cuda-11.4/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda-11.4/lib64
sudo chmod a+r /usr/local/cuda-11.4/include/cudnn.h 
sudo chmod a+r /usr/local/cuda-11.4/lib64/libcudnn*
```



## 9. 卸载Nvidia驱动

如果以前是通过ppa源安装的，可以通过下面命令卸载：

```bash
sudo  apt-get  remove  --purge  nvidia*
```

如果以前是通过runfile安装的，可以通过下面命令卸载：

```bash
sudo  ./NVIDIA-Linux-x86_64-430.09.run  --uninstall     #（430.09为我使用的版本号，要自行修改对应版本）
```

