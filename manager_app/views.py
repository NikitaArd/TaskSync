from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import ValidationError

# Local imports
from .models import (
    CustomUser,
    Avatar,
    Project,
    MemberPool,
    Column,
    Task,
    TasksSeq,
    Chat,
    Message,
    AttachmentFile,
    ProjectFiles
)

from .forms import (
    RegistrationForm,
    LoginForm,
    NewPasswordSetForm,
    ProjectCreateForm,
)
from .decorators import (
    anonymous_required
)


def get_error_message_from_form(form) -> dict:
    invalid_field = [field for field in form.errors.as_data()][0]  # From Python 3.7 dict saves ordering
    error_message = form.errors[invalid_field][0]

    return {'invalid_field': invalid_field, 'error_message': error_message}


def main_page(request):
    return render(request, 'manager_app/title_page.html', {})


@anonymous_required
def registration_page(request):
    form = RegistrationForm

    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            created_user = form.save()
            login(request, created_user)
            return redirect(reverse('account_info_page'))

        form_error = get_error_message_from_form(form)

        context['form'] = form  # Sends filled form
        context['invalid_field'] = form_error['invalid_field']
        context['error_message'] = form_error['error_message']

    return render(request, 'manager_app/registration_page.html', context)


@anonymous_required
def login_page(request):
    form = LoginForm

    context = {'form': form}

    if request.method == 'POST':

        form = LoginForm(request.POST)
        user = authenticate(email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)

            return redirect(reverse('account_info_page'))

        context['form'] = form
        context['invalid_field'] = 'all'
        context['error_dict'] = {'all': 'Wprowadzono błędne dane'}

    return render(request, 'manager_app/login_page.html', context)


def logout_page(request):
    logout(request)

    return redirect(reverse('login_page'))


@login_required
def account_info_page(request):
    mode = request.GET.get('mode', '')
    avatar_slug = request.GET.get('avatar', '')

    if mode == 'change':
        cur_user = CustomUser.objects.get(id=request.user.id)
        try:
            cur_user.user_avatar = Avatar.objects.get(search_slug=avatar_slug)
        except Avatar.DoesNotExist:
            return redirect(reverse('account_info_page'))
        cur_user.save()

        return redirect(reverse('account_info_page'))

    avatars = Avatar.objects.all()
    avatar_change_url = '{}{}'.format(reverse('account_info_page'), '?mode=change&avatar=')
    project_count = Project.objects.filter(memberpool__members__in=str(request.user.id)).count()

    context = {
        'avatars': avatars,
        'avatar_change_url': avatar_change_url,
        'project_count': project_count,
    }

    return render(request, 'manager_app/account_info_page.html', context)


@login_required
def projects_menu(request):
    form = ProjectCreateForm

    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)

        if form.is_valid():
            new_project = Project(
                name=form.cleaned_data['name'],
                max_members=form.cleaned_data['max_members'],
                owner=request.user,
            )

            new_project.save()

            return redirect(reverse('projects_menu'))

    mode = request.GET.get('mode', '')
    option = request.GET.get('option', '')

    projects = Project.objects.filter(memberpool__members__in=str(request.user.id))
    projects_own = Project.objects.filter(owner=request.user)

    if mode == 'sort' and option:

        if option == 'own':
            projects = projects_own
        elif option == 'member':
            projects = projects.difference(projects_own)
        else:
            return redirect(reverse('projects_menu'))

    context = {
        'projects': projects,
        'form': form,
    }

    return render(request, 'manager_app/projects_menu.html', context)


@login_required
def project_settings(request, project_uuid):
    try:
        project = Project.objects.get(uuid=project_uuid)
    except Project.DoesNotExist:
        return redirect(reverse('projects_menu'))

    form = ProjectCreateForm

    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            max_members = form.cleaned_data['max_members']

            project.change_project_settings(name, max_members)

            return redirect(reverse('projects_menu'))

    members = project.memberpool.members.all()

    context = {
        'project': project,
        'members': members,
        'form': form,
    }

    return render(request, 'manager_app/project_settings.html', context)


@login_required
def project_delete(request, project_uuid):
    try:
        project = Project.objects.get(uuid=project_uuid)
    except Project.DoesNotExist:
        return redirect(reverse('projects_menu'))

    if project.owner == request.user:
        project.delete()

    return redirect(reverse('projects_menu'))


@login_required
def project_main_page(request, project_uuid):
    try:
        project = Project.objects.get(uuid=project_uuid)
    except (Project.DoesNotExist, ValidationError):
        return redirect(reverse('projects_menu'))

    if request.user not in project.memberpool.members.all():
        return redirect(reverse('projects_menu'))

    columns = Column.objects.filter(project__uuid=project_uuid)
    tasks_seq = TasksSeq.objects.filter(column__in=columns)
    tasks = Task.objects.get_by_sequence(tasks_seq=tasks_seq, columns=columns)
    chat = project.chat
    project_messages = Message.objects.filter(chat=chat)
    project_files = AttachmentFile.objects.filter(project_files_id__project_id=project)

    context = {
        'project': project,
        'columns': columns,
        'tasks': tasks,
        'chat': chat,
        'project_messages': project_messages,
        'project_files': project_files,
    }

    response = render(request, 'manager_app/project_main_page.html', context)
    response.set_cookie('p_uuid', project.uuid)

    return response


@login_required
def file_upload(request, project_uuid):
    if request.POST:
        print(request.FILES)
        try:
            project = Project.objects.get(uuid=project_uuid)
        except (Project.DoesNotExist, ValidationError):
            return Http404()

        if request.user not in project.memberpool.members.all():
            return redirect(reverse('projects_menu'))

        new_file_uploaded = AttachmentFile(source_file=request.FILES['uploaded_file'],
                                           project_files_id=ProjectFiles.objects.get(project_id=project),
                                           uploaded_by=request.user)
        new_file_uploaded.save()

        return redirect(request.POST.get('next', '/'))
    return Http404()


@login_required
def file_delete(request, project_uuid, file_uuid):
    try:
        project = Project.objects.get(uuid=project_uuid)
    except (Project.DoesNotExist, ValidationError):
        return Http404()

    if request.user not in project.memberpool.members.all():
        return redirect(reverse('projects_menu'))

    try:
        file_to_delete = AttachmentFile.objects.get(uuid=file_uuid)
        file_to_delete.delete()
    except (AttachmentFile.DoesNotExist, ValidationError):
        return Http404()

    return redirect(project_main_page, project_uuid)


class PasswordResetConfirmViewWithErrors(PasswordResetConfirmView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':

            form = context['form']

            if form.is_valid():
                context['invalid_field'] = ''
                context['error_dict'] = {}
            else:
                form_error = get_error_messages(form)

                context['invalid_field'] = form_error['invalid_field']
                context['error_message'] = form_error['error_message']

        return context
