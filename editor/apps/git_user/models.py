import os

from django.db import models
from django.utils.functional import cached_property
from django.conf import settings

from social_django.models import UserSocialAuth

from github import Github
from git import Actor

class GitUser(models.Model):

    def __init__(self, access_token):
        self._github = Github(access_token)
        self.user = self._github.get_user()
    
    @cached_property
    def git_username(self):
        return self.user.login

    @cached_property
    def name(self):
        return self.user.name

    @cached_property
    def email(self):
        return self.user.email

    @cached_property
    def as_git_actor(self):
        return Actor()

    @cached_property
    def data_path(self):
        path = os.path.join(settings.DATA_DIR, self.git_username)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

def init_git_user(request):
    user = request.user
    if user.is_authenticated:
        try:
            gh_login = user.social_auth.get(provider='github')
            gh_access_token = gh_login.extra_data['access_token']
            git_user = GitUser(gh_access_token) 
        except UserSocialAuth.DoesNotExist:
            git_user = None
    else:
        git_user = None
    return git_user

