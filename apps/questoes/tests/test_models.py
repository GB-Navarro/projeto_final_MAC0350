import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestQuestaoModel:

    def test_nova_questao_inicia_sem_revisao(self):
        # Arrange
        usuario = baker.make("contas.Usuario")

        # Act
        questao = baker.make(
            "questoes.Questao",
            criado_por=usuario,
            tipo="DISSERTATIVA",
            enunciado="Qual é a capital do Brasil?",
            solucao="Brasília.",
        )

        # Assert
        assert questao.revisado_por is None
        assert questao.revisado_em is None

    def test_questao_multipla_escolha_armazena_alternativas_e_gabarito(self):
        # Arrange

        # Act
        questao = baker.make(
            "questoes.Questao",
            tipo="MULTIPLA_ESCOLHA",
            alternativas={
                "A": "...",
                "B": "...",
                "C": "...",
                "D": "...",
                "E": "...",
            },
            gabarito="C",
        )

        # Assert
        assert questao.alternativas["C"] == "..."
        assert questao.gabarito == "C"
        assert questao.revisado_por is None
        assert questao.revisado_em is None