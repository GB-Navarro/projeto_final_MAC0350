from django.urls import path

from apps.contas import views

app_name = 'contas'

urlpatterns = [
    path("cadastro/aluno/", views.cadastro_aluno, name="cadastro_aluno"),
]
