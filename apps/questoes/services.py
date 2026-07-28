from django.utils import timezone

from apps.questoes.models import Questao

def criar_questao(usuario, dados):
    return Questao.objects.create(
        criado_por=usuario,
        tipo=dados["tipo"],
        enunciado=dados["enunciado"],
        solucao=dados["solucao"],
        alternativas=dados.get("alternativas"),
        gabarito=dados.get("gabarito"),
    )

def revisar_questao(questao, usuario):
    questao.revisado_por = usuario
    questao.revisado_em = timezone.now()
    questao.save()

    return questao