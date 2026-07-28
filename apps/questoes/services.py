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