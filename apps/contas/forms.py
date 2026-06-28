from django import forms

from apps.contas.models import Aluno, Usuario


class CadastroAlunoForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
    genero = forms.ChoiceField(choices=Aluno.GENERO_CHOICES)
    serie = forms.ChoiceField(choices=Aluno.SERIE_CHOICES)
    escola = forms.CharField(max_length=200)
    tipo_escola = forms.ChoiceField(choices=Aluno.TIPO_ESCOLA_CHOICES)
    professor_nome = forms.CharField(max_length=200, required=False)
    professor_email = forms.EmailField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email
