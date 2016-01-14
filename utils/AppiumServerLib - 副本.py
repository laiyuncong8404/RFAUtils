# -*- coding: utf-8 -*-
#author:yanyj
import urllib
import subprocess
import time
import datetime
import os


class AppiumServerLib():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass

    def start_appium_server(self,appium_log_path,appium_log_name,statusUrl,timeout = 20):
        """
        start appium server
        :return:True or False
        """
        if self._check_server_status(statusUrl):
            self.stop_appium_server(statusUrl)   
        starttime=datetime.datetime.now()
        print starttime
        try:
            #sp = subprocess.Popen('appium >%sappium_run_%s.log'%(appium_log_path,time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))), stdout=subprocess.PIPE,shell=True)
            sp = subprocess.Popen('appium >%s'%(appium_log_path+appium_log_name), stdout=subprocess.PIPE,shell=True)
        except Exception as e:
            print e
            raise "error"
        while (datetime.datetime.now()-starttime).seconds < timeout:
            if self._check_server_status(statusUrl):
                print 'start appium server ok'
                return True
            print 'wait for appium server start'
            time.sleep(1)
        print "time out,start appium server is fail"
        return False

    def stop_appium_server(self,statusUrl):
        """
        sop appium server
        :return:True or False
        """
        try:
            p = os.popen('TASKKILL /F  /IM node.exe')
            if not self._check_server_status(statusUrl):
                print 'stop appium server ok'
                return True
            else:
                print 'stop appium server fail'
                return False        
        except Exception as e:
            print e
            return False


    def _check_server_status(self,statusUrl):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        try:
            response = urllib.urlopen(statusUrl)
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
    appium_run_log_path = "E:\\Test\\AutoTest\\Log\\appium_run_log\\"
    baseurl="http://localhost:4723/wd/hub/status"
    a=AppiumServerLib()
    for i in range(1):
        print i
        
        if a.start_appium_server(appium_run_log_path,baseurl):
            time.sleep(5)
            if not a.stop_appium_server(baseurl):
                print 'error ,stop appium fail'
                raise Exception('error ,stop appium fail')
            print "####################################################################"
        else:
            raise Exception("error,start appium fial")
        time.sleep(3)
