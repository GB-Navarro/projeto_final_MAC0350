from django.utils import timezone
import json

from apps.questoes.models import Questao

def normalizar_alternativas(alternativas):
    if not alternativas:
        return None

    if isinstance(alternativas, str):
        alternativas = json.loads(alternativas)

    return alternativas

def criar_questao(usuario, dados):
    alternativas = None

    if dados["tipo"] == "MULTIPLA_ESCOLHA":
        alternativas = normalizar_alternativas(
            dados.get("alternativas")
        )

    return Questao.objects.create(
        criado_por=usuario,
        tipo=dados["tipo"],
        enunciado=dados["enunciado"],
        solucao=dados["solucao"],
        alternativas=alternativas,
        gabarito=dados.get("gabarito"),
    )

def editar_questao(questao, dados):
    questao.tipo = dados["tipo"]
    questao.enunciado = dados["enunciado"]
    questao.solucao = dados["solucao"]

    if questao.tipo == "MULTIPLA_ESCOLHA":
        questao.alternativas = normalizar_alternativas(
            dados.get("alternativas")
        )
        questao.gabarito = dados["gabarito"]

    else:
        questao.alternativas = None
        questao.gabarito = None

    questao.revisado_por = None
    questao.revisado_em = None

    questao.save()

    return questao

def revisar_questao(questao, usuario):
    questao.revisado_por = usuario
    questao.revisado_em = timezone.now()
    questao.save()

    return questao