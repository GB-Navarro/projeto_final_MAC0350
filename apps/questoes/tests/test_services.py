from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
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

        primeiro_instante = timezone.now()
        segundo_instante = primeiro_instante + timedelta(seconds=1)

        with patch("apps.questoes.services.timezone.now", return_value=primeiro_instante):
            services.revisar_questao(
                questao,
                admin_aprovado.usuario,
            )

        primeira_revisao = questao.revisado_em

        # Act
        with patch("apps.questoes.services.timezone.now", return_value=segundo_instante):
            services.revisar_questao(
                questao,
                outro_admin_aprovado.usuario,
            )

        # Assert
        questao.refresh_from_db()

        assert questao.revisado_por == outro_admin_aprovado.usuario
        assert questao.revisado_em != primeira_revisao

@pytest.mark.django_db
class TestEditarQuestao:

    def test_admin_edita_questao_criada_por_outro_admin(
        self,
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
            "enunciado": "Enunciado novo",
            "solucao": "Solução nova",
        }

        # Act
        services.editar_questao(
            questao,
            dados,
        )

        # Assert
        questao.refresh_from_db()

        assert questao.enunciado == "Enunciado novo"
        assert questao.solucao == "Solução nova"

    def test_alterar_questao_dissertativa_para_multipla_escolha(self):
        questao = baker.make(
            "questoes.Questao",
            tipo="DISSERTATIVA",
            enunciado="Qual é a capital do Brasil?",
            solucao="Brasília.",
        )

        dados = {
            "tipo": "MULTIPLA_ESCOLHA",
            "enunciado": "Qual é a capital do Brasil?",
            "solucao": "Brasília.",
            "alternativas": [
                "São Paulo",
                "Brasília",
                "Rio de Janeiro",
            ],
            "gabarito": "B",
        }

        services.editar_questao(
            questao,
            dados,
        )

        questao.refresh_from_db()

        assert questao.tipo == "MULTIPLA_ESCOLHA"
        assert questao.alternativas == [
            "São Paulo",
            "Brasília",
            "Rio de Janeiro",
        ]
        assert questao.gabarito == "B"


    def test_alterar_questao_multipla_escolha_para_dissertativa(self):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            tipo="MULTIPLA_ESCOLHA",
            alternativas={
                "A": "São Paulo",
                "B": "Brasília",
            },
            gabarito="B",
        )

        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a resposta.",
            "solucao": "Resposta explicada.",
        }

        # Act
        services.editar_questao(
            questao,
            dados,
        )

        # Assert
        questao.refresh_from_db()

        assert questao.tipo == "DISSERTATIVA"
        assert questao.solucao == "Resposta explicada."
        assert questao.alternativas is None
        assert questao.gabarito is None