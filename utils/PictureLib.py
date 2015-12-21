# -*- coding: utf-8 -*-
import Image
from ConfigLib import *
from AdbLib import *
from ElementLib import *

Adb = AdbLib()
Conf = ConfigLib()
Element = ElementLib()

class PictureLib():
    """
    基于分块的直方图相似算法
    """
    def __init__(self):
            self.spath=Conf.get_option_value('section1','picSpath')
            self.dpath=Conf.get_option_value('section1','picDpath')

    def _load_img(self,imgname):
            if os.path.isfile(imgname):
                    load = Image.open(imgname)
                    return load
            else:
                raise Exception("image is not exist")

    def _make_regalur_image(self,img, size = (256, 256)):
            return img.resize(size).convert('RGB')

    def _split_image(self,img, part_size = (64, 64)):
            w, h = img.size
            pw, ph = part_size
            assert w % pw == h % ph == 0
            return [img.crop((i, j, i+pw, j+ph)).copy() for i in xrange(0, w, pw) for j in xrange(0, h, ph)]

    def _hist_similar(self,lh, rh):
            assert len(lh) == len(rh)
            return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
        
    def _calc_similar(self,li, ri):
            return sum(self._hist_similar(l.histogram(), r.histogram()) for l, r in zip(self._split_image(li), self._split_image(ri))) / 16.0

    def picture_cmp(self,lf, rf):
            li, ri = self._make_regalur_image(self._load_img(self.spath+lf)), self._make_regalur_image(self._load_img(self.dpath+rf))
            return self._calc_similar(li, ri)
        
    def screen_capture(self,pic_name,device_id=''):
            Adb.excute_shell_command("screencap -p /data/local/tmp/temp.png",device_id)
            Adb.excute_adb_command("pull /data/local/tmp/temp.png %s" %(self.dpath+pic_name),device_id)
            Adb.excute_shell_command("rm -p /data/local/tmp/temp.png",device_id)
                
    def get_sub_image(self,source_imgname,sub_imgname,coord):
            image = self._load_img(self.dpath+source_imgname)
            newImage = image.crop(coord)
            newImage.save(self.dpath+sub_imgname)
                
        
if __name__ == '__main__':
    coods=[223,99,434,385]
    coods1=[12,99,223,385]
    coods2=Element.get_element_bounds_by_name("huawei_home.xml","node","华为商城")
    print coods2
    a=PictureLib()
    r1= a.picture_cmp('1.jpg','2.png')
    print r1
    if r1<1:
        print "buyiyang"
    print a.picture_cmp('11.jpg','22.jpg')

    
    r2= a.picture_cmp('111.jpg','222.jpg')
    if r2==1:
        print "yiyang"
    print a.picture_cmp('1111.jpg','2222.jpg')
    print a.picture_cmp('11111.jpg','22222.jpg')
    print a.picture_cmp('111111.jpg','222222.jpg')
    a.screen_capture('huawei_home1.png')
    a.get_sub_image("huawei_home.png","huawei_home_media.png",coods)
    a.get_sub_image("huawei_home.png","huawei_home_music.png",coods1)
    a.get_sub_image("huawei_home.png","huawei_home_hueweistore.png",coods2)



