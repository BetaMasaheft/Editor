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

def base_view(request):
    return render(request, "repository_contents.html")

def repository_contents(request, repository_name):
    """List all the files in the given directory

    :dir_path: TODO
    :returns: TODO

    """

    f_info = {
            "name": lambda o: o.name,
            "f_type": lambda o: o.ext, 
            "f_class": lambda o: o.__class__.__name__,
            "edit": lambda o: edit_html(repository_name, o.name),
            } 

    repo = Repository(repository_name) 

    file_info = [f.create_info(f_info) for f in repo.files]
    
    repo.xml_files = file_info
    return render(request, "xml_repository_contents.html", {
        "repository": repo,
        })


