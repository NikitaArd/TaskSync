from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import (
        authenticate,
        login,
        logout,
        )
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from django.contrib.auth.views import PasswordResetConfirmView

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

def get_error_messages(form) -> dict:
    error_dict = dict()
    invalid_field = ''

    for field in form.errors:
        error_dict[field] = form.errors[field][0]

    invalid_field = [x for x in form.errors.as_data()]

    return {'invalid_field': invalid_field[0], 'error_dict': error_dict}

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
            form.save() 
            return redirect(reverse('title_page'))

        error_messages = get_error_messages(form)
        
        context['form'] = form
        context['invalid_field'] = error_messages['invalid_field']
        context['error_dict'] = error_messages['error_dict']

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

    context = {
            'avatars': avatars,
            'avatar_change_url': avatar_change_url,
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

    context = {
            'project': project,
            'columns': columns,
            'tasks': tasks,
            'chat': chat,
            'project_messages': project_messages
            }

    response = render(request, 'manager_app/project_main_page.html', context)
    response.set_cookie('p_uuid', project.uuid)

    return response


class PasswordResetConfirmViewWithErrors(PasswordResetConfirmView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':

            form = context['form']

            if form.is_valid():
                context['invalid_field'] = ''
                context['error_dict'] = {}
            else:
                error_messages = get_error_messages(form)

                context['invalid_field'] = error_messages['invalid_field']
                context['error_dict'] = error_messages['error_dict']

        return context

