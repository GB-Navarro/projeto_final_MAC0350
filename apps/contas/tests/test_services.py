import pytest
from django.urls import reverse
from apps.contas import services

@pytest.mark.django_db
class TestAprovacaoAdministrador:
    def test_superuser_aprova_administrador_pendente(
        self,
        superuser,
        admin_pendente,
    ):
        services.aprovar_administrador(
            admin_pendente,
            superuser,
        )

        admin_pendente.refresh_from_db()

        assert admin_pendente.aprovado is True
        assert admin_pendente.aprovado_por == superuser
        assert admin_pendente.aprovado_em is not None
    
    def test_aprovacao_nao_altera_admin_ja_aprovado(
        self,
        superuser,
        admin_aprovado,
    ):
        aprovado_por = admin_aprovado.aprovado_por
        aprovado_em = admin_aprovado.aprovado_em

        services.aprovar_administrador(
            admin_aprovado,
            superuser,
        )

        admin_aprovado.refresh_from_db()

        assert admin_aprovado.aprovado is True
        assert admin_aprovado.aprovado_por == aprovado_por
        assert admin_aprovado.aprovado_em == aprovado_em