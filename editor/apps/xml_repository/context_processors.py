import os
from django.conf import settings

def repository_list(request):
    return {'repository_list': os.listdir(settings.DATA_DIR)}
