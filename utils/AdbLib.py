# -*- coding: utf-8 -*-  #
#author=yanjy
import os
import time
import re

class AdbLib():

    def __init__(self):

        self.device_list=[]

    def excute_adb_command(self,args,device_id=""):
        """
        excute adb command
        if only one device,don not need the device_id.
        directs command to the device or emulator with the given serial number or qualifier. Overrides ANDROID_SERIAL environment variable.
        """
        if device_id == "":
            device_id = ""
        else:
            device_id = "-s %s" %device_id
        cmd = "adb %s %s" % (device_id, str(args))
        print cmd
        return os.popen(cmd)

    def excute_shell_command(self,args,device_id):
        """
        ecxute shell command
        if only one device,don not need the device_id.
        directs command to the device or emulator with the given serial number or qualifier. Overrides ANDROID_SERIAL environment variable.
        """
        if device_id == "":
            device_id = ""
        else:
            device_id = "-s %s" %device_id
        cmd = "adb %s shell %s" % (device_id, str(args))
        print cmd
        return os.popen(cmd)
    
    def connect_device_by_ip(self,ip):
        """
        connect to a device via TCP/IP
        Port 5555 is used by default if no port number is specified.
        """
        self.restart_adb_server()
        rr=self.excute_adb_command("connect %s" %ip).read()
        print rr
        if 'connected' in rr:
            print "connect device ok"
            return True
        if rr=='':
            print "adb error,need to check it"
            return None
        else:
            print "connect device fail"
            return False

    def shell_should_be_open(self,device_id=""):
        """
        Confirm that shell has been turned on
        """
        for i in range(10):
            if len(self.excute_shell_command("ls",device_id).readlines())>1:
                print 'go to shell ok'
                return True
        else:
            raise Exception("go to shell fail")

    def get_devices_status(self,device_id=""):
        """
        get devices status：
        return:offline | bootloader | device | ''
        """
       	try:
       		assert self.excute_adb_command("get-state",device_id).read().strip() == "device"
       	except AssertionError:
       		raise AssertionError ("Error! no device connected.")
       	else:
       		pass

    def get_devices_id(self,device_id=""):
        """
        get devices id，return serialNo
        """
        device_list=[]
        for device in self.excute_adb_command("get-serialno",device_id).readlines():
            device_list.append(device.strip().split("\t")[0])
        if len(device_list)>0:
            for device in device_list:
                print device
                if "daemon" not in device and "unknown" not in device:
                    return device
                if "unknown" in device:
                    raise Exception("No device connected error!")
        else:
            raise Exception("adb error, need to reatsrt adb server.")

    def get_all_connected_devices(self,device_id=""):
        """
        list all connected devices
        """
        device_list=[]
        device_list1=[]
        for device in self.excute_adb_command("devices",device_id).readlines():
                device_list.append(device.strip().split("\t")[0])
        if len(device_list)>0:
            for device in device_list:
                print device
                if "daemon" not in device and "unknown" not in device and "List of devices attached" not in device:
                    device_list1.append(device)
                if "unknown" in device:
                    raise Exception("No device connected error!")
            return device_list1[:-1]
        else:
            raise Exception("adb error, need to reatsrt adb server.")

