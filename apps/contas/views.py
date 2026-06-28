from django.shortcuts import redirect, render

from apps.contas.forms import CadastroAlunoForm
from apps.contas.services import cadastrar_aluno


def cadastro_aluno(request):
    if request.method == "POST":
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            cadastrar_aluno(form.cleaned_data)
            return redirect("/")
    else:
        form = CadastroAlunoForm()
    return render(request, "contas/cadastro_aluno.html", {"form": form})
