from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View



def class_login_required(cls):
    if (not isinstance(cls,type) or not issubclass(cls,View)):
        raise ImproperlyConfigured('class login required must be applied ro subclass or view class')
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls



def require_authenticated_permission(permission):


    def decorator(cls):
        if (not isinstance(cls, type) or not issubclass(cls, View)):
            raise ImproperlyConfigured(
                'require_authenticated_permission must be applied to subclass or view class'
            )
        check_auth = method_decorator(login_required)
        check_perm = method_decorator(permission_required(permission,raise_exception=True))

        cls.dispatch = check_auth(check_perm(cls.dispatch))
        return cls

    return decorator




