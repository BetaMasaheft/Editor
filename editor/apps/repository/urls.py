from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.base_view, name='base'),
        #url(r'^(?P<repository_name>\w+)/$', views.repository_contents, name='repository_contents'),
        ]
