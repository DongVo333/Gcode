from django.contrib.auth import decorators
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request,*args,*kwargs)
    return wrapper_func

def allowed_users(allowed_group=[]):
    def decorator (view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_group:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to enter this page')
        return wrapper_func
    return decorator
def allowed_permission(allowed_roles={}):
    def decorator (view_func):
        def wrapper_func(request, *args, **kwargs):
            roles = set()
            if len(request.user.get_group_permissions())>0:
                roles = request.user.get_group_permissions()
            if allowed_roles.issubset(roles):
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to enter this page')
        return wrapper_func
    return decorator