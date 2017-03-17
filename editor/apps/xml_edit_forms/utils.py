from .forms import *
from .models import *

base_form_types = {
        'text_form': TextForm,
        'xml_form': XMLForm,
        }

def forms_for_typedfile(typed_file):
    return XMLEditForm.objects.filter(file_type=typed_file.ftype)
