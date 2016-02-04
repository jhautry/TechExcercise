from django.conf.urls import patterns, url
from reportCard import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<c_id>\d+)/$', views.assignList, name='assignList'),

)
