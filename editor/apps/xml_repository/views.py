from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os

from .models import XMLRepository, XMLFile
from .forms import BasicXMLForm

def base_view(request):
    return render(request, "repository_contents.html")

def xml_repository_contents(request, repository_name):
    """List all the files in the given directory

    :dir_path: TODO
    :returns: TODO

    """
    repo = XMLRepository(repository_name)
    return render(request, "xml_repository_contents.html", {"repository": repo})

def edit_xml_file(request, dir_path, file_path):
    """TODO: Docstring for view_xml_file.

    :request: TODO
    :file_path: TODO
    :returns: TODO

    """
    file_path = os.path.join(settings.DATA_DIR, dir_path, file_path)
    f = XMLFile(file_path)
    form = BasicXMLForm(initial={'xml_text': f.as_text()}) 
    return render(request, "xml_repository_xml_file.html", {"form": form})
