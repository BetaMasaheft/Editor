import os
import git
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings

from editor.apps.files.constructors import *
from editor.apps.files.models import *
from .utils import *

class RemoteRepository(models.Model):
    name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=400)

    def __str__(self):
        return "{}: {}".format(self.repository_name, self.source_url)

class LocalUserRepository():

    def __init__(self, user, repository):
        self.user = user
        self.repository = repository
        if not os.path.exists(self.path):
            self._initial_clone()

    @property
    def path(self):
        return os.path.join(self.user.data_path, self.repository.name)
    
    def __str__(self):
        return "{}: {}".format(self.user.name, self.repository.name)

    @property
    def git_repo(self):
        return git.Repo(self.path)

    def _initial_clone(self):
        git.Repo.clone_from(self.repository.source_url, self.path)

    @cached_property
    def _changed_paths(self):
        return self._f_paths(self.git_repo.git.diff(name_only=True).split('\n'))

    @cached_property
    def as_directory(self):
        return Directory(self.path)

