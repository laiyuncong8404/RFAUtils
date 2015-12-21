# -*- coding: utf-8 -*-  #
#author=yanjy
import serial
import time
import sys
import os
import re

from ConfigLib import *

Conf = ConfigLib()

class SerialLib():
    def __init__(self):
        self.ser = None
        self.ser_tag=None
        self.port = Conf.get_option_value('section1','com')
        self.baudrate = int(Conf.get_option_value('section1','baud'))
        print self.port
        print self.baudrate
        
    def open_ser(self,time_out=2):
        self.ser = serial.Serial(port=self.port,baudrate=self.baudrate,timeout=time_out)
        self.ser.write('\r')
        if self.ser.isOpen():
            print "open ser ok"
            return True
        else:
            raise SerialException("could not open port")
            
    def login_ser(self):
        self.excute_command('\r')
        r=self.read_ser()
        if "shell@ChangHong:/" in r:
            print "not need password......"
            self.ser_tag=True
        if "Password:" in r:
            print "need the password......"
            self.excute_command("smart_ch")
            if "shell@ChangHong:/" in self.read_ser():
                print "login successful"
                self.ser_tag=True
            else:
                print "login fail"
        print "the ser_tag is %s"%(self.ser_tag)
        if self.ser_tag==True:
            return True
        else:
            return False    
            
    def excute_command(self,cmd):
        cmd=cmd+'\r'
        self.ser.write(cmd)

    def read_ser(self):
        return self.ser.read(4096)
    
    def close_ser(self):
        self.ser.close()

    def start_tv_adb_server(self):
        try:
            self.open_ser()
            self.login_ser()
            self.excute_command("su")
            self.excute_command("busybox")
            self.excute_command("start adbd")
        finally:
            self.close_ser()
            
    def _get_tv_eth0_ipaddress(self):
        try:
            self.open_ser()
            self.excute_command('''busybox ifconfig eth0 | grep "inet addr:"''')
            r=self.read_ser()
            if "inet addr:" in r and "Mask:" in r and "inet addr:192.168.43.1  Bcast:192.168.43.255" not in r:
                return r
        finally:
            self.close_ser()

    def _get_tv_wlan0_ipaddress(self):
        try:
            self.open_ser()
            self.excute_command('''busybox ifconfig wlan0 | grep "inet addr:"''')
            r=self.read_ser()
            if "inet addr:"in r and "Mask:" in r:
                print r
                return r
        finally:
            self.close_ser()

    def _split_ipaddress(self,s):
        r=re.search(r'inet addr:(\d){1,3}.(\d){1,3}.(\d){1,3}.(\d){1,3}',s)
        if r:
            ip_address=r.group().split(":")[1]
            print "the tv ipaddress is %s "%ip_address
            return ip_address
        else:
            raise Exception("error,coud not get ip address")

    def _get_tv_interface(self):
        try:
            self.open_ser()
            self.excute_command('''busybox ifconfig wlan0 | grep "inet addr"''')
            if "inet addr:192.168.43.1  Bcast:192.168.43.255" in self.read_ser():
                print 'interface is eth0,wifi hot is open'
                return 2
            else:
                s.excute_command('''busybox ifconfig | grep "wlan0"''')
                r=s.read_ser()
                if "wlan0" in r and "Link encap" in r:
                    print 'interface is wlan0'
                    return 1
                else:
                    print "interface is eth0"
                    return 2
        finally:
            self.close_ser()
        
    def get_tv_ipaddress(self):
        ifname=self._get_tv_interface()
        if ifname==1:
            tt=self._get_tv_wlan0_ipaddress()
            if tt!=None:
                tvip=self._split_ipaddress(tt)
                print 'ip is %s '%tvip
        if ifname==2:
            tt=self._get_tv_eth0_ipaddress()
            if tt!=None:
                tvip=self._split_ipaddress(tt)
                print 'ip is %s '%tvip
        return tvip

    def reboot_tv(self):
        try:
            self.open_ser()
            self.login_ser()
            self.excute_command("reboot")
        finally:
            self.close_ser()

if __name__=="__main__":
    s=SerialLib()
    for i in range(10):
        print "执行第%s次"%i
        s.start_tv_adb_server()
        s.get_tv_ipaddress()
        s.reboot_tv()
        time.sleep(150)










    
