import os
import functools as f

from django.db import models
from django.utils.functional import cached_property
from django.utils.html import *

from lxml import etree

class BaseNode():
    
    def __init__(self, path):
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

class BaseFile(BaseNode):

    @cached_property
    def text(self):
        with open(self.path, 'r') as file_in:
            text = file_in.read()
        return text

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

class TemplateXMLFile(models.Model):
    template_for_type = models.ForeignKey('TypedXMLFile')
    template_file = models.FileField(upload_to='templates/')

class TypedXMLFile(models.Model):
    file_type = models.CharField(max_length=200)
    type_xpath = models.CharField(max_length=1000)
    type_string = models.CharField(max_length=200)

    def __str__(self):
        return self.file_type

    def create_class(self):
             return type(self.file_type, (XMLFile,), {})
    

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
to_markdown = f.partial(to_class, MarkdownFile)

def to_typed_xml(xmlf):
    for t in TypedXMLFile.objects.all():
        if xmlf.string_at_xpath(t.type_xpath, t.type_string):
            xmlf = to_class(t.create_class(), xmlf)
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
        f = to_typed_xml(f)
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
    if os.path.isdir(path):
        return Directory(path)
    else: 
        return BaseFile(path)

