import uuid

from apps.contas.models import Aluno


def gerar_codigo_aluno() -> str:
    for _ in range(5):
        codigo = "E" + uuid.uuid4().hex[:6]
        if not Aluno.objects.filter(codigo=codigo).exists():
            return codigo
    raise RuntimeError("Não foi possível gerar um código único para o aluno após 5 tentativas.")
