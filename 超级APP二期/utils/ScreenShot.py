#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re,time,platform,subprocess

#判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"
    
#判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
    else:
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." %os.environ["ANDROID_HOME"])
    
#adb命令
def adb(args):
    cmd = "%s %s" %(command, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#adb shell命令
def shell(args):
    cmd = "%s shell %s" %(command, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#时间戳
def timestamp():
    return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

#截取当前屏幕，截屏文件保存至当前目录下的screen文件夹中
PATH = lambda p: os.path.abspath(p)

def screenshot():
    # path = PATH("%sScreenShot" %os.getcwd())
    path = PATH("../AutoTest/ScreenShot")

    shell("screencap -p /data/local/tmp/tmp.png").wait()
    if not os.path.isdir(path):
        os.makedirs(path)
        
    adb("pull /data/local/tmp/tmp.png %s" %PATH("%s/%s.png" %(path, timestamp()))).wait()
    shell("rm /data/local/tmp/tmp.png")   

if __name__ == "__main__":
    screenshot()
    print "success"
