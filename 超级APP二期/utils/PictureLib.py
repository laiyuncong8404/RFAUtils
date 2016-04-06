# -*- coding: utf-8 -*-
import Image
import os

class PictureLib():
    """
    基于分块的直方图相似算法
    """
    def __init__(self):
        pass

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
    
    def _excute_shell_command(self,args,device_id=""):
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
    
    def _excute_adb_command(self,args,device_id=""):
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
        
    def _calc_similar(self,li, ri):
        return sum(self._hist_similar(l.histogram(), r.histogram()) for l, r in zip(self._split_image(li), self._split_image(ri))) / 16.0

    def picture_cmp(self,spath,lf,dpath,rf):
        li, ri = self._make_regalur_image(self._load_img(spath+lf)), self._make_regalur_image(self._load_img(dpath+rf))
        return self._calc_similar(li, ri)
        
    def screen_capture(self,dpath,pic_name,device_id=''):
        self._excute_shell_command("screencap -p /data/local/tmp/temp.png",device_id)
        self._excute_adb_command("pull /data/local/tmp/temp.png %s" %(dpath+pic_name),device_id)
        self._excute_shell_command("rm -p /data/local/tmp/temp.png",device_id)
                
    def get_sub_image(self,dpath,source_imgname,sub_imgname,coord):
        image = self._load_img(dpath+source_imgname)
        newImage = image.crop(coord)
        newImage.save(dpath+sub_imgname)
                
        
if __name__ == '__main__':
    Spath="E:\\Test\\AutoTest\\Pic\\Spath\\"
    Dpath="E:\\Test\\AutoTest\\Pic\\Dpath\\"
    coods=[223,99,434,385]
    coods1=[12,99,223,385]
    a=PictureLib()
    r1= a.picture_cmp(Spath,'1.jpg',Dpath,'2.png')
    print r1
    if r1<1:
        print "buyiyang"
    print a.picture_cmp(Spath,'11.jpg',Dpath,'22.jpg')

    
    r2= a.picture_cmp(Spath,'111.jpg',Dpath,'222.jpg')
    if r2==1:
        print "yiyang"
    print a.picture_cmp(Spath,'1111.jpg',Dpath,'2222.jpg')
    print a.picture_cmp(Spath,'11111.jpg',Dpath,'22222.jpg')
    print a.picture_cmp(Spath,'111111.jpg',Dpath,'222222.jpg')
    a.screen_capture(Dpath,'huawei_home123.png')
    a.get_sub_image(Dpath,"huawei_home.png","huawei_home_media.png",coods)
    a.get_sub_image(Dpath,"huawei_home.png","huawei_home_music.png",coods1)
    #a.get_sub_image(Dpath,"huawei_home.png","huawei_home_hueweistore.png",coods2)



