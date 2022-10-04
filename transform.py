#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import re

def getCurDir():
    return os.path.abspath(os.path.dirname(__file__))

def handleFile(upDir, file, isGit=False):
    p1 = re.compile(r'.*神经设计原则.*')
    m1 = p1.match(file)
    if m1:
        all_cont = []
        p2 = re.compile(r'.*(/img/jwblog/neuralDesign.*)')
        with open(os.path.join(upDir, file), 'r') as f:
            for line in f:
                m2 = p2.match(line)
                if m2:
                    a = m2.group(1)
                    if isGit:
                        a = '![]({}'.format(a)
                    else:
                        a = '![](../{}'.format(a)
                    all_cont.append(a)
                else:
                    all_cont.append(line)
        
        with open(os.path.join(upDir, file), 'w') as f:
            for line in all_cont:
                f.write(line)


if __name__ == '__main__':
    curPath = getCurDir()
    postDir = os.path.join(curPath, '_posts')
    files = os.listdir(postDir)
    for file in files:
        handleFile(postDir, file, isGit=True)  # 将图片路径转换为web可用
        #handleFile(postDir, file, isGit=False) # 将图片路径转换为Typora可用