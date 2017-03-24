import os
import urllib.parse 
import collections
from django.urls import reverse

from editor.apps.xml_edit_forms.utils import * 

def generate_breadcrumbs(path):
    def _format_breadcrumbs(breadcrumbs, path):
        head, tail = os.path.split(path)
        if head:
            breadcrumbs = _format_breadcrumbs(breadcrumbs, head)
        breadcrumbs.append({"label": tail, "url_path": path})
        return breadcrumbs
    return _format_breadcrumbs([], path)

def url_with_qs(path, qs_dict={}):
    if qs_dict:
        return path + '?' + urllib.parse.urlencode(qs_dict)
    else:
        return path

def dummy_lookup(node):
    names = form_names_for_typed_file(node)
    return 

class NodeURLFactory():

    def __init__(self, repository):
        self.node_qs_lookup = {}
        self.node_qs_generator = form_names_for_typed_file
        self.repository = repository

    def _view_node_url(self, node):
        return reverse('view_file_or_directory', 
                args=[
                    self.repository.repository.name,
                    self.repository.rel_node_path(node)
                    ]
                )
    def _edit_form_node_url(self, node, form_name):
        return url_with_qs(self._view_node_url(node),
                {'form_type': form_name}
                )

    def _format_url(self, name, url):
        return format_html("<a href='{}'>{}</a>", url, name)

    def _lookup_qs_for_node(self, node):
        if node.ftype not in self.node_qs_lookup:
            self.node_qs_lookup[node.ftype] = self.node_qs_generator(node)
        return self.node_qs_lookup[node.ftype]

    def generate_urls(self, node):
        """ Generate a list of name, url tuples for this node """
        qss = self._lookup_qs_for_node(node)
        if qss:
            return [(q, self._edit_form_node_url(node, q)) for q in qss]
        else:
            return [('view', self._view_node_url(node))]

    def format_node_urls(self, node):
        return format_html(" ".join(self._format_url(*a) for a in self.generate_urls(node)))
