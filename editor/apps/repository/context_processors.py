import os
from django.conf import settings
from .models import *

def repository_list(request):
    return {'repository_list': RemoteRepository.objects.all()}
