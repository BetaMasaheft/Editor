from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.base_view, name='base'),
        url(r'^(?P<repository_name>\w+)/$', views.xml_repository_contents, name='xml_repository_contents'),
        url(r'^(?P<dir_path>\w+)/(?P<file_path>.+)$', views.edit_xml_file, name='edit_xml_file')
        ]
