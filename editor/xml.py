from lxml import etree

def parse_xml(path):
    """ Applies the xml_reader to a 
    :path: filepath
    :returns:
    """
    return xml_reader(etree.parse(path))

def xml_reader(tree):
    return document_type(tree) 

def document_type(tree):
    return tree.getroot().attrib['type']

