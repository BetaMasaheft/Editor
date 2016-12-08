import os

from django.db import models
from django.utils.functional import cached_property

from lxml import etree

class BaseFile(models.Model):

    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[1]
        self.ext = os.path.splitext(self.name)[1]

    def text(self):
        with open(self.path, 'r') as file_in:
            text = file_in.read()
        return text

    def create_info(self, d):
        return {k: f(self) for k,f in d.items()}

class HiddenFile(BaseFile): pass

class MarkdownFile(BaseFile): pass
    
class BaseXMLFile(BaseFile): pass 

class UnparsableXMLFile(BaseXMLFile): pass

class XMLFile(BaseXMLFile):

    @cached_property
    def parsed_tree(self):
        return etree.parse(self.path) 

    @cached_property
    def namespace(self):
        return self.parsed_tree.xpath('namespace-uri(.)')
    
    def ns_xpath(self, xpath, namespace=None):
        if not namespace:
            namespace = self.namespace
        return self.parsed_tree.xpath(xpath, 
                namespaces={'ns': namespace}
                )
