from django.http import HttpResponse
from django.shortcuts import redirect

def unauthorized_user(view_func): 
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func): 
        def wrapper_func(request,*args,**kwargs):
            if request.user.is_superuser:
                print("yes")
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("<h1>You are not allowed to access this page</h1>")
        return wrapper_func
    return decorator

            
def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('userPage')
    return wrapper_func
   
