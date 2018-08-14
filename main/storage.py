# -*- coding: UTF-8 -*-
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ImageStorage(FileSystemStorage): 
    from django.conf import settings 
    def __init__(self, location=settings.MEDIA_ROOT,   base_url=settings.MEDIA_URL): 
        super(ImageStorage, self).__init__(location, base_url)
    # 重写 _save方法  
    def _save(self, name, content): 
        import os, time, random
        # 文件扩展名 
        ext = os.path.splitext(name)[1] 
        # 文件目录 
        d = os.path.dirname(name) 
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S') 
        fn = fn + '_%d'  % random.randint(0,100)
        sa = []
        #加入16位随机字符串
        for i in range(16):
            sa.append(random.choice(seed))
        fn += ''.join(sa)
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        a = super(ImageStorage, self)._save(name, content)
        return a

