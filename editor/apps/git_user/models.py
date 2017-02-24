from django.db import models
from django.utils.functional import cached_property

from github import Github
from git import Actor

class GitUser(models.Model):

    def __init__(self, access_token):
        self._github = Github(access_token)
        self.user = self._github.get_user()

    @cached_property
    def name(self):
        return self.user.name

    @cached_property
    def email(self):
        return self.user.email

    @cached_property
    def as_git_actor(self):
        return Actor()

