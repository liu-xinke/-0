from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^1/$',help_1_views),
    url(r'^2/$',help_2_views),
    url(r'^3/$',help_3_views),
    url(r'^4/$',help_4_views),
    url(r'^5/$',help_5_views),
    url(r'^[\s\S]*/$',redirect_views),
]
