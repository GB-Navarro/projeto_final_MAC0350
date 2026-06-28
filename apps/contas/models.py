from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    ALUNO = 'ALUN'
    ADM = 'ADM'
    TIPO_CHOICES = [
        (ALUNO, 'Aluno'),
        (ADM, 'Administrador'),
    ]
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
