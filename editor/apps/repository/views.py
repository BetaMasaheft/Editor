from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.html import *

import os

from .models import *

def edit_html(repo_name, file_name):
    return format_html("<a href='{}'>{}</a>",
            reverse('edit_file', args=[repo_name, file_name]),
            "Edit")

def view_html(repo_name, file_name):
    return format_html("<a href='{}'>{}</a>",
            reverse('view_file', args=[repo_name, file_name]),
            "View")


def base_view(request):
    return render(request, "repository_contents.html")

def add_and_commit(request, repository_name):
    return render(request, "repository_commit.html")
