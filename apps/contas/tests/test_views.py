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

@pytest.mark.django_db
class TestLoginView:
    def test_aluno_faz_login_com_sucesso(
        self,
        client,
        aluno,
    ):
        response = client.post(
            reverse("contas:login"),
            {
                "email": aluno.usuario.email,
                "senha": "senha123",
            },
        )

        assert response.status_code == 302
        assert response.url == "/aluno/"

        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user == aluno.usuario

    def test_admin_aprovado_faz_login_com_sucesso(
        self,
        client,
        admin_aprovado,
    ):
        response = client.post(
            reverse("contas:login"),
            {
                "email": admin_aprovado.usuario.email,
                "senha": "senha123",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("questoes:lista")

        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user == admin_aprovado.usuario

    def test_admin_pendente_nao_consegue_logar(
        self,
        client,
        admin_pendente,
    ):
        response = client.post(
            reverse("contas:login"),
            {
                "email": admin_pendente.usuario.email,
                "senha": "senha123",
            },
        )

        assert response.status_code == 200

        assert not response.wsgi_request.user.is_authenticated

    def test_login_com_senha_errada_falha(
        self,
        client,
        aluno,
    ):
        response = client.post(
            reverse("contas:login"),
            {
                "email": aluno.usuario.email,
                "senha": "senha_errada",
            },
        )

        assert response.status_code == 200

        assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
class TestTelaLogin:
    def test_tela_login_renderiza_formulario(
        self,
        client,
    ):
        response = client.get(
            reverse("contas:login"),
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert 'name="email"' in html
        assert 'name="senha"' in html
        assert "Entrar" in html
    
    def test_login_invalido_exibe_mensagem_erro(
        self,
        client,
        aluno,
    ):
        response = client.post(
            reverse("contas:login"),
            {
                "email": aluno.usuario.email,
                "senha": "senha_errada",
            },
            follow=True,
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert "Email ou senha incorretos." in html

@pytest.mark.django_db
class TestAprovacaoAdministrador:
    def test_superuser_pode_aprovar(
        self,
        client_superuser,
        admin_pendente,
    ):
        response = client_superuser.client.post(
            reverse(
                "contas:aprovar_administrador",
                args=[admin_pendente.id],
            )
        )

        assert response.status_code == 302

    def test_admin_comum_nao_pode_aprovar(
        self,
        client_admin,
        admin_pendente,
    ):
        response = client_admin.client.post(
            reverse(
                "contas:aprovar_administrador",
                args=[admin_pendente.id],
            )
        )

        assert response.status_code == 403

        admin_pendente.refresh_from_db()

        assert admin_pendente.aprovado is False
        assert admin_pendente.aprovado_por is None
        assert admin_pendente.aprovado_em is None

    def test_admin_aprovado_passa_a_logar(
        self,
        client_superuser,
        admin_pendente,
    ):

        client_superuser.client.post(
            reverse(
                "contas:aprovar_administrador",
                args=[admin_pendente.id],
            )
        )

        client_superuser.client.logout()

        response = client_superuser.client.post(
            reverse("contas:login"),
            {
                "email": admin_pendente.usuario.email,
                "senha": "senha123",
            },
        )

        assert response.status_code == 302

@pytest.mark.django_db
class TestAdministradoresPendentes:

    def test_superuser_visualiza_admins_pendentes(
        self,
        client_superuser,
        admin_pendente,
    ):
        response = client_superuser.client.get(
            reverse("contas:administradores_pendentes")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert admin_pendente.usuario.email in html

    def test_superuser_aprova_admin_pendente_pela_tela(
        self,
        client_superuser,
        admin_pendente,
    ):
        response = client_superuser.client.post(
            reverse(
                "contas:aprovar_administrador",
                args=[admin_pendente.id],
            )
        )

        assert response.status_code == 302

        admin_pendente.refresh_from_db()

        assert admin_pendente.aprovado is True
    
    def test_admin_comum_nao_acessa_tela_de_pendentes(
        self,
        client_admin,
    ):
        response = client_admin.client.get(
            reverse("contas:administradores_pendentes")
        )

        assert response.status_code == 403

@pytest.mark.django_db
class TestAreaAluno:
    def test_aluno_logado_acessa_area_aluno(
        self,
        client_aluno,
    ):
        response = client_aluno.client.get(
            reverse("contas:area_aluno")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert "Área do aluno" in html

    def test_usuario_nao_autenticado_nao_acessa_area_aluno(
        self,
        client,
    ):
        response = client.get(
            reverse("contas:area_aluno")
        )

        assert response.status_code == 302

        assert "/login/" in response.url

    def test_aluno_nao_ve_informacoes_administrativas(
        self,
        client_aluno,
    ):
        response = client_aluno.client.get(
            reverse("contas:area_aluno")
        )

        html = response.content.decode()

        assert "Aprovar administrador" not in html
        assert "Administradores pendentes" not in html

    def test_aluno_visualiza_seu_codigo(
        self,
        client_aluno,
    ):
        response = client_aluno.client.get(
            reverse("contas:area_aluno")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert client_aluno.usuario.aluno.codigo in html