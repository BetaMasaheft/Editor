from django import forms
from django.utils.functional import *

class BaseXMLField():

    def __init__(self, name="", xpath="", mode=""):
        self.name = name
        self.xpath = xpath
        self.mode = mode
        self.field_class = forms.CharField
        self.field_kwargs = {"widget": forms.TextInput(attrs={'class': 'form-control'})}

    @cached_property
    def ftype(self):
        return self.__class__.__name__
    
    def populate(self, typed_file):
        xpath_node = typed_file.ns_xpath(self.xpath).text
        return self.name, self.field_class(initial=xpath_node, **self.field_kwargs)

    def process(self, typed_file, content):
        typed_file.set_at_xpath(self.xpath, content)
        return typed_file

class StandardCharField(BaseXMLField): pass

def xml_fields():
    return BaseXMLField.__subclasses__()

def xml_field_choices():
    return tuple((f().ftype, f().ftype) for f in xml_fields())

def xml_field_lookup_dict():
    return dict((f().ftype, f) for f in xml_fields())

def assign_xml_field(field_type):
    return xml_field_lookup_dict().get(field_type, BaseXMLField)

def append(element, text_function):
    """Appends the results of at text generation function to an element. 

    :element: TODO
    :text_function: TODO
    :returns: TODO

    """
    return 

def replace(element, text_function):
    """Replaces an element with the result of a text generation function.

    :element: TODO
    :text_function: TODO
    :returns: TODO

    """
    return 

EDIT_ACTION_FUNCTIONS = (
        ("append", "append"),
        ("replace", "replace")
        )
