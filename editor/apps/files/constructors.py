from .models import *

import functools as f

from lxml import etree

def to_class(cls, obj):
    """Changes the class of an object to the provided Class. 

    :cls: Class
    :obj: Object
    :returns: Object

    """
    obj.__class__ = cls
    return obj

to_base = f.partial(to_class, BaseFile)
to_markdown = f.partial(to_class, MarkdownFile)

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
    except: 
        f = to_class(UnparsableXMLFile, f)
    return f

def to_file_type(bf):
    """ Convert BaseFile to specialised subtypes 
        depending on the file extension. """
    _type_assigners = {
            ".md": to_markdown,  
            ".xml": to_xml_type, 
            }
    return _type_assigners.get(bf.ext, to_base)(bf)
