# -*- coding: utf-8 -*-  #
#author=yanjy

import subprocess
import time
import ctypes
import sys
import os
from ConfigLib import *



Conf = ConfigLib() 
TH32CS_SNAPPROCESS = 0x00000002
class PROCESSENTRY32(ctypes.Structure):
     _fields_ = [("dwSize", ctypes.c_ulong),
                 ("cntUsage", ctypes.c_ulong),
                 ("th32ProcessID", ctypes.c_ulong),
                 ("th32DefaultHeapID", ctypes.c_ulong),
                 ("th32ModuleID", ctypes.c_ulong),
                 ("cntThreads", ctypes.c_ulong),
                 ("th32ParentProcessID", ctypes.c_ulong),
                 ("pcPriClassBase", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("szExeFile", ctypes.c_char * 260)]

class LogLib():

     def __init__(self):
          self.logpath = Conf.get_option_value('section1','logPath')
          self.Process=None
          self.tags=None
          self.PID=None
          if not os.path.exists(self.logpath):
               print 'the xmlpath is not exists,create it'
               try:
                    os.makedirs(self.logpath)
               except:
                    raise Exception("create file fail,maybe this dir is not exists,please check")
          else:
               print 'the xmlpath %s is exists'%self.logpath
 
     def _getProcList(self):
         CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
         Process32First = ctypes.windll.kernel32.Process32First
         Process32Next = ctypes.windll.kernel32.Process32Next
         CloseHandle = ctypes.windll.kernel32.CloseHandle
         hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
         pe32 = PROCESSENTRY32()
         pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
         if Process32First(hProcessSnap,ctypes.byref(pe32)) == False:
             print >> sys.stderr, "Failed getting first process."
             return
         while True:
             yield pe32
             if Process32Next(hProcessSnap,ctypes.byref(pe32)) == False:
                 break
         CloseHandle(hProcessSnap)
 
     def _getChildPid(self,pid):
         procList = self._getProcList()
         for proc in procList:
             if proc.th32ParentProcessID == pid:
                  yield proc.th32ProcessID
    
     def _killPid(self,pid):
         childList = self._getChildPid(pid)
         for childPid in childList:
             self._killPid(childPid)
         handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
         ctypes.windll.kernel32.TerminateProcess(handle,0)

     def _check_subprocess_status(self,PID):
          cmd1='''tasklist | find "%s"'''%PID
          print cmd1
          r=os.popen(cmd1).readlines()
          for line in r:
               print line
          if len(r)==0:
               print "stop logcat ok"
               return True
          else:
               print "stop logcat fail"
               return False

    
     def start_log(self,logname,device_id=""):
          """
          start the logcat,Log name support Chinese.If it is a single device access,don not need the device_id
          """
          if device_id == "":
               device_id = ""
          else:
               device_id = "-s %s" %device_id
          logname=self.logpath+'\\'+logname.decode('utf-8').encode('gbk')
          logcmd='adb %s shell logcat -v time > %s' % (device_id,logname)
          print logcmd
          self.Process = subprocess.Popen (logcmd,shell=True)
          time.sleep (2)
          self.PID=self.Process.pid
          print "the logcat pid is %s"%(self.PID)
         
     def stop_log(self):
          """
          kill process through the ID to stop grasping the log
          """
          try:
               self._killPid((self.PID))
          except Exception as e:
               print "kill logcat subprocess fail ",e
          finally:
               if not self._check_subprocess_status((self.PID)):
                    self._killPid((self.PID))
         

if __name__ == '__main__':
     deviceid="P4M0215520004561"
     deviceid1="192.168.103.111:5555"
     a=LogLib()
     for i in range(10):
          print i
          name=str(i)+"中过.txt"
          a.start_log(name,deviceid)
          time.sleep(5)
          a.stop_log()
          time.sleep(2)

