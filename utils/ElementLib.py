# -*- coding: utf-8 -*-
#author=yanjy
from xml.dom.minidom import parse
import lxml.etree
import os
import re
from AdbLib import *
from ConfigLib import *


Adb = AdbLib()
Conf = ConfigLib()

class ElementLib(object):
    
    def __init__(self):
        self.xmlpath = Conf.get_option_value('section1','xmlPath')
        self.pattern = re.compile(r"\d+")
        if not os.path.exists(self.xmlpath):
            print 'the xmlpath is not exists,create it'
            try:
                os.makedirs(self.xmlpath)
            except:
                raise Exception("create file fail,maybe this dir is not exists,please check")
        else:
            print 'the xmlpath %s is exists'%self.xmlpath
            
    def _get_all_tags(self,source,nodename):
        source_path=self.xmlpath+'\\'+source
        dom=parse(source_path)
        root = dom.documentElement
        tags=root.getElementsByTagName(nodename)
        return tags
    
    def _decode_string_to_utf8(self,text):
        return text.decode('utf-8')
    
    def _element_should_be(self,source,nodename,attr,attrvalue,flag):
        """
        this function is used to get elment attrbutevalue,such as Attribute of sentence elements,such as if the element is be focused、clicked、enabled、selected...
        """
        element_list=[]
        tags=self._get_all_tags(source,nodename)
        for tag in tags:
            print tag
            if tag.getAttribute(attr)==attrvalue and tag.getAttribute(flag)=="true":
                print "element is %s by %s=%s" % (flag,attr,attrvalue)
                return True
        else:
            print "element is not %s by %s=%s" % (flag,attr,attrvalue)
            return False
    
    def _get_bounds(self,source,nodename,attr,attrvalue):
        
        coord_list=[]
        tags=self._get_all_tags(source,nodename)
        for tag in tags:
            if tag.getAttribute(attr)==attrvalue:
                for i in self.pattern.findall(tag.getAttribute("bounds")):
                    coord_list.append(int(i.encode('utf-8')))
        if len(coord_list)==0:
            raise Exception('get element coodrs fail')
        else:
            return coord_list
            
    def _find_element(self,source,nodename,attr,attrvalue):
        tags=self._get_all_tags(source,nodename)
        for tag in tags:
            if tag.getAttribute(attr)==attrvalue:
                print "find element by %s=%s"%(attr,attrvalue)
                return True
        else:
            error="Error,element is not exits by %s=%s "%(attr,attrvalue)
            print error
            raise Exception("Error,element is not exits")
        
    def _find_element_by_xpath(self,source,xpath):
        source_path=self.xmlpath+'\\'+source
        element=[]
        xpath=self._decode_string_to_utf8(xpath)
        doc = lxml.etree.parse(source_path)
        for node in doc.xpath(xpath):
            for attr in node.items():
                element.append(attr)
        if len(element)>0:
            print len(element)
            print "find element by xpath=%s" %xpath
            return element
        else:
            print "Error,element is not exits by xpath=%s"%xpath
            raise Exception('''"Error,element is not exits by xpath''')
        
    def get_center_coordinate(self,*args):
        Xpoint = (int(args[0][2]) - int(args[0][0])) / 2.0 + int(args[0][0])
        Ypoint = (int(args[0][3]) - int(args[0][1])) / 2.0 + int(args[0][1])
        print Xpoint,Ypoint
        return (Xpoint,Ypoint)
        
    def write_to_file(self,xmlname):
        xmlname=self.xmlpath+'\\'+xmlname
        print xmlname
        if os.path.exists(xmlname):
            print 'xml exists,remove it'
            os.remove(xmlname)
            if os.path.exists(xmlname):
                print 'remove xmlfile fail'
                return False
            else:
                print 'remove xmlfile ok'
        else:
            print 'have no the xml'
        try:
            f=open(xmlname,'w')
            for i in ss:
                f.write(i.encode('utf-8'))
        except:
            raise Exception("open file error")
        finally:
            f.close()
            
    def dump_xml(self,xmlname,device_id=''):
        str1="UI hierchary dumped to: /data/local/tmp/uidump.xml"
        try:
            Adb.excute_shell_command("rm /data/local/tmp/uidump.xml",device_id)
            if str1 in Adb.excute_shell_command("uiautomator dump --compressed /data/local/tmp/uidump.xml",device_id).read():
                print str1
                self._pull_xml_to_pc(xmlname,device_id)
            else:
                print "dump xml fail"
                return False
        except Exception as e:
            print e
            raise ("error,dump xml fail")
        
    def _pull_xml_to_pc(self,xmlname,device_id=''):
        xmlname=self.xmlpath+'\\'+xmlname.decode('utf-8').encode('gbk')
        print xmlname
        if os.path.exists(self.xmlpath)==False:
               print 'the xmlpath is not exists,create it'
               os.makedirs(self.xmlpath)
        if os.path.exists(xmlname):
            print 'xml exists,remove it'
            os.remove(xmlname)
            if os.path.exists(xmlname):
                print 'remove xmlfile fail'
                return False
            else:
                print 'remove xmlfile ok'
        else:
            print 'have no the xml'
        Adb.excute_adb_command("pull data/local/tmp/uidump.xml %s" %xmlname,device_id)
        if os.path.exists(xmlname):
            print 'pull the xmlfile ok'
            return True
        else:
            print 'pull the xmlfile fail'
            return False

    def element_should_be_enabled_by_id(self,source,nodename,resourceid):
        return self._element_should_be(source,nodename,"resource-id",resourceid,"enabled")
    
    def element_should_be_enabled_by_text(self,source,nodename,text):
        text=self._decode_string_to_utf8(text)
        print text
        return self._element_should_be(source,nodename,"text","enabled")

    def element_should_be_selected_by_id(self,source,nodename,resourceid):
        return self._element_should_be(source,nodename,"resource-id",resourceid,"selected")

    def element_should_be_selected_by_text(self,source,nodename,text):
        text=self._decode_string_to_utf8(text)
        print text
        return self._element_should_be(source,nodename,"text",text,"selected")
 
    def element_should_be_checked_by_id(self,source,nodename,resourceid):
        return self._element_should_be(source,nodename,"resource-id",resourceid,"checked")

    def element_should_be_checked_by_text(self,source,nodename,text):
        text=self._decode_string_to_utf8(text)
        print text
        return self._element_should_be(source,nodename,"text",text,"checked")
    
    def element_should_be_focused_by_id(self,source,nodename,resourceid):
        return self._element_should_be(source,nodename,"resource-id",resourceid,"focused")
    
    def element_should_be_focused_by_text(self,source,nodename,text):
        text=self._decode_string_to_utf8(text)
        print text
        return self._element_should_be(source,nodename,"text",text,"focused")
    
    def get_element_bounds_by_class(self,source,nodename,classname):
        """
        get element bounds by classname
        """
        return self._get_bounds(source,nodename,"class",classname)
 
    def get_element_bounds_by_name(self,source,nodename,text):
        text=self._decode_string_to_utf8(text)
        print text
        return self._get_bounds(source,nodename,"text",text)

    def get_element_bounds_by_id(self,source,nodename,resourceid):
        """
        get element bounds by id
        """
        return self._get_bounds(source,nodename,"resource-id",resourceid)
    
    def get_element_bounds_by_xpath(self,source,xpath):
        coord_list=[]
        r=self._find_element_by_xpath(source,xpath)
        print len(r),type(r)
        for attr in r:
            if "bounds" in attr:
                print "find elment bounds by xpath=%s"%xpath
                print str(attr).strip(")").split("'bounds'")[1].strip(',')
                for i in self.pattern.findall(str(attr).strip(")").split("'bounds'")[1].strip(',')):
                    coord_list.append(int(i))
                return coord_list

        else:
            print "cannot find elment bounds by xpath=%s"%xpath
            raise Exception("cannot find elment bounds by xpath")
        
    def find_all_elements_by_same_id(self,source,nodename,resourceid,attr="text"):
        """
        find all elements by same id
        """
        element_list=[]
        tags=self._get_all_tags(source,nodename)
        for tag in tags:
            if tag.getAttribute("resource-id")==resourceid:
                print "find element by resource-id=%s"%resourceid
                element_list.append(tag.getAttribute(attr))
        return element_list

    def find_element_by_xpath(self,source,xpath):
        """
        find elemnt by xpath
        """
        return self._find_element_by_xpath(source,xpath)

    def find_element_by_class(self,source,nodename,classname):
        """
        find element by class
        """
        return self._find_element(source,nodename,"class",classname)

    def find_element_by_id(self,source,nodename,resourceid):
        """
        find element by resource_id
        """
        return self._find_element(source,nodename,"resource-id",resourceid)
    
    def find_element_by_name(self,source,nodename,textname):
        """
        Find element by text name
        """
        textname=self._decode_string_to_utf8(textname)
        return self._find_element(source,nodename,"text",textname)
 
    def find_element_by_contentdesc(self,source,nodename,contentdesc):
        """
        Find element by text content-desc
        """
        contentdesc=self._decode_string_to_utf8(contentdesc)
        return self._find_element(source,nodename,"content-desc",contentdesc)


