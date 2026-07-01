import pytest
from django.urls import reverse
from model_bakery import baker

from apps.contas.models import Administrador, Aluno, Usuario

DADOS_VALIDOS_ALUNO = {
    "nome": "Ana Silva",
    "email": "ana@exemplo.com",
    "senha": "senha-forte-123",
    "genero": "F",
    "serie": "1EM",
    "escola": "Escola X",
    "tipo_escola": "PUBLICA",
}

DADOS_VALIDOS_ADMINISTRADOR = {
    "nome": "Carlos Souza",
    "email": "carlos@exemplo.com",
    "senha": "senha-forte-123",
}


# --- Aluno ---


@pytest.mark.django_db
def test_cadastro_valido_cria_usuario_e_aluno(client):
    # Arrange
    url = reverse("contas:cadastro_aluno")

    # Act
    client.post(url, DADOS_VALIDOS_ALUNO)

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
    response = client.post(url, DADOS_VALIDOS_ALUNO)

    # Assert
    assert response.status_code == 302


@pytest.mark.django_db
def test_email_duplicado_nao_cria_nada_aluno(client):
    # Arrange
    baker.make(Usuario, email="ana@exemplo.com")
    url = reverse("contas:cadastro_aluno")
    quantidade_antes = Usuario.objects.count()

    # Act
    response = client.post(url, DADOS_VALIDOS_ALUNO)

    # Assert
    assert Usuario.objects.count() == quantidade_antes
    assert response.status_code == 200


@pytest.mark.django_db
def test_campo_obrigatorio_ausente_nao_cria_nada_aluno(client):
    # Arrange
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS_ALUNO.items() if k != "email"}
    url = reverse("contas:cadastro_aluno")
    quantidade_antes = Usuario.objects.count()

    # Act
    response = client.post(url, dados_sem_email)

    # Assert
    assert Usuario.objects.count() == quantidade_antes
    assert response.status_code == 200


# --- Aluno: F1-4 Frontend ---


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
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS_ALUNO.items() if k != "email"}
    url = reverse("contas:cadastro_aluno")

    # Act
    response = client.post(url, dados_sem_email)
    html = response.content.decode()

    # Assert
    assert response.status_code == 200
    assert "errorlist" in html


# --- Administrador ---


@pytest.mark.django_db
def test_cadastro_com_dados_validos_cria_usuario_e_administrador(client):
    # Arrange
    url = reverse("contas:cadastro_administrador")

    # Act
    client.post(url, DADOS_VALIDOS_ADMINISTRADOR)

    # Assert
    usuario = Usuario.objects.get(email="carlos@exemplo.com")
    assert usuario.tipo == Usuario.ADM
    assert usuario.check_password("senha-forte-123")

    administrador = Administrador.objects.get(usuario=usuario)
    assert administrador.aprovado is False


@pytest.mark.django_db
def test_cadastro_redireciona_apos_sucesso(client):
    # Arrange
    url = reverse("contas:cadastro_administrador")

    # Act
    response = client.post(url, DADOS_VALIDOS_ADMINISTRADOR)

    # Assert
    assert response.status_code == 302


@pytest.mark.django_db
def test_email_duplicado_nao_cria_nada_administrador(client):
    # Arrange
    baker.make(Usuario, email="carlos@exemplo.com")
    url = reverse("contas:cadastro_administrador")
    quantidade_antes = Usuario.objects.count()

    # Act
    response = client.post(url, DADOS_VALIDOS_ADMINISTRADOR)

    # Assert
    assert Usuario.objects.count() == quantidade_antes
    assert response.status_code == 200
    assert "errorlist" in response.content.decode()


@pytest.mark.django_db
def test_campo_obrigatorio_ausente_nao_cria_nada_administrador(client):
    # Arrange
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS_ADMINISTRADOR.items() if k != "email"}
    url = reverse("contas:cadastro_administrador")
    quantidade_antes = Usuario.objects.count()

    # Act
    response = client.post(url, dados_sem_email)

    # Assert
    assert Usuario.objects.count() == quantidade_antes
    assert response.status_code == 200
    assert "errorlist" in response.content.decode()


# --- Administrador: F1-6 Frontend ---


@pytest.mark.django_db
def test_get_cadastro_administrador_exibe_formulario_com_todos_os_campos(client):
    # Arrange
    url = reverse("contas:cadastro_administrador")

    # Act
    response = client.get(url)
    html = response.content.decode()

    # Assert
    assert response.status_code == 200
    assert 'name="nome"' in html
    assert 'name="email"' in html
    assert 'name="senha"' in html


@pytest.mark.django_db
def test_erro_de_validacao_exibe_mensagem_visivel_no_cadastro_administrador(client):
    # Arrange
    dados_sem_email = {k: v for k, v in DADOS_VALIDOS_ADMINISTRADOR.items() if k != "email"}
    url = reverse("contas:cadastro_administrador")

    # Act
    response = client.post(url, dados_sem_email)
    html = response.content.decode()

    # Assert
    assert response.status_code == 200
    assert "errorlist" in html
