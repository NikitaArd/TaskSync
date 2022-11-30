from django.conf import settings

from .models import (
    CustomUser,
    Project,
    Column,
    Task,
    TasksSeq,
    Chat,
    Message,
)

def task_shift(json_data:dict) -> dict:
    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['to_column_uuid'])
        tasks_seq = TasksSeq.objects.get(column=column)
    except (Column.DoesNotExist, TasksSeq.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']
        

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        if not tasks_seq.shift_task(json_data['prev_task_uuid'], json_data['task_uuid'], json_data['user_id']):
            error_message = settings.WS_ERROR_MESSAGES['Invalid_data']
    else:
        error_message = settings.WS_ERROR_MESSAGES['Access_denied']

    context = {
        'request_type': json_data['request_type'],
        'prev_task': json_data['prev_task_uuid'],
        'task': json_data['task_uuid'],
        'column': json_data['to_column_uuid'],
        'error_message': error_message,
    } 

    return context

def task_add(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
        new_task = Task(content=settings.DEFAULT_TASK_CONTENT, column=column)
        new_task.save()
    except (Column.DoesNotExist, Task.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    context = {
        'request_type':json_data['request_type'],
        'new_task_uuid': str(new_task.uuid),
        'new_task_content': new_task.content,
        'column_uuid': json_data['column_uuid'],
        'error_message': error_message,
    }

    return context
    
def task_status_edit(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
    except (Column.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MASSEGES['Invalid_data']

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        task_toggle = Task.objects.get(uuid=json_data['task_uuid'])
        task_toggle.toggle_status()
    else:
        error_message = settings.WS_ERROR_MESSAGES

    context = {
        'request_type': json_data['request_type'],
        'task_uuid': json_data['task_uuid'],
        'column_uuid': json_data['column_uuid'],
        'error_message': error_message, 
    }

    return context

def task_delete(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
    except (Column.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        try:
            task_to_delete = Task.objects.get(uuid=json_data['task_uuid'])
            task_to_delete.delete()
        except (Task.DoesNotExist, ValueError):
            error_message = settings.WS_ERROR_MESSAGES['Invalid_data']
    else:
        error_message = settings.WS_ERROR_MESSAGES['Access_denied']

    context = {
        'request_type': json_data['request_type'],
        'task_uuid': json_data['task_uuid'],
        'error_message': error_message, 
    }

    return context

def task_content_edit(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
    except (Column.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        task_to_edit = Task.objects.get(uuid=json_data['task_uuid'])
        if not task_to_edit.change_content(json_data['new_content']):
            error_message = settings.WS_ERROR_MESSAGES
    else:
        error_message = settings.WS_ERROR_MESSAGES['Acess_denied']

    context = {
        'request_type': json_data['request_type'],
        'task_uuid': json_data['task_uuid'],
        'column_uuid': json_data['column_uuid'],
        'new_content': json_data['new_content'],
        'error_message': error_message,
    }

    return context

def column_add(json_data:dict) -> dict:

    error_message = ''

    try:
        project = Project.objects.get(uuid=json_data['project_uuid'])
        column = Column(name=settings.DEFAULT_COLUMN_NAME, project=project)
        column.save()
    except (Project.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    context = {
        'request_type': json_data['request_type'],
        'column_uuid': str(column.uuid),
        'column_name': column.name,
        'error_message': error_message,
    }

    return context

def column_delete(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
    except (Column.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        column.delete()
    else:
        error_message = settings.WS_ERROR_MESSAGES

    context = {
        'request_type': json_data['request_type'],
        'column_uuid': json_data['column_uuid'],
        'error_message': error_message, 
    }

    return context

def column_name_edit(json_data:dict) -> dict:

    error_message = ''

    try:
        column = Column.objects.get(uuid=json_data['column_uuid'])
    except (Column.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    if column.project.check_user_is_member(user_uuid=json_data['user_id']):
        if not column.change_name(json_data['new_name']):
            error_message = settings.WS_ERROR_MESSAGES['Invalid_data']
    else:
        error_message = settings.WS_ERROR_MESSAGE['Access_denied']

    context = {
        'request_type': json_data['request_type'],
        'column_uuid': json_data['column_uuid'],
        'new_name': json_data['new_name'],
        'error_message': error_message,
    }

    return context

def chat_message(json_data:dict) -> dict:

    error_message = ''

    try:
        project = Project.objects.get(uuid=json_data['project_uuid'])
        user = CustomUser.objects.get(uuid=json_data['user_id'])

        new_message = Message(message_content=json_data['message'], chat=project.chat, writer=user)
        new_message.save()
    except (User.DoesNotExist, Project.DoesNotExist, ValueError):
        error_message = settings.WS_ERROR_MESSAGES['Invalid_data']

    context = {
        'request_type': json_data['request_type'],
        'message': json_data['message'],
        'username': json_data['username'],
        'user_id': json_data['user_id'],
        'error_message': error_message,
    }

    return context

