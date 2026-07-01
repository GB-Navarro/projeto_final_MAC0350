from django.shortcuts import redirect, render

from apps.contas.forms import CadastroAlunoForm, CadastroAdministradorForm
from apps.contas.services import cadastrar_aluno, cadastrar_administrador


def cadastro_aluno(request):
    if request.method == "POST":
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            cadastrar_aluno(form.cleaned_data)
            return redirect("/")
    else:
        form = CadastroAlunoForm()
    return render(request, "contas/cadastro_aluno.html", {"form": form})

def cadastro_administrador(request):
    if request.method == "POST":
        form = CadastroAdministradorForm(request.POST)
        if form.is_valid():
            cadastrar_administrador(form.cleaned_data)
            return redirect("/")
    else:
        form = CadastroAdministradorForm()
    return render(request, "contas/cadastro_administrador.html", {"form": form})
