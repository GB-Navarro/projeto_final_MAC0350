from functools import wraps

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from apps.contas.models import Usuario, Administrador


def admin_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.tipo != Usuario.ADM:
            return HttpResponseForbidden()

        try:
            administrador = request.user.administrador
        except Administrador.DoesNotExist:
            return HttpResponseForbidden()

        if not administrador.aprovado:
            return HttpResponseForbidden()

        return view(request, *args, **kwargs)

    return wrapper

def superuser_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        return view(request, *args, **kwargs)

    return wrapper