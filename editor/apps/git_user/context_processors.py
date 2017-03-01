from social.apps.django_app.default.models import UserSocialAuth
from .models import *

def git_user(request):
    return {'git_user': init_git_user(request)}

