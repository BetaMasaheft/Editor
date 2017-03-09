import os
import git
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings

from editor.apps.files.models import *
from .utils import *

class RemoteRepository(models.Model):
    name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=400)

    def __str__(self):
        return "{}: {}".format(self.name, self.source_url)

class LocalUserRepository():

    def __init__(self, user, repository):
        self.user = user
        self.repository = repository
        if not os.path.exists(self.path):
            self._initial_clone()
    
    def __str__(self):
        return "{}: {}".format(self.user.name, self.repository.name)

    @property
    def path(self):
        return os.path.join(self.user.data_path, self.repository.name)

    @property
    def git_repo(self):
        return git.Repo(self.path)

    def _initial_clone(self):
        git.Repo.clone_from(self.repository.source_url, self.path)

    def rel_node_path(self, node):
        """ The relative path of a node and this repository. """
        return os.path.relpath(node.path, self.path)

    def pull(self):
        """ Pulls updates from the remote repository. """
        origin = self.git_repo.remotes.origin
        origin.pull()

    def push(self):
        """ Pushes updates to the remote repository. """
        origin = self.git_repo.remotes.origin
        origin.push()

    def add_file(self, path):
        """ Adds a file to the current staged index"""
        self.git_repo.index.add([path])

    def commit(self, commit_message):
        """ Commits the current staged index"""
        self.git_repo.index.commit(commit_message)

    def add_commit_and_push(self, commit_message):
        for p in self.changed_paths():
            self.add_file(p)
        self.commit(commit_message)
        self.push()

    def changed_paths(self, directory=None):
        if not directory:
            directory = self.as_directory
        return self.git_repo.git.diff(directory.path, name_only=True).split('\n')

    def changed_names(self, directory):
        """ A list of names of changed files within a directory. """
        return [os.path.split(p)[1] for p in self.changed_paths(directory)]

    def all_changed_files(self):
        """ A list of all file objects within the repository that have changed. """
        return [path_to_file_type(os.path.join(self.path, p)) for p in self.changed_paths() if p]

    @cached_property
    def as_directory(self):
        return Directory(self.path)