#新增
    def get_platformName(self,device_id=""):
        """
        "return Android platformName, eg:Android"
        """
        platformName = []
        platformName = self.excute_shell_command("getprop net.bt.name",device_id).read().strip()
        return platformName

    def get_platformVersion(self,device_id=""):
        """
        "return Android PlatformVersion, eg:4.4.4"
        """
        AndroidVersion = []
        AndroidVersion = self.excute_shell_command("getprop ro.build.version.release",device_id).read().strip()
        return AndroidVersion

    def get_platformLevel(self,device_id=""):
        """
        "return Android PlatformLevel, eg:19"
        """
        APILevel = []
        APILevel = self.excute_shell_command("getprop ro.build.version.sdk",device_id).read().strip()
        return APILevel
    
    def _kill_adb_server(self):
        """
        kill the server if it is running
        """
        self.excute_adb_command("kill-server")

    def _start_adb_server(self):
        """
        ensure that there is a server running
        """
        self.excute_adb_command("start-server")

    def restart_adb_server(self):
        """
        restart the adb server
        """
        self._kill_adb_server()
        self._start_adb_server()

    def get_focused_package_and_activity(self,device_id=""):
        """
        Gets the package name of the current application interface and Activity
        #return:packageName/activityName
        """
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.excute_shell_command("dumpsys window w | findstr \/ | findstr name=",device_id).read()
        return pattern.findall(out)[0]

    def get_current_packagename(self,device_id=""):
        """
        Gets the package name for the current application
        """
        return self.get_focused_package_and_activity(device_id).split("/")[0]

    def get_current_activity(self,device_id=""):
        """
        Gets the activity for the current application
        """
        return self.get_focused_package_and_activity(device_id).split("/")[-1]
    
    def get_app_start_totaltime(self, component,device_id=""):
        """
        Get the time to start the application
        """
        time = self.excute_shell_command("am start -W %s | findstr TotalTime" %(component),device_id).read().split(": ")[-1]
        return int(time)

    def send_keyevent(self,keycode,device_id=""):
        """
        By sending keycode analog buttons
        """
        self.excute_shell_command("input keyevent %s" %str(keycode),device_id)

    def long_press_keyevent(self,keycode,device_id=""):
        """
        Through the simulation of long press button to send keycode
        """
        self.excute_shell_command("input keyevent --longpress %s" %str(keycode),device_id)

    def touch_by_XYpoint(self,Xpoint,Ypoint,device_id=""):
        """
        Touch screen according to coordinate values
        """
        self.excute_shell_command("input tap %s %s" %(str(Xpoint),str(Ypoint)),device_id)

    def swipe_by_XYpoint(self, start_Xpoint, start_Ypoint, end_Xpoint, end_Ypoint, device_id="",duration=" "):
        """
        Sliding event, Android 4.4 or more optional duration (MS)
        usage: swipe(800, 500, 200, 500)
        """
        self.excute_shell_command(("input swipe %s %s %s %s %s" % (str(start_Xpoint), str(start_Ypoint), str(end_Xpoint), str(end_Ypoint), str(duration))),device_id)

    def getScreenResolution(self,device_id):
        """
        Get device screen resolution，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.excute_shell_command("dumpsys display | findstr PhysicalDisplayInfo",device_id).read()
        display = pattern.findall(out)
        for i in (int(display[0]), int(display[1])):
            print i
        return (int(display[0]), int(display[1]))

    def swipeByRatio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh,device_id, duration=" "):
        """
        Android 4.4 or more optional duration (MS) by the ratio of the transmission sliding event.
        """
        self.excute_shell_command("input swipe %s %s %s %s %s" % (str(start_ratioWidth * self.getScreenResolution(device_id)[0]), str(start_ratioHigh * self.getScreenResolution(device_id)[1]), \
                                             str(end_ratioWidth * self.getScreenResolution(device_id)[0]), str(end_ratioHigh * self.getScreenResolution(device_id)[1]), str(duration)),device_id)
        time.sleep(0.5)
        
    def swipe_to_left(self,device_id=""):
        """
        Left sliding screen
        """
        self.swipeByRatio(0.8, 0.5, 0.2, 0.5,device_id)

    def swipe_to_right(self,device_id=""):
        """
        Right sliding screen
        """
        self.swipeByRatio(0.2, 0.5, 0.8, 0.5,device_id)

    def swipe_to_up(self,device_id=""):
        """
        Up sliding screen
        """
        self.swipeByRatio(0.5, 0.8, 0.5, 0.2,device_id)

    def swipe_to_down(self,device_id=""):
        """
        Down sliding screen
        """
        self.swipeByRatio(0.5, 0.2, 0.5, 0.8,device_id)

    def send_text(self, string,device_id=""):
        """
        Send a text, can only contain English characters and spaces, more than a single space
        usage: sendText("i am unique")
        """
        self.excute_shell_command("input text %s" % string,device_id)

    def getSystemAppList(self,device_id=""):
        """
        A list of system application packages installed in the device
        """
        sysApp = []
        for packages in self.excute_shell_command("pm list packages -s",device_id).readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp

    def getThirdAppList(self,device_id=""):
        """
        A list of third party application packages installed in the device
        """
        thirdApp = []
        for packages in self.excute_shell_command("pm list packages -3",device_id).readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp
    
    def getMatchingAppList(self, keyword,device_id=""):
        """
        Fuzzy query and keyword matching application package name list
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.excute_shell_command("pm list packages | findstr %s" % keyword,device_id).readlines():
            matApp.append(packages.split(":")[-1].splitlines()[0])

        return matApp

    def installApp(self, appFile,device_id=""):
        """
        Install app, APP name can not contain Chinese characters
        """
        self.excute_adb_command("install %s" % appFile,device_id)
        
    def isInstall(self, packageName,device_id=""):
        """
        To determine whether the application is installed, has been installed to return True, otherwise it returns False
        """
        if self.getMatchingAppList(packageName,device_id):
            return True
        else:
            return False

    def remove_app(self, packageName,device_id=""):
        """
        remove app
        """
        self.excute_adb_command("uninstall %s" % packageName,device_id)

    def clearAppData(self, packageName,device_id=""):
        """
        Clear application user data
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.excute_shell_command("pm clear %s" % packageName,device_id).read().splitlines():
            return True
        else:
            return False

    def resetCurrentApp(self,device_id=""):
        """
        Reset current application
        """
        packageName = self.get_current_packagename(device_id)
        component = self.get_focused_package_and_activity(device_id)
        self.clearAppData(packageName,device_id)
        self.start_activity(component,device_id)

    def stop_app(self, packageName,device_id=""):
        """
        stop app
        """
        self.excute_shell_command("am force-stop %s" % packageName,device_id)

    def start_activity(self, component,device_id=""):
        """
        start a activity
        usage: start_activity("com.android.settinrs/.Settings")
        """
        self.excute_shell_command("am start -n %s" % component,device_id)
        
    def start_service(self,component,device_id=""):
        """
        Start a service
        usege:start_service(com.changhong.easysetting/.MainService)
        """
        self.excute_shell_command("am startservice %s" % component,device_id)
        
    def send_broadcast(self,bradcast_action,device_id=""):
        """
        send a broadcast
        """
        self.excute_shell_command("am broadcast -a %s" % bradcast_action,device_id)



if __name__ == '__main__':
    # qqapp="com.ktcp.music/.MusicTV"
    # deviceid="P4M0215520004561"
    # deviceid1="192.168.103.109:5555"
    a = AdbLib()
    a.get_platformVersion()
    # a.get_devices_status()
    # a.get_focused_package_and_activity()
    # a.get_current_packagename()
    # a.get_current_activity()



"""
    for i in range(1):
        print i
        #a.connect_device_by_ip('192.168.103.109')
        #time.sleep(3)
        #a.shell_should_be_open(deviceid1)
        print "*********************************************************************"
        a.connect_device_by_ip('192.168.103.111')
        print "*********************************************************************"
        print a.get_all_connected_devices()
        print "*********************************************************************"
        print a.get_devices_status(deviceid)
        print "*********************************************************************"
        print a.get_devices_status(deviceid1)
        print "*********************************************************************"
        print a.get_devices_id(deviceid)
        print "*********************************************************************"
        print a.get_devices_id(deviceid1)
        print "*********************************************************************"
        time.sleep(3)'''
        print "*********************************************************************"
        print a.get_focused_package_and_activity(deviceid)
        #print a.get_focused_package_and_activity(deviceid)
        #print a.get_focused_package_and_activity()
        #print a.get_current_packagename(deviceid1)
        #print a.get_current_activity(deviceid1)
        #print a.get_current_packagename()
        #print a.get_current_activity()
        #print a.get_app_start_totaltime(qqapp,deviceid1)
        #a.send_keyevent(4)
        #a.send_keyevent(4124,deviceid1)
        #time.sleep(3)
        #a.long_press_keyevent(82,deviceid1)
        #a.touch_by_XYpoint(500,100,deviceid1)
        #a.swipe_by_XYpoint(200,750,500,750,deviceid)
        #a.swipe_to_left(deviceid)
        #a.swipe_to_right(deviceid)
        #a.swipe_to_up()
        #a.swipe_to_down()
        #a.send_text('33333333')
        #a.send_text('5555brr',deviceid1)
        for i in a.getSystemAppList(deviceid):
            print i
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #for i in a.getSystemAppList(deviceid1):
            #print i
        #for i in a.getThirdAppList(deviceid):
            #print i
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        for i in a.getThirdAppList(deviceid):
            print i
        print a.getMatchingAppList('com.ktcp.music')
        #print a.getMatchingAppList('yunpan',deviceid)
        #a.installApp("D:\\Tool\\shafa.market.apk")
        #a.installApp("D:\\Tool\\Dangbei.apk",deviceid1)
        #print a.isInstall("com.ktcp.music")
        #a.start_activity("com.ktcp.music/.MusicTV",deviceid1)
        #a.start_service("com.changhong.easysetting/.MainService")
        #a.resetCurrentApp(deviceid1)
        #a.remove_app("com.dangbeimarket")
        #a.send_broadcast("android.net.conn.CONNECTIVITY_CHANGE")
        #a.send_broadcast("com.changhong.dmt.system.usb.unmounted")
        #a.send_broadcast("com.changhong.dmt.system.usb.mounted")
        print a.get_all_connected_devices()
        print "*********************************************************************"
"""