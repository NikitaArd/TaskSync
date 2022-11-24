from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
# Local imports
from .models import (
        Project,
        CustomUser,
        )

# All ajax request

def delete_user_from_project(request, project_uuid):

    try:
        user_uuid = request.POST['user_uuid']
    except Exception as e:
        return JsonResponse({'error_message': 'Wystąpił błąd'}, status=400)
    
    try:
        project_object = Project.objects.get(uuid=project_uuid)
        user_object = CustomUser.objects.get(uuid=user_uuid)
    except (Project.DoesNotExist, CustomUser.DoesNotExist, ValidationError):
        return JsonResponse({'error_message': 'Wystąpił błąd'}, status=400)

    if project_object.owner == request.user:
        if project_object.memberpool.user_delete(user_object):
            return JsonResponse({}, status=200)

        return JsonResponse({'error_message': 'Wystąpił błąd'}, status=400)

    return JsonResponse({'error_message': 'Odmowa dostępu'}, status=400)

def add_user_to_project(request, project_uuid):

    try:
        user_email = request.POST['user_email']
    except Exception as e:
        return JsonResponse({'error_message': 'Nieprawidłowy e-mail'}, status=400)

    try:
        project_object = Project.objects.get(uuid=project_uuid)
        user_object = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error_message': 'Nieprawidłowy e-mail'}, status=400)
    except (Project.DoesNotExist, ValidationError):
        return JsonResponse({'error_message': 'Wystąpił błąd'}, status=400)

    if project_object.owner == request.user:
        if project_object.memberpool.user_add(user_object):
            context = {
                    'user_uuid': str(user_object.uuid),
                    'username': user_object.username,
                    'user_avatar_url': user_object.user_avatar.source_image.url,
                    }
            return JsonResponse(context, status=200)

        return JsonResponse({'error_message': 'Wystąpił błąd'}, status=400)

    return JsonResponse({'error_message': 'Odmowa dostępu'}, status=400)


