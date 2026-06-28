from django.urls import path, include

urlpatterns = [
    path('', include('apps.contas.urls')),
    path('adm/', include('apps.questoes.urls')),
]
