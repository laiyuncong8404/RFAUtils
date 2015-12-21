# -*- coding: utf-8 -*-
#author:yanyj
import urllib
import subprocess
import time
import datetime
import os
from ConfigLib import *


Conf=ConfigLib()

class AppiumServerLib(object):

    def __init__(self):
        self.statusUrl=Conf.get_option_value('section1','statusUrl')

    def start_appium_server(self,timeout = 20):
        """
        start appium server
        :return:True or False
        """
        if self._check_server_status():
            self.stop_appium_server()   
        starttime=datetime.datetime.now()
        try:
            sp = subprocess.Popen('appium', stdout=subprocess.PIPE,shell=True)
        except Exception as e:
            print e
            raise "error"
        while (datetime.datetime.now()-starttime).seconds < timeout:
            if self._check_server_status():
                print 'start appium server ok'
                return True
            print 'wait for appium server start'
            time.sleep(1)
        print "time out,start appium server is fail"
        return False

    def stop_appium_server(self):
        """
        sop appium server
        :return:True or False
        """
        try:
            p = os.popen('TASKKILL /F  /IM node.exe')
            if not self._check_server_status():
                print 'stop appium server ok'
                return True
            else:
                print 'stop appium server fail'
                return False        
        except Exception as e:
            print e
            return False


    def _check_server_status(self):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        try:
            response = urllib.urlopen(self.statusUrl)
            if '''"status":0''' in response.read() or str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except Exception as e:
            print "AppiumServer not start",e
            return False
        finally:
            if response:
                response.close()

    def _check_node_whether_exists(self):
        r=os.popen('''tasklist | find "node.exe"''').readlines()
        print len(r)
        for line in r:
            print line
        if len(r)==0:
            print "stop appium ok"
            return True
        else:
            print "stop appium fail"
            return False
            
        


if __name__=='__main__':
    a=AppiumServerLib()
    for i in range(50):
        print i
        
        if a.start_appium_server():
            time.sleep(5)
            if not a.stop_appium_server():
                print 'error ,stop appium fail'
                raise Exception('error ,stop appium fail')
            print "####################################################################"
        else:
            raise Exception("error,start appium fail")
        time.sleep(3)
