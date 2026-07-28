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