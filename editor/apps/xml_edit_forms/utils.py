from .models import *

from editor.apps.files.models import *

def forms_for_typed_file(typed_file):
    if typed_file.ftype in all_xml_type_names():
        return [XMLForm] + [form for form in XMLEditForm.objects.filter(file_type=typed_file.ftype)]
    elif typed_file.ftype in all_file_type_names():
        return [TextForm]
    else:
        return []

def form_names_for_typed_file(typed_file):
    return [f.form_name for f in forms_for_typed_file(typed_file)]

def form_lookup_for_typed_file(typed_file, name):
    return dict((f.form_name, f) for f in forms_for_typed_file(typed_file)).get(name, XMLForm)

