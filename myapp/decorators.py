from django.shortcuts import redirect

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            role = request.session.get('role')
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('employee_login')  # Redirect unauthorized users
        return wrapper
    return decorator
