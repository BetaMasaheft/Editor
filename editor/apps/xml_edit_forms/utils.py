from .forms import *
from .models import *

def forms_for_typed_file(typed_file):
    return [XMLForm] + [form for form in XMLEditForm.objects.filter(file_type=typed_file.ftype)]

def form_names_for_typed_file(typed_file):
    return [f.form_name for f in forms_for_typed_file(typed_file)]

def form_lookup_for_typed_file(typed_file, name):
    return dict((f.form_name, f) for f in forms_for_typed_file(typed_file)).get(name, XMLForm)

