import pytest
from model_bakery import baker

from apps.questoes import services

@pytest.mark.django_db
class TestCriarQuestao:

    def test_admin_cria_questao_dissertativa_associada_a_ele(self):
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

        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a teoria da relatividade.",
            "solucao": "A teoria descreve a relação entre espaço e tempo.",
        }

        # Act
        questao = services.criar_questao(admin_usuario, dados)

        # Assert
        assert questao.criado_por == admin_usuario
        assert questao.enunciado == dados["enunciado"]

"""
Não implementado ainda, resolvendo dependências anteriores

@pytest.mark.django_db
class TestRevisaoQuestao:

    def test_revisar_registra_administrador_e_data(self):
        # Arrange
        admin = baker.make("contas.Administrador", aprovado=True)
        questao = baker.make("questoes.Questao")

        # Act
        services.marcar_como_revisada(questao, admin.usuario)

        # Assert
        questao.refresh_from_db()

        assert questao.revisado_por == admin.usuario
        assert questao.revisado_em is not None

    def test_revisar_novamente_sobrescreve_revisao_anterior(self):
        # Arrange
        admin1 = baker.make("contas.Administrador", aprovado=True)
        admin2 = baker.make("contas.Administrador", aprovado=True)
        questao = baker.make("questoes.Questao")

        services.marcar_como_revisada(questao, admin1.usuario)

        primeira_revisao = questao.revisado_em

        # Act
        services.marcar_como_revisada(questao, admin2.usuario)

        # Assert
        questao.refresh_from_db()

        assert questao.revisado_por == admin2.usuario
        assert questao.revisado_em != primeira_revisao
"""