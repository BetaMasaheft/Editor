from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.html import *
from django.contrib.auth.decorators import login_required

from .models import *
from .constructors import *

from editor.apps.xml_edit_forms.utils import *
from editor.apps.repository.models import * 
from editor.apps.repository.forms import * 
from editor.apps.repository.utils import * 
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
        # This indicates that it's a repository root.
        if not url_node_path:
            return _view_repository_root(request, repository)
        else:
            return _view_directory(request, repository, url_node_path)
    else: 
        return _view_file(request, repository, url_node_path)

def edit_html(repo_name, file_name):
    return format_html("<a href='{}'>{}</a>",
            reverse('edit_file', args=[repo_name, file_name]),
            "Edit")

def _view_directory(request, repository, url_dir_path):
    """ List all files in the given directory. """
    def all_form_urls(typed_file):
        out = ""
        for f in form_names_for_typed_file(typed_file):
            out += format_html("<a href='{}?form_type={}'>{}</a> ",
                    reverse('view_file_or_directory', 
                        args=[repository.repository.name, repository.rel_node_path(typed_file)]
                        ), f, f)
        return format_html(out)

    f_info = {
            "Name": lambda o: repository.rel_node_path(o),
            "Type": lambda o: o.ftype,
            "Edit": lambda o: all_form_urls(o),
            } 

    fs_full_path = os.path.join(repository.path, url_dir_path)

    directory = Directory(fs_full_path)

    changed_names = repository.changed_names(directory)
    unchanged, changed = partition(lambda x: x.name in changed_names, directory.display_files())
    changed_files = [f.create_info(f_info) for f in changed]
    unchanged_files = [f.create_info(f_info) for f in unchanged]
    
    bcs = generate_breadcrumbs(url_dir_path)

    return render(request, "view_directory.html", {
        "repository": repository,
        "changed_files": changed_files,
        "unchanged_files": unchanged_files,
        "bcs": bcs
        })

def _view_repository_root(request, repository):
    """ A view for the repository root that also displays all uncommitted files 
    within the repo. """

    def all_form_urls(typed_file):
        out = ""
        for f in form_names_for_typed_file(typed_file):
            out += format_html("<a href='{}?form_type={}'>{}</a>",
                    reverse('view_file_or_directory', 
                        args=[repository.repository.name, repository.rel_node_path(typed_file)]
                        ), f, f)
        return format_html(out)

    f_info = {
            "Name": lambda o: repository.rel_node_path(o),
            "Type": lambda o: o.ftype,
            "Edit": lambda o: all_form_urls(o),
            } 

    bcs = generate_breadcrumbs("")

    directory = repository.as_directory
    changed_files = [f.create_info(f_info) for f in repository.all_changed_files()]
    unchanged_files = [f.create_info(f_info) for f in directory.display_files()]

    if request.method == 'POST':
        commit_form = CommitForm(request.POST)
        if commit_form.is_valid():
            message = commit_form.cleaned_data['message']
            repository.add_commit_and_push(message)
            commit_form = CommitForm()
    else:
        commit_form = CommitForm()

    return render(request, "view_repository_root.html", {
        "repository": repository,
        "commit_form": commit_form,
        "changed_files": changed_files,
        "unchanged_files": unchanged_files,
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

    form_type = request.GET.get('form_type', 'xml_form')

    form_model = form_lookup_for_typed_file(f, form_type)
    form = form_model.create_and_populate(f) 

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            f = form_model.process_form(form, f)
            f.write()
    else:
        form = form()

    return render(request, 
            "view_file.html", 
            {"f": f, 
             "repository": repository,
             "form": form, 
             "bcs": bcs
             })

def generate_breadcrumbs(path):
    def _format_breadcrumbs(breadcrumbs, path):
        head, tail = os.path.split(path)
        if head:
            breadcrumbs = _format_breadcrumbs(breadcrumbs, head)
        breadcrumbs.append({"label": tail, "url_path": path})
        return breadcrumbs
    return _format_breadcrumbs([], path)

