import os
import git
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings

from editor.apps.files.constructors import *
from editor.apps.files.models import *
from .utils import *

class Repository(models.Model):
    repository_name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=400)

    def __str__(self):
        return "{}: {}".format(self.repository_name, self.source_url)

    def save(self, *args, **kwargs):
        if not self.pk:
            self._initial_clone()
        super(Repository, self).save(*args, **kwargs)
    
    @property
    def path(self):
        return os.path.join(settings.DATA_DIR, self.repository_name)

    @property
    def git_repo(self):
        return git.Repo(self.path)

    def _initial_clone(self):
        git.Repo.clone_from(self.source_url, self.path)

    @cached_property
    def _changed_paths(self):
        return self._f_paths(self.git_repo.git.diff(name_only=True).split('\n'))

    @cached_property
    def as_directory(self):
        return Directory(self.path)

