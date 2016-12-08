from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^(?P<dir_path>\w+)/(?P<file_path>.+)$', views.edit_file, name='edit_file')
        ]
