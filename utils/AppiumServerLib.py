# -*- coding: utf-8 -*-
#author:yanyj
import subprocess,os,time,datetime
import requests


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
        starttime = datetime.datetime.now()
        print starttime
        try:
            #sp = subprocess.Popen('appium >%sappium_run_%s.log'%(appium_log_path,time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))), stdout=subprocess.PIPE,shell=True)
            sp = subprocess.Popen('appium >%s'%(appium_log_path+appium_log_name), stdout=subprocess.PIPE,shell=True)
        except Exception as e:
            print e
            raise "error"
        while (datetime.datetime.now()-starttime).seconds < timeout:
            if self._check_server_status(statusUrl):
                print "Appium server start success, it's now running on %s..." % statusUrl
                return True
            # print 'Wait for Appium server start...'
            time.sleep(1)
        print "Time out, Appium server start on %s fail!" % statusUrl
        return False

    def stop_appium_server(self,statusUrl):
        """
        stop appium server
        :return:True or False
        """
        try:
            p = os.popen('''taskkill /F /IM "node.exe"''')
            time.sleep(3)
            if not self._check_server_status(statusUrl):
                #node is not exist
                print 'Appium server stop success!'
                return True
            else:
                print 'Appium server stop fail!'
                return False        
        except Exception as e:
            print e
            return False


    def _check_server_status(self,statusUrl):
        """Determine whether server is running
        :return:True(runing) or False
        """
        response = None
        try:
            r = requests.get(statusUrl)
            response_json = r.json()
            if response_json['status'] == '0' or str(r.status_code).startswith("2"):
                return True
            else:
                return False
        except Exception as e:
            print "AppiumServer is not start", e
            return False
        finally:
            if response:
                response.close()

    def _check_node_whether_exists(self):
        r = os.popen('''tasklist | find "node.exe"''').readlines()
        print len(r)
        for line in r:
            print line
            if len(r) != 0:
                # print "Node is exist"
                return True #node is exist
            else:
                return False


if __name__=='__main__':
    # appium_run_log_path = "E:\\Test\\AutoTest\\Log\\appium_run_log\\"
    baseurl = "http://localhost:4723/wd/hub/status"
    a = AppiumServerLib()
    print a._check_server_status(baseurl)
    # for i in range(1):
    #     print i
        
    #     if a.start_appium_server(appium_run_log_path,baseurl):
    #         time.sleep(5)
    #         if not a.stop_appium_server(baseurl):
    #             print 'error ,stop appium fail'
    #             raise Exception('error ,stop appium fail')
    #         print "####################################################################"
    #     else:
    #         raise Exception("error,start appium fial")
    #     time.sleep(3)
