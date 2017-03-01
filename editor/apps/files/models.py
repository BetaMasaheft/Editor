import os
import functools as f
import types

from django.db import models
from django.utils.functional import cached_property
from django.utils.html import *

from editor.apps.xml_edit_forms.forms import *

from lxml import etree

class BaseNode():
    
    def __init__(self, path=""):
        self.path = path
        self.name = os.path.split(self.path)[1]
        self.ext = os.path.splitext(self.name)[1]

    @cached_property
    def ftype(self):
        return self.__class__.__name__
    
    def create_info(self, d):
        return {k: f(self) for k,f in d.items()}

    def generate_html(self, fmt_str, *args):
        return format_html(fmt_str, *args)

class Directory(BaseNode):

    def _f_path(self, f_name):
        return os.path.join(self.path, f_name)
    
    def _f_paths(self, f_names):
        return sorted([self._f_path(n) for n in f_names])

    @cached_property
    def _content_paths(self):
        return self._f_paths(os.listdir(self.path))

    @cached_property
    def contents(self):
        return [to_directory_or_file(p) for p in self._content_paths]

    @cached_property
    def files(self):
        return [to_file_type(f) for f in self.contents]

    def file_ok(self, f):
        exclude = [HiddenDirectory().ftype, HiddenFile().ftype]
        return f.ftype not in exclude

    def display_files(self):
        return [f for f in self.files if self.file_ok(f)]

class BaseFile(BaseNode):

    @cached_property
    def text(self):
        with open(self.path, 'r') as file_in:
            text = file_in.read()
        return text

    def form_types(self):
        """ Returns a list of possible file types for this file """
        return [TextForm]

class HiddenDirectory(Directory): pass

class HiddenFile(BaseFile): pass

class MarkdownFile(BaseFile): pass
    
class BaseXMLFile(BaseFile): pass 

class UnparsableXMLFile(BaseXMLFile): pass

class XMLFile(BaseXMLFile):

    @cached_property
    def parsed_tree(self):
        return etree.parse(self.path) 

    @cached_property
    def text(self):
        return etree.tostring(self.parsed_tree, pretty_print=True)

    @cached_property
    def namespace(self):
        return self.parsed_tree.xpath('namespace-uri(.)')
    
    def ns_xpath(self, xpath, namespace=None):
        if not namespace:
            namespace = self.namespace
        return self.parsed_tree.xpath(xpath, 
                namespaces={'ns': namespace}
                )

    def string_at_xpath(self, xpath, string):
        """ Tests if a given string exists at an xpath. """
        results = self.ns_xpath(xpath)
        if results:
            if results[0] == string:
                return True
            else:
                return False
        else:
            return False

    @cached_property
    def form_types(self):
        """ Returns a list of possible file types for this file """
        return [XMLForm]

class TEITypedXMLFile(XMLFile):
    type_xpath = "/ns:TEI/@type"
    type_string = ""

class TEIPlace(TEITypedXMLFile):
    type_string = "place"

    def form_types(self):
        """ Returns a list of possible file types for this file """
        return [TextForm, XMLForm]

class TEIPerson(TEITypedXMLFile):
    type_string = "pers"

class TEIWork(TEITypedXMLFile):
    type_string = "work"

class TEIManuscript(TEITypedXMLFile):
    type_string = "mss"

FILE_TYPE_CHOICES = tuple((str(ft().ftype), str(ft().ftype)) for ft in TEITypedXMLFile.__subclasses__())

class TemplateXMLFile(models.Model):
    file_type = models.CharField(max_length=100, choices=FILE_TYPE_CHOICES)
    template_file = models.FileField(upload_to='templates/')

def to_class(cls, obj):
    """Changes the class of an object to the provided Class. 

    :cls: Class
    :obj: Object
    :returns: Object

    """
    obj.__class__ = cls
    return obj

identity = lambda x: x
to_basefile = f.partial(to_class, BaseNode)
to_directory = f.partial(to_class, Directory)
to_hidden_file = f.partial(to_class, HiddenFile)
to_hidden_directory = f.partial(to_class, HiddenDirectory)
to_markdown = f.partial(to_class, MarkdownFile)

def tei_typed_xml_file_types():
    return TEITypedXMLFile.__subclasses__()

def to_tei_typed_xml(xmlf):
    for tei_type in tei_typed_xml_file_types():
        if xmlf.string_at_xpath(tei_type.type_xpath, tei_type.type_string):
            xmlf = to_class(tei_type, xmlf)
            break
    return xmlf

def to_xml_type(bf):
    """Attempt to convert a BaseFile to an XMLFile type.
    :bf: BaseFile
    :returns: 
    """
    f = bf
    try: 
        tree = etree.parse(f.path)
        f = to_class(XMLFile, f)
        f.parsed_tree = tree
        f = to_tei_typed_xml(f)
    except Exception as e: 
        f = to_class(UnparsableXMLFile, f)
    return f

def to_file_type(bf):
    """ Convert BaseFile to specialised subtypes 
        depending on the file extension. """
    _type_assigners = {
            ".md": to_markdown,  
            ".xml": to_xml_type, 
            }
    return _type_assigners.get(bf.ext, identity)(bf)

def to_directory_or_file(path):
    bn = BaseNode(path)
    if bn.name.startswith('.'):
        if os.path.isdir(bn.path):
            return to_hidden_directory(bn)
        else: 
            return to_hidden_file(bn)
    else:
        if os.path.isdir(bn.path):
            return to_directory(bn)
        else: 
            return to_basefile(bn)
