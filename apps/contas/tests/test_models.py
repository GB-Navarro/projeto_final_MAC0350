import pytest
from model_bakery import baker

from apps.contas.models import Usuario


@pytest.mark.django_db
def test_usuario_usa_email_como_login():
    # Arrange / Act
    usuario = baker.make(Usuario, email="ana@exemplo.com")

    # Assert
    assert Usuario.USERNAME_FIELD == "email"
    assert not hasattr(usuario, "username") or usuario.username is None


@pytest.mark.django_db
def test_aluno_campos_obrigatorios():
    # Arrange / Act
    aluno = baker.make(
        "contas.Aluno",
        genero="F",
        serie="1EM",
        escola="Escola X",
        tipo_escola="PUBLICA",
    )

    # Assert
    assert aluno.genero == "F"
    assert aluno.serie == "1EM"
    assert aluno.escola == "Escola X"
    assert aluno.tipo_escola == "PUBLICA"


@pytest.mark.django_db
def test_aluno_campos_opcionais_nulos_por_padrao():
    # Arrange / Act
    aluno = baker.make("contas.Aluno", professor_nome=None, professor_email=None)

    # Assert
    assert aluno.professor_nome is None
    assert aluno.professor_email is None


@pytest.mark.django_db
def test_aluno_codigo_no_formato_correto():
    # Arrange / Act
    aluno = baker.make("contas.Aluno")

    # Assert
    assert aluno.codigo.startswith("E")
    assert len(aluno.codigo) == 7


@pytest.mark.django_db
def test_aluno_codigo_unico():
    # Arrange / Act
    aluno1 = baker.make("contas.Aluno")
    aluno2 = baker.make("contas.Aluno")

    # Assert
    assert aluno1.codigo != aluno2.codigo


@pytest.mark.django_db
def test_administrador_nasce_pendente():
    # Arrange / Act
    admin = baker.make("contas.Administrador")

    # Assert
    assert admin.aprovado is False
    assert admin.aprovado_por is None
    assert admin.aprovado_em is None
