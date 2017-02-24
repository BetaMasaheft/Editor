from social.apps.django_app.default.models import UserSocialAuth
from .models import *

def git_user(request):
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
    return {'git_user': git_user}

