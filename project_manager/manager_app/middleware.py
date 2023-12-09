
def default_cookie_setter(next):

    def core_middleware(request):

        response = next(request)

        if request.user.is_authenticated:
            response.set_cookie('u_uuid', request.user.uuid)
        
        return response

    return core_middleware
