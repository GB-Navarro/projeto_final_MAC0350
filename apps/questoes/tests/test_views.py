import pytest
from django.urls import reverse
from model_bakery import baker
from django.utils import timezone

from apps.questoes.models import Questao


@pytest.mark.django_db
class TestCriarQuestaoView:

    def test_admin_logado_cria_questao_dissertativa(
        self,
        client_admin,
    ):
        # Arrange
        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a fotossíntese.",
            "solucao": "Processo realizado pelas plantas.",
        }

        # Act
        response = client_admin.client.post(
            reverse("questoes:criar_questao"),
            dados,
        )

        # Assert
        assert response.status_code == 302

        questao = Questao.objects.get(
            enunciado=dados["enunciado"]
        )

        assert questao.criado_por == client_admin.usuario

@pytest.mark.django_db
class TestListarQuestoesView:

    def test_admin_logado_consulta_questoes(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200
        assert questao in response.context["questoes"]
    
    def test_listagem_exibe_dados_de_revisao(
        self,
        client_admin,
    ):
        # Arrange
        revisor = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            revisado_por=revisor,
            revisado_em=timezone.now(),
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200

        questao_listada = response.context["questoes"].get(
            id=questao.id
        )

        assert questao_listada.revisado_por == revisor
        assert questao_listada.revisado_em is not None

@pytest.mark.django_db
class TestTelaListagemQuestoes:

    def test_tela_exibe_questoes(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            enunciado="Qual é a capital do Brasil?",
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200
        assert questao.enunciado.encode() in response.content
    
    def test_tela_exibe_informacoes_de_revisao(
        self,
        client_admin,
    ):
        # Arrange
        revisor = baker.make(
            "contas.Usuario",
            tipo="ADM",
            first_name="João",
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            enunciado="Questão revisada",
            revisado_por=revisor,
            revisado_em=timezone.now(),
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        html = response.content.decode()

        assert "Revisada por" in html
        assert "João" in html

@pytest.mark.django_db
class TestEditarQuestaoView:

    def test_admin_edita_questao_de_outro_admin(
        self,
        client_admin,
        outro_admin_aprovado,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=outro_admin_aprovado.usuario,
            tipo="DISSERTATIVA",
            enunciado="Enunciado antigo",
            solucao="Solução antiga",
        )

        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Enunciado atualizado",
            "solucao": "Solução atualizada",
        }

        # Act
        response = client_admin.client.post(
            reverse("questoes:editar_questao", args=[questao.id]),
            dados,
        )

        # Assert
        assert response.status_code == 302

        questao.refresh_from_db()

        assert questao.enunciado == "Enunciado atualizado"
        assert questao.solucao == "Solução atualizada"

@pytest.mark.django_db
class TestRevisarQuestaoTela:

    def test_tela_exibe_status_da_revisao(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
        )

        # Antes da revisão
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        html = response.content.decode()

        assert "Não revisada" in html
        assert "Revisada por" not in html
        assert "Marcar como revisada" in html

        # Act
        client_admin.client.post(
            reverse("questoes:revisar", args=[questao.id]),
        )

        # Depois da revisão
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        html = response.content.decode()

        questao.refresh_from_db()

        # Assert
        assert "Não revisada" not in html
        assert "Revisada por" in html
        assert "Marcar como revisada" not in html

        nome_ou_email = (
            client_admin.usuario.first_name
            or client_admin.usuario.email
        )

        assert nome_ou_email in html
        assert str(questao.revisado_em.year) in html