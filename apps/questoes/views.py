from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, redirect

from apps.questoes.models import Questao
from apps.questoes import services

# Create your views here.

@login_required
def criar_questao(request):
    if request.method == "POST":
        services.criar_questao(request.user, request.POST)
        return redirect("questoes:lista")

    return render(request, "questoes/formulario.html")


# Placeholder !!!
@login_required
def lista(request):
    return render(request, "questoes/lista.html")


@login_required
def revisar_questao(request, id):
    questao = get_object_or_404(Questao, id=id)

    services.revisar_questao(
        questao,
        request.user,
    )

    return redirect("questoes:lista")

@login_required
def lista(request):
    questoes = Questao.objects.all()

    return render(
        request,
        "questoes/lista.html",
        {
            "questoes": questoes,
        },
    )

@login_required
def editar_questao(request, id):
    questao = get_object_or_404(
        Questao,
        id=id,
    )

    if request.method == "POST":
        services.editar_questao(
            questao,
            request.POST,
        )

        return redirect("questoes:lista")

    return render(
        request,
        "questoes/formulario.html",
        {"questao": questao},
    )