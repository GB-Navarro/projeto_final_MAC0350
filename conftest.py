import pytest
from model_bakery import baker


@pytest.fixture
def superuser(db):
    return baker.make("contas.Usuario", is_superuser=True, is_staff=True, tipo="ADM")


# Adicione fixtures aqui à medida que os modelos forem criados. Padrão:
#
# @pytest.fixture
# def admin_aprovado(db):
#     return baker.make("contas.Administrador", aprovado=True)
#
# @pytest.fixture
# def client_admin(client, admin_aprovado):
#     client.force_login(admin_aprovado.usuario)
#     return client
#
# @pytest.fixture
# def aluno(db):
#     return baker.make("contas.Aluno")
#
# @pytest.fixture
# def client_aluno(client, aluno):
#     client.force_login(aluno.usuario)
#     return client
