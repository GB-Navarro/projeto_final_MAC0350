import pytest
from model_bakery import baker

from apps.questoes import services

@pytest.mark.django_db
class TestCriarQuestao:

    def test_admin_cria_questao_dissertativa_associada_a_ele(
        self,
        admin_aprovado,
    ):
        # Arrange
        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a teoria da relatividade.",
            "solucao": "A teoria descreve a relação entre espaço e tempo.",
        }

        # Act
        questao = services.criar_questao(
            admin_aprovado.usuario,
            dados,
        )

        # Assert
        assert questao.criado_por == admin_aprovado.usuario
        assert questao.enunciado == dados["enunciado"]

@pytest.mark.django_db
class TestRevisaoQuestao:

    def test_revisar_registra_administrador_e_data(self, admin_aprovado):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=admin_aprovado.usuario,
        )

        # Act
        services.revisar_questao(
            questao,
            admin_aprovado.usuario,
        )

        # Assert
        questao.refresh_from_db()

        assert questao.revisado_por == admin_aprovado.usuario
        assert questao.revisado_em is not None

    def test_revisar_novamente_sobrescreve_revisao_anterior(
        self,
        admin_aprovado,
        outro_admin_aprovado,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=admin_aprovado.usuario,
        )

        services.revisar_questao(
            questao,
            admin_aprovado.usuario,
        )

        primeira_revisao = questao.revisado_em

        # Act
        services.revisar_questao(
            questao,
            outro_admin_aprovado.usuario,
        )

        # Assert
        questao.refresh_from_db()

        assert questao.revisado_por == outro_admin_aprovado.usuario
        assert questao.revisado_em != primeira_revisao