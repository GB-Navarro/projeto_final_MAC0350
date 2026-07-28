import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from apps.contas.models import Administrador, Aluno, Usuario

DADOS_VALIDOS = {
    "nome": "Ana Silva",
    "email": "ana@exemplo.com",
    "senha": "senha-forte-123",
    "genero": "F",
    "serie": "1EM",
    "escola": "Escola X",
    "tipo_escola": "PUBLICA",
}


def criar_usuario(
    email,
    *,
    is_superuser=False,
    is_staff=False,
):
    usuario = Usuario(
        email=email,
        first_name="Usuario Teste",
        tipo=Usuario.ADM,
        is_superuser=is_superuser,
        is_staff=is_staff,
    )
    usuario.set_password("senha-forte-123")
    usuario.save()
    return usuario


def criar_administrador(email="admin@exemplo.com", *, aprovado=False):
    usuario = criar_usuario(email)
    return Administrador.objects.create(usuario=usuario, aprovado=aprovado)


@pytest.mark.django_db
def test_cadastro_valido_cria_usuario_e_aluno(client):
    # Arrange
    url = reverse("contas:cadastro_aluno")

    # Act
    client.post(url, DADOS_VALIDOS)

    # Assert
    usuario = Usuario.objects.get(email="ana@exemplo.com")
    assert usuario.tipo == Usuario.ALUNO
    assert usuario.check_password("senha-forte-123")

    aluno = Aluno.objects.get(usuario=usuario)
    assert aluno.codigo.startswith("E")
    assert len(aluno.codigo) == 7


@pytest.mark.django_db
def test_cadastro_valido_redireciona(client):
    # Arrange
    url = reverse("contas:cadastro_aluno")

    # Act
    response = client.post(url, DADOS_VALIDOS)

    # Assert
    assert response.status_code == 302


@pytest.mark.django_db
def test_email_duplicado_nao_cria_nada(client):
    # Arrange
    baker.make(Usuario, email="ana@exemplo.com")
    url = reverse("contas:cadastro_aluno")
    quantidade_antes = Usuario.objects.count()

    # Act
    response = client.post(url, DADOS_VALIDOS)

    # Assert
    assert Usuario.objects.count() == quantidade_antes
    assert response.status_code == 200


@pytest.mark.django_db
def test_campo_obrigatorio_ausente_nao_cria_nada(client):
    # Arrange
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS.items() if k != "email"}
    url = reverse("contas:cadastro_aluno")

    # Act
    response = client.post(url, dados_sem_email)

    # Assert
    assert Usuario.objects.count() == 0
    assert response.status_code == 200


# --- F1-4: Frontend ---


@pytest.mark.django_db
def test_get_cadastro_aluno_exibe_formulario_com_campos(client):
    # Arrange
    url = reverse("contas:cadastro_aluno")

    # Act
    response = client.get(url)
    html = response.content.decode()

    # Assert
    assert response.status_code == 200
    assert 'name="nome"' in html
    assert 'name="email"' in html
    assert 'name="senha"' in html
    assert 'name="genero"' in html
    assert 'name="serie"' in html
    assert 'name="escola"' in html
    assert 'name="tipo_escola"' in html


@pytest.mark.django_db
def test_erro_de_validacao_exibe_mensagem_visivel(client):
    # Arrange
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS.items() if k != "email"}
    url = reverse("contas:cadastro_aluno")

    # Act
    response = client.post(url, dados_sem_email)
    html = response.content.decode()

    # Assert
    assert response.status_code == 200
    assert "errorlist" in html


# --- F1-7: Aprovacao de administrador ---


@pytest.mark.django_db
def test_superuser_aprova_administrador_pendente(client):
    # Arrange
    superuser = criar_usuario(
        "root@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    administrador = criar_administrador("pendente@exemplo.com")
    client.force_login(superuser)
    url = reverse("contas:aprovar_administrador", args=[administrador.id])

    # Act
    response = client.post(url)

    # Assert
    administrador.refresh_from_db()
    assert 200 <= response.status_code < 400
    assert administrador.aprovado is True
    assert administrador.aprovado_por == superuser
    assert administrador.aprovado_em is not None


@pytest.mark.django_db
def test_admin_comum_recebe_403_e_nao_aprova(client):
    # Arrange
    admin_comum = criar_administrador(
        "admin-comum@exemplo.com",
        aprovado=True,
    )
    pendente = criar_administrador("pendente@exemplo.com")
    client.force_login(admin_comum.usuario)
    url = reverse("contas:aprovar_administrador", args=[pendente.id])

    # Act
    response = client.post(url)

    # Assert
    pendente.refresh_from_db()
    assert response.status_code == 403
    assert pendente.aprovado is False
    assert pendente.aprovado_por is None
    assert pendente.aprovado_em is None


@pytest.mark.django_db
def test_usuario_anonimo_nao_aprova(client):
    # Arrange
    pendente = criar_administrador("pendente@exemplo.com")
    url = reverse("contas:aprovar_administrador", args=[pendente.id])

    # Act
    response = client.post(url)

    # Assert
    pendente.refresh_from_db()
    assert response.status_code == 302
    assert response.url.startswith("/login/")
    assert pendente.aprovado is False
    assert pendente.aprovado_por is None
    assert pendente.aprovado_em is None


@pytest.mark.django_db
def test_aprovacao_aceita_somente_post(client):
    # Arrange
    superuser = criar_usuario(
        "root@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    pendente = criar_administrador("pendente@exemplo.com")
    client.force_login(superuser)
    url = reverse("contas:aprovar_administrador", args=[pendente.id])

    # Act
    response = client.get(url)

    # Assert
    pendente.refresh_from_db()
    assert response.status_code == 405
    assert pendente.aprovado is False


@pytest.mark.django_db
def test_aprovacao_de_id_inexistente_retorna_404(client):
    # Arrange
    superuser = criar_usuario(
        "root@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    client.force_login(superuser)
    url = reverse("contas:aprovar_administrador", args=[999_999])

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404


@pytest.mark.django_db
def test_aprovacao_sem_csrf_retorna_403():
    # Arrange
    client = Client(enforce_csrf_checks=True)
    superuser = criar_usuario(
        "root@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    pendente = criar_administrador("pendente@exemplo.com")
    client.force_login(superuser)
    url = reverse("contas:aprovar_administrador", args=[pendente.id])

    # Act
    response = client.post(url)

    # Assert
    pendente.refresh_from_db()
    assert response.status_code == 403
    assert pendente.aprovado is False


@pytest.mark.django_db
def test_aprovacao_repetida_preserva_primeira_auditoria(client):
    # Arrange
    primeiro_superuser = criar_usuario(
        "root-1@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    segundo_superuser = criar_usuario(
        "root-2@exemplo.com",
        is_superuser=True,
        is_staff=True,
    )
    administrador = criar_administrador("pendente@exemplo.com")
    url = reverse("contas:aprovar_administrador", args=[administrador.id])

    client.force_login(primeiro_superuser)
    primeira_resposta = client.post(url)
    administrador.refresh_from_db()
    primeira_data = administrador.aprovado_em

    # Act
    client.force_login(segundo_superuser)
    segunda_resposta = client.post(url)

    # Assert
    administrador.refresh_from_db()
    assert 200 <= primeira_resposta.status_code < 400
    assert 200 <= segunda_resposta.status_code < 400
    assert administrador.aprovado is True
    assert administrador.aprovado_por == primeiro_superuser
    assert administrador.aprovado_em == primeira_data
