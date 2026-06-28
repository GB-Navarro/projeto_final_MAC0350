import uuid

from apps.contas.models import Aluno, Usuario


def gerar_codigo_aluno() -> str:
    for _ in range(5):
        codigo = "E" + uuid.uuid4().hex[:6]
        if not Aluno.objects.filter(codigo=codigo).exists():
            return codigo
    raise RuntimeError("Não foi possível gerar um código único para o aluno após 5 tentativas.")


def cadastrar_aluno(dados: dict) -> Aluno:
    usuario = Usuario(
        email=dados["email"],
        first_name=dados.get("nome", ""),
        tipo=Usuario.ALUNO,
    )
    usuario.set_password(dados["senha"])
    usuario.save()

    aluno = Aluno(
        usuario=usuario,
        genero=dados["genero"],
        serie=dados["serie"],
        escola=dados["escola"],
        tipo_escola=dados["tipo_escola"],
        professor_nome=dados.get("professor_nome") or None,
        professor_email=dados.get("professor_email") or None,
    )
    aluno.save()

    return aluno
