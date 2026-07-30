from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve possuir um email.")

        email = self.normalize_email(email)

        usuario = self.model(
            email=email,
            **extra_fields,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tipo", Usuario.ADM)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser precisa ter is_staff=True.")

        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    objects = UsuarioManager()

    ALUNO = 'ALUNO'
    ADM = 'ADM'
    TIPO_CHOICES = [
        (ALUNO, 'Aluno'),
        (ADM, 'Administrador'),
    ]
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES, default = ADM)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Aluno(models.Model):
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]
    SERIE_CHOICES = [
        ('9EF', '9º ano EF'),
        ('1EM', '1ª série EM'),
        ('2EM', '2ª série EM'),
        ('3EM', '3ª série EM'),
        ('4EM', '4ª série EM'),
    ]
    TIPO_ESCOLA_CHOICES = [
        ('PUBLICA', 'Pública'),
        ('PRIVADA', 'Privada'),
        ('SELETIVA', 'Seletiva'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aluno'
    )
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    serie = models.CharField(max_length=3, choices=SERIE_CHOICES)
    escola = models.CharField(max_length=200)
    tipo_escola = models.CharField(max_length=8, choices=TIPO_ESCOLA_CHOICES)
    professor_nome = models.CharField(max_length=200, blank=True, null=True)
    professor_email = models.EmailField(blank=True, null=True)
    codigo = models.CharField(max_length=7, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            from apps.contas.services import gerar_codigo_aluno
            self.codigo = gerar_codigo_aluno()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class Administrador(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='administrador'
    )
    aprovado = models.BooleanField(default=False)
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aprovacoes',
    )
    aprovado_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.usuario.email
