import os
import git
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings

from editor.apps.files.constructors import *
from editor.apps.files.models import *

class Repository(models.Model):

    def __init__(self, repository_name):
        self.name = repository_name
        self.path = os.path.join(settings.DATA_DIR, repository_name)
        self.git_repo = git.Repo(self.path)

    def _f_path(self, f_name):
        return os.path.join(self.path, f_name)
    
    def _f_paths(self, f_names):
        return sorted([self._f_path(n) for n in f_names])

    @cached_property
    def _content_paths(self):
        return self._f_paths(os.listdir(self.path))

    @cached_property
    def _changed_paths(self):
        return self._f_paths(self.git_repo.git.diff(name_only=True).split('\n'))
    
    @cached_property
    def base_files(self):
        return [BaseFile(p) for p in self._content_paths]

    @cached_property
    def files(self):
        return [to_file_type(f) for f in self.base_files]

