from django.conf.urls import url
from . import views

urlpatterns = [
        #url(r'^(?P<repository_name>\w+)/$', views.view_directory, name='view_directory'),
        url(r'^(?P<repository_name>\w+)/(?P<url_node_path>.*)$', views.view_file_or_directory, name='view_file_or_directory'),

        #url(r'^(?P<repository_name>\w+)/(?P<file_name>.+)/view$', views.view_file, name='view_file'),
        #url(r'^(?P<repository_name>\w+)/(?P<file_name>.+)/edit$', views.edit_file, name='edit_file'),
        #url(r'^(?P<repository_name>\w+)/(?P<file_name>.+)/edit/(?P<form_type>.+)/$', views.edit_file, name='edit_file')
        ]
