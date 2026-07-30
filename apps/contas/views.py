from django.shortcuts import redirect, render, get_object_or_404

from apps.contas.decorators import superuser_required
from apps.contas.forms import CadastroAlunoForm, CadastroAdministradorForm
from apps.contas import services
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.contas.models import Usuario, Administrador

def cadastro_aluno(request):
    if request.method == "POST":
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            services.cadastrar_aluno(form.cleaned_data)
            return redirect("/")
    else:
        form = CadastroAlunoForm()
    return render(request, "contas/cadastro_aluno.html", {"form": form})

def cadastro_administrador(request):
    if request.method == "POST":
        form = CadastroAdministradorForm(request.POST)
        if form.is_valid():
            services.cadastrar_administrador(form.cleaned_data)
            return redirect("/")
    else:
        form = CadastroAdministradorForm()
    return render(request, "contas/cadastro_administrador.html", {"form": form})

def login_usuario(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        usuario = authenticate(
            request,
            username=email,
            password=senha,
        )

        if usuario is None:
            messages.error(
                request,
                "Email ou senha incorretos.",
            )
            return render(
                request,
                "contas/login.html",
            )

        if usuario.tipo == Usuario.ADM:
            if not usuario.administrador.aprovado:
                messages.error(
                    request,
                    "Administrador aguardando aprovação.",
                )
                return render(
                    request,
                    "contas/login.html",
                )

            login(request, usuario)
            return redirect("questoes:lista")

        if usuario.tipo == Usuario.ALUNO:
            login(request, usuario)
            return redirect("/aluno/")

    return render(
        request,
        "contas/login.html",
    )


def logout_usuario(request):
    logout(request)
    return redirect("contas:login")

@superuser_required
def aprovar_administrador(request, id):
    administrador = get_object_or_404(
        Administrador,
        id=id,
    )

    services.aprovar_administrador(
        administrador,
        request.user,
    )

    return redirect("/")

@superuser_required
def administradores_pendentes(request):
    administradores = Administrador.objects.filter(
        aprovado=False
    )

    return render(
        request,
        "contas/administradores_pendentes.html",
        {
            "administradores": administradores,
        },
    )