from django.shortcuts import redirect
from django.http import JsonPresponse

def change_avatar(request):

    print(request.POST)

    return JsonResponse({}, status=200)
