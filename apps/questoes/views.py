from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.questoes import services

# Create your views here.

@login_required
def criar_questao(request):
    if request.method == "POST":
        services.criar_questao(request.user, request.POST)
        return redirect("questoes:lista")

    return render(request, "questoes/form_questao.html")


# Placeholder !!!
@login_required
def lista(request):
    return render(request, "questoes/lista.html")