import pytest
from model_bakery import baker
from types import SimpleNamespace
from django.utils import timezone

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
        email="adm@email.com",
        tipo="ADM",
    )

    usuario.set_password("senha123")
    usuario.save()

    return baker.make(
        "contas.Administrador",
        usuario=usuario,
        aprovado=True,
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

@pytest.fixture
def aluno(db):
    usuario = baker.make(
        "contas.Usuario",
        email="aluno@email.com",
        tipo="ALUNO",
    )
    usuario.set_password("senha123")
    usuario.save()

    return baker.make(
        "contas.Aluno",
        usuario=usuario,
    )


@pytest.fixture
def admin_pendente(db):
    usuario = baker.make(
        "contas.Usuario",
        email="adm_pendente@email.com",
        tipo="ADM",
    )

    usuario.set_password("senha123")
    usuario.save()

    return baker.make(
        "contas.Administrador",
        usuario=usuario,
        aprovado=False,
    )

@pytest.fixture
def client_admin(client, admin_aprovado):
    client.force_login(admin_aprovado.usuario)

    return SimpleNamespace(
        client=client,
        usuario=admin_aprovado.usuario,
    )

@pytest.fixture
def client_aluno(client, aluno):
    client.force_login(aluno.usuario)

    return SimpleNamespace(
        client=client,
        usuario=aluno.usuario,
    )

@pytest.fixture
def client_superuser(client, superuser):
    client.force_login(superuser)

    return SimpleNamespace(
        client=client,
        usuario=superuser,
    )

@pytest.fixture
def questao(db):
    return baker.make(
        "questoes.Questao",
        tipo="DISSERTATIVA",
        enunciado="Enunciado original",
        solucao="Solução original",
    )


@pytest.fixture
def questao_revisada(questao, admin_aprovado):
    questao.revisado_por = admin_aprovado.usuario
    questao.revisado_em = timezone.now()
    questao.save()

    return questao

@pytest.fixture
def questao_multipla(db):
    return baker.make(
        "questoes.Questao",
        tipo="MULTIPLA_ESCOLHA",
        enunciado="Questão múltipla",
        solucao="Solução original",
        alternativas=[
            "Primeira alternativa",
            "Segunda alternativa",
            "Terceira alternativa",
        ],
        gabarito="A",
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
