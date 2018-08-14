from django.conf.urls import url, include
from .views import *

urlpatterns = [
	url(r'^$',index),
	url(r'^about/',about),
	url(r'^detail/(?P<pk>[0-9]+)/$',detail),
	url(r'photo/$',photo),
	url(r'diary/$',diary),
	url(r'checkout/$',checkout),
]