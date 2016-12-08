from django.shortcuts import render
from django.conf import settings

from .models import *
from .constructors import *

#from editor.apps.edit_forms.constructors import *

def edit_file(request, dir_path, file_path):
    """TODO: Docstring for view_xml_file.

    :request: TODO
    :file_path: TODO
    :returns: TODO

    """
    file_path = os.path.join(settings.DATA_DIR, dir_path, file_path)
    f = to_file_type(BaseFile(file_path))
    form = assign_form(f)
    return render(request, "xml_repository_xml_file.html", {"form": form})
