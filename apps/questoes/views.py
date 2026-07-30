from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, redirect

from apps.contas.decorators import admin_required
from apps.questoes.models import Questao
from apps.questoes import services

# Create your views here.

@admin_required
def criar_questao(request):
    if request.method == "POST":
        services.criar_questao(request.user, request.POST)
        return redirect("questoes:lista")

    return render(request, "questoes/formulario.html")

@admin_required
def revisar_questao(request, id):
    questao = get_object_or_404(Questao, id=id)

    services.revisar_questao(
        questao,
        request.user,
    )

    return redirect("questoes:lista")

@admin_required
def lista(request):
    questoes = Questao.objects.all()

    return render(
        request,
        "questoes/lista.html",
        {
            "questoes": questoes,
        },
    )

@admin_required
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