# -* - coding: UTF-8 -* -
#author:yanjy
import ConfigParser
import os

class ConfigLib():
    def __init__(self):
        self.conf=ConfigParser.ConfigParser()
        self.config_path=os.path.abspath('.')+ "\\config.conf"
    def _read_config(self):
        return self.conf.read(self.config_path)

    def _write_to_config(self):
        self.conf.write(open(self.config_path,"w"))
        
    def get_option_value(self,section,option):
        '''
        get the option vlaue from config file
        :return:the option value
        '''
        self._read_config()
        return self.conf.get(section,option)
    
    def update_option_value(self,section,option,value):
        '''
        update the option value
        '''
        self._read_config()
        self.conf.set(section,option,value)
        self._write_to_config()

    def write_option_value(self,section,option,value):
        self._read_config()
        self.conf.set(section,option,value)
        self._write_to_config()

    def add_section(self,section,option,value):
        self._read_config()
        self.conf.add_section(section)
        self.conf.set(section,option,value)
        self._write_to_config

    def get_all_sections(self):
        self._read_config()
        return self.conf.sections()
    
if __name__=='__main__':
    r=ConfigLib()
    print r.get_option_value('section1','baseUrl')
    r.add_section("section4","age",'26')
    print r.get_all_sections()
    print r.get_option_value('section3','age')
    r.write_option_value('section3','age1','44')
    print r.get_option_value('section3','age1')
    r.update_option_value('section3','age1','45')
    print r.get_option_value('section3','age1')
    r.update_option_value('section2','name','hy')



