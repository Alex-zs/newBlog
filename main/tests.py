from django.test import TestCase
from .qcloud import qcouldCos

img_url = '/media/article_img/20180802171217_31FzuQI7D9gT4rgJnp.jpeg'

qcloudCos('..'+img_url,img_url)

# Create your tests here.
