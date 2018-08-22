from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^&back/$',back_views),
	url(r'^&rank/(\w+)/$',rank_views),
	url(r'^&info/(\w+)/$',info_views),
	url(r'^(\w+)/$',name_views),
	url(r'^\w+/\w+',error_views),
]