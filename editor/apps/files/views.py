from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .constructors import *

from editor.apps.xml_edit_forms.utils import generate_form
from editor.apps.xml_edit_forms.forms import *
from editor.apps.repository.models import * 
from editor.apps.git_user.models import *
from django import forms

@login_required
def view_file_or_directory(request, repository_name, url_node_path=""):
    """ Delegate display of a path to the directory or file view. """
    remote_repository = RemoteRepository.objects.get(name=repository_name) 
    user = init_git_user(request) 

    repository = LocalUserRepository(user, remote_repository)
    fs_full_path = os.path.join(repository.path, url_node_path)

    if os.path.isdir(fs_full_path):
        return _view_directory(request, repository, url_node_path)
    else: 
        return _view_file(request, repository, url_node_path)

def edit_html(repo_name, file_name):
    return format_html("<a href='{}'>{}</a>",
            reverse('edit_file', args=[repo_name, file_name]),
            "Edit")

@login_required
def view_directory(request, repository_name, path="./"):
    repository = Repository.objects.get(repository_name=repository_name) 
    full_path = os.path.join(repository.path, node_path)
    return _view_directory(request, repository, full_path)

def _view_directory(request, repository, url_dir_path):
    """ List all files in the given directory. """
    f_info = {
            "Name": lambda o: o.name,
            "Type": lambda o: o.ftype,
            "Edit": lambda o: o.generate_html(
                "<a href='{}'>{}</a>",
                reverse('view_file_or_directory', args=[repository.repository.name, os.path.join(url_dir_path, o.name)]),
                "Edit")
            } 
    fs_full_path = os.path.join(repository.path, url_dir_path)
    directory = Directory(fs_full_path)
    file_info = [f.create_info(f_info) for f in directory.display_files()]
    repository.xml_files = file_info
    bcs = generate_breadcrumbs(url_dir_path)
    return render(request, "view_directory.html", {
        "repository": repository,
        "bcs": bcs
        })

def _view_file(request, repository, url_file_path):
    """Provides a view that allows the file contents to be viewed, but not edited. 

    :request: TODO
    :repository_name: TODO
    :file_name: TODO
    :returns: TODO

    """
    fs_full_path = os.path.join(repository.path, url_file_path)
    f = to_file_type(BaseFile(fs_full_path))


    bcs = generate_breadcrumbs(url_file_path)
    if request.method == 'POST':
        form = XMLForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data['text']
            f.write(new_text)
            form = XMLForm(initial={'text':new_text})
            return render(request, "view_file.html", {"f": f, "form": form})
    else:
        form = XMLForm(initial={'text':f.text})

    return render(request, 
            "view_file.html", 
            {"f": f, 
             "repository": repository,
             "form": form, 
             "bcs": bcs
             })

def _edit_file(request, repository, url_file_path, form_type="text_form"):

    fs_full_path = os.path.join(repository.path, url_file_path)
    file_path = os.path.join(settings.DATA_DIR, repository_name, file_name)
    f = to_file_type(BaseFile(file_path))
    form = generate_form(form_type, f)

    return render(request, "dynamic_edit_file.html", {"f": f, "form": form})

def generate_breadcrumbs(path):
    def _format_breadcrumbs(breadcrumbs, path):
        head, tail = os.path.split(path)
        if head:
            breadcrumbs = _format_breadcrumbs(breadcrumbs, head)
        breadcrumbs.append({"label": tail, "url_path": path})
        return breadcrumbs
    return _format_breadcrumbs([], path)

