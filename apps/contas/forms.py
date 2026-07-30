from django import forms

from apps.contas.models import Aluno, Usuario

class CadastroAlunoForm(forms.Form):
    nome = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    genero = forms.ChoiceField(choices=Aluno.GENERO_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    serie = forms.ChoiceField(choices=Aluno.SERIE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    escola = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    tipo_escola = forms.ChoiceField(choices=Aluno.TIPO_ESCOLA_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    professor_nome = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    professor_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

class CadastroAdministradorForm(forms.Form):
    nome = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email