if __name__=='__main__':
    aa=ElementLib()
    '''aa.dump_xml('huawei_home1.xml')
    r=aa.get_element_bounds_by_id("more_task.xml","android.widget.TextView","com.changhong.system.app.task:id/content")
    print type(r),len(r)
    for i in r:
        print i
    r1=aa.get_element_bounds_by_name("more_task.xml","android.widget.TextView","上方向键:清除任务")
    print r1,len(r1)
    for i in r1:
        print i
    r2=aa.get_element_bounds_by_class("more_task.xml","android.widget.TextView","android.widget.TextView")
    print r2
    for i in r2:
        print i
    r3=aa.find_element_by_name("more_task.xml","android.widget.TextView","数字电视")
    print r3
    r4=aa.find_element_by_id("more_task.xml","android.widget.TextView","com.changhong.system.app.task:id/text04")
    print r4
    r5=aa.find_element_by_class("more_task.xml","android.widget.FrameLayout","android.widget.FrameLayout")
    print r5
    #r6=aa.find_element_by_contentdesc("more_task.xml","android.widget.TextView","数字电视")
    r7=aa.find_all_elements_by_same_id("wifiscan.xml","node","com.changhong.easysetting:id/text_item")
    for i in r7:
        print i
    r8=aa.find_element_by_xpath("22.xml","//system/patch/info[@version = '7.00003']")
    #print r8'''
    r9=aa.get_element_bounds_by_xpath("more_task.xml","//android.widget.RelativeLayout[1]/android.widget.TextView[1][@resource-id = 'com.changhong.system.app.task:id/content']")
    for i in r9:
        print i,type(i)
    print len(r9),type(r9)
    aa.get_center_coordinate(r9)
    '''aa.element_should_be_focused_by_text("more_task.xml","android.widget.RadioButton","上方向键:清除任务")
    aa.element_should_be_focused_by_id("tengxunmusic.xml","android.widget.ImageButton","com.ktcp.music:id/player_btn_play")
    print "##########################################################"
    #a=aa.Get_ResourseID_AttributeValue('E:\\AppiumAutoTest\\AndoridTVAutoTest\\xml\\DTV_dump.xml',"com.changhong.tvos.dtv:id/title","浙江卫视",'selected')
    #print str(a)
    #print a
    #if a=="true":
        #print 'pass，，，浙江卫视被选中了'
    #else:
        #print 'fail,,,浙江卫视没有被选中'
        
    print "##########################################################"
    b=aa.element_should_be_focused_by_text("more_task.xml","android.widget.RadioButton","HDMI3")
    print b
    c=aa.find_all_elements_by_same_id("DTV_dump.xml","com.changhong.tvos.dtv:id/title",'text')
    for i in c:
        print i

    print "##########################################################"'''
 
    

