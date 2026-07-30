from django.db import models
from django.conf import settings

# Create your models here.

class Questao(models.Model):
    class Tipo(models.TextChoices):
        MULTIPLA_ESCOLHA = "MULTIPLA_ESCOLHA", "Múltipla escolha"
        DISSERTATIVA = "DISSERTATIVA", "Dissertativa"

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="questoes_criadas",
    )

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
    )

    enunciado = models.TextField()
    solucao = models.TextField()

    alternativas = models.JSONField(
        null=True,
        blank=True,
    )

    gabarito = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
        ],
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    revisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questoes_revisadas",
    )

    revisado_em = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Questão {self.id}"