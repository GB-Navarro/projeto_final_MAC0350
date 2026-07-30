from django.urls import path

from apps.contas import views

app_name = 'contas'

urlpatterns = [
    path("cadastro/aluno/", views.cadastro_aluno, name="cadastro_aluno"),
    path("cadastro/administrador/", views.cadastro_administrador, name="cadastro_administrador"),
    path(
        "login/",
        views.login_usuario,
        name="login",
    ),
    path(
        "logout/",
        views.logout_usuario,
        name="logout",
    ),
    path(
        "administradores/<int:id>/aprovar/",
        views.aprovar_administrador,
        name="aprovar_administrador",
    ),
    path(
        "administradores/pendentes/",
        views.administradores_pendentes,
        name="administradores_pendentes",
    ),
]
