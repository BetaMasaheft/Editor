import os
import git
from lxml import etree
from django.db import models
from django.conf import settings

def apply_dict(func_dict, obj):
    return dict((key, func(obj)) for key, func in func_dict.items())


class XMLRepository(models.Model):

    #repository_url = models.URLField()
    #repository_path = models.CharField(editable=False)

    list_data = {
            'Name': lambda x: x.name, 
            'Type': lambda x: x.document_type()
            }

    def __init__(self, repository_name):
        self.name = repository_name
        self.path = os.path.join(settings.DATA_DIR, repository_name)
        self.git_repo = git.Repo(self.path)

    def _contents(self):
        return os.listdir(self.path)

    def xml_paths(self):
        _create_path = lambda x: os.path.join(self.path, x)
        _xml_filter = lambda x: x.endswith(('xml'))
        return sorted(map(_create_path, filter(_xml_filter, self._contents())))

    def changed_xml_files(self):
        """ Returns a list of filenames that have changed since the last commit. """
        return self.git_repo.git.diff(name_only=True).split('\n')

    def formatted_content_list(self): 
        return [apply_dict(self.list_data, XMLFile(p)) for p in self.xml_paths()]

class XMLFile(models.Model):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)

    def _as_tree(self):
        return etree.parse(self.path) 

    def document_type(self):
        return self._as_tree().getroot().attrib['type']

    def as_text(self):
        with open(self.path, 'r') as xml_in:
            text = xml_in.read()
        return text
