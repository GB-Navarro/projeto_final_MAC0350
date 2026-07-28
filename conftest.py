import pytest
from model_bakery import baker
from types import SimpleNamespace

@pytest.fixture
def superuser(db):
    return baker.make(
        "contas.Usuario",
        is_superuser=True,
        is_staff=True,
        tipo="ADM",
    )


@pytest.fixture
def admin_aprovado(db):
    usuario = baker.make(
        "contas.Usuario",
        tipo="ADM",
    )

    return baker.make(
        "contas.Administrador",
        usuario=usuario,
        aprovado=True,
    )


@pytest.fixture
def client_admin(client, admin_aprovado):
    client.force_login(admin_aprovado.usuario)

    return SimpleNamespace(
        client=client,
        usuario=admin_aprovado.usuario,
    )

@pytest.fixture
def outro_admin_aprovado(db):
    usuario = baker.make(
        "contas.Usuario",
        tipo="ADM",
    )

    return baker.make(
        "contas.Administrador",
        usuario=usuario,
        aprovado=True,
    )


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
