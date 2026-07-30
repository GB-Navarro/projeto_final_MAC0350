from django.utils import timezone
import json

from apps.questoes.models import Questao

def normalizar_alternativas(alternativas):
    if not alternativas:
        return None

    if isinstance(alternativas, str):
        return json.loads(alternativas)

    return alternativas

def criar_questao(usuario, dados):
    alternativas = dados.get("alternativas")

    if alternativas:
        alternativas = normalizar_alternativas(alternativas)

    return Questao.objects.create(
        criado_por=usuario,
        tipo=dados["tipo"],
        enunciado=dados["enunciado"],
        solucao=dados["solucao"],
        alternativas=alternativas,
        gabarito=dados.get("gabarito"),
    )

def revisar_questao(questao, usuario):
    questao.revisado_por = usuario
    questao.revisado_em = timezone.now()
    questao.save()

    return questao

def editar_questao(questao, dados):
    questao.tipo = dados["tipo"]
    questao.enunciado = dados["enunciado"]
    questao.solucao = dados["solucao"]

    if questao.tipo == "MULTIPLA_ESCOLHA":
        questao.alternativas = normalizar_alternativas(
            dados["alternativas"]
        )
        questao.gabarito = dados["gabarito"]

    else:
        questao.alternativas = None
        questao.gabarito = None

    questao.save()

    return questao