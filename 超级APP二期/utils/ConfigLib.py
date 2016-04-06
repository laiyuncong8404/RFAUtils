# -* - coding: UTF-8 -* -
#author:yanjy
__doc__ = """you can use 'configobj' Module more easier for Reading and Writing Config Files.
setup by run 'pip install configobj' in command line.
"""

import os,ConfigParser

class ConfigLib():
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.config_path = os.path.abspath('.') + "\\config.conf"
    
    def _read_config(self):
        return self.conf.read(self.config_path)

    def _write_to_config(self):
        self.conf.write(open(self.config_path,"w"))

    def _check_file_exists(self,pathname):
        if not os.path.exists(pathname):
            print 'The "%s" is Not exists,create it now …'% pathname
            try:
                os.makedirs(pathname)
            except:
                raise Exception("create file fail, maybe this path is not exists,please check!")
        else:
            print 'The path of "%s" is exist.' % pathname
        
    def check_file_weather_exists(self,xml_path,log_path,appium_run_log_path,picspath,picdpath):
        self._check_file_exists(xml_path)
        self._check_file_exists(log_path)
        self._check_file_exists(appium_run_log_path)
        self._check_file_exists(picspath)
        self._check_file_exists(picdpath)    

    def get_all_sections(self):
        self._read_config()
        return self.conf.sections()

    def get_option_value(self,section,option):
        '''
        get the option vlaue from config file
        :return:the option value
        '''
        self._read_config()
        return self.conf.get(section,option)
    
    def update_option_value(self,section,option,value):
        """update the option value."""
        self._read_config()
        self.conf.set(section,option,value)
        self._write_to_config()
        # return self.conf.get(section,option)

    def write_option_value(self,section,option,value):
        self._read_config()
        self.conf.set(section,option,value)
        self._write_to_config()
        # return self.conf.get(section,option)

    def add_section(self,section,option,value):
        """Create a new section in the configuration."""
        self._read_config()
        self.conf.add_section(section)
        self.conf.set(section,option,value)
        self._write_to_config()
        # return self.conf.sections()
    
    def remove_option(self,section,option):
        """Remove an option."""
        self._read_config()
        self.conf.remove_option(section,option)
        self._write_to_config()
    
    def remove_section(self,section):
        """Remove a file section."""
        self._read_config()
        self.conf.remove_section(section)
        self._write_to_config()
    
if __name__=='__main__':
    r = ConfigLib()
    print 'get all sections:', r.get_all_sections()
    print 'get statusUrl value:', r.get_option_value('section1','statusUrl')
    print 'add section2:', r.add_section('section2','age','26')
    print 'get all sections:', r.get_all_sections()
    print 'get age value of section2:', r.get_option_value('section2','age')
    print 'update age value:', r.update_option_value('section2','age','31')
    print 'remove option age:', r.remove_option('section2','age')
    print 'remove section2:', r.remove_section('section2')