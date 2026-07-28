import pytest
from django.urls import reverse
from model_bakery import baker

from apps.questoes.models import Questao


@pytest.mark.django_db
class TestCriarQuestaoView:

    def test_admin_logado_cria_questao_dissertativa(self, client):
        # Arrange
        admin_usuario = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        baker.make(
            "contas.Administrador",
            usuario=admin_usuario,
            aprovado=True,
        )

        client.force_login(admin_usuario)

        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a fotossíntese.",
            "solucao": "Processo realizado pelas plantas.",
        }

        # Act
        response = client.post(
            reverse("questoes:criar_questao"),
            dados,
        )

        # Assert
        assert response.status_code == 302

        questao = Questao.objects.get(
            enunciado=dados["enunciado"]
        )

        assert questao.criado_por == admin_usuario


@pytest.mark.django_db
class TestListarQuestoesView:

    def test_admin_logado_consulta_questoes(self, client):
        # Arrange
        admin_usuario = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        baker.make(
            "contas.Administrador",
            usuario=admin_usuario,
            aprovado=True,
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=admin_usuario,
        )

        client.force_login(admin_usuario)

        # Act
        response = client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200
        assert questao in response.context["questoes"]
    
    def test_listagem_exibe_dados_de_revisao(self, client):
        # Arrange
        admin_usuario = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        baker.make(
            "contas.Administrador",
            usuario=admin_usuario,
            aprovado=True,
        )

        revisor = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=admin_usuario,
            revisado_por=revisor,
            revisado_em="2026-07-28T12:00:00Z",
        )

        client.force_login(admin_usuario)

        # Act
        response = client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200

        questao_listada = response.context["questoes"].get(
            id=questao.id
        )

        assert questao_listada.revisado_por == revisor
        assert questao_listada.revisado_em is not None