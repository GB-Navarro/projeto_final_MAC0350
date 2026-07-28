from django.urls import path

from apps.questoes import views

app_name = 'questoes'

urlpatterns = [
    path(
        "questoes/nova/",
        views.criar_questao,
        name="criar_questao",
    ),
    path(
        "questoes/<int:id>/revisar/",
        views.revisar_questao,
        name="revisar",
    ),
    path(
        "questoes/",
        views.lista,
        name="lista",
    ),
]
