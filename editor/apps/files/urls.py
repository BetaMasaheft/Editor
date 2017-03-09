from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^(?P<repository_name>\w+)/(?P<url_node_path>.*)$', views.view_file_or_directory, name='view_file_or_directory'),
        ]
