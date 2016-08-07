from django.shortcuts import render
from django.http import HttpResponse

import os

from .models import XMLRepository

def base_view(request):
    return render(request, "repository_contents.html")

def xml_repository_contents(request, repository_name):
    """List all the files in the given directory

    :dir_path: TODO
    :returns: TODO

    """
    repo = XMLRepository(repository_name)
    return render(request, "xml_repository_contents.html", {"repository": repo})

def view_xml_file(request, dir_path, file_path):
    """TODO: Docstring for view_xml_file.

    :request: TODO
    :file_path: TODO
    :returns: TODO

    """
    file_path = os.path.join("../data/", dir_path, file_path)
    with open(file_path, 'r') as f_in:
        text = f_in.read()
    return HttpResponse(text)
