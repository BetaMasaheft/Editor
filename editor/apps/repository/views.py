from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.html import *

import os

from editor.apps.git_user.models import *
from .models import *

def base_view(request):
    return render(request, "repository_contents.html")

