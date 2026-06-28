# Guia do Desenvolvedor — Plataforma OBCON

> Como construir neste projeto: fluxo de trabalho, padrões de código e uso de IA.
> Leia [CLAUDE.md](../CLAUDE.md) antes deste guia. Tarefas → [backlog.md](backlog.md) · Testes → [testes.md](testes.md)

---

## 1. Antes de escrever qualquer código

1. Pegue um card do [backlog.md](backlog.md).
2. Leia os **critérios de aceitação** do card.
3. Escreva o critério no formato Gherkin (Template A do [testes.md](testes.md)) — **antes de abrir o editor**.
4. Crie a branch: `git checkout -b feat/<nome-curto>`.

Se for usar IA para gerar o teste, cole o critério no Template B do [testes.md](testes.md). O teste deve **falhar** antes de você implementar qualquer coisa.

---

## 2. Ordem de implementação de um card

Para qualquer feature que envolva banco + backend + frontend, siga esta ordem:

```
1. Model (models.py)
2. Migração (makemigrations + migrate)
3. Serviço (services.py)
4. View (views.py)
5. URL (urls.py)
6. Template (.html)
7. Teste de integração (tests/test_views.py)
```

Cards de camada única (só `[Banco]`, só `[Backend]`, só `[Frontend]`) seguem só a etapa correspondente.

---

## 3. Git

```bash
# criar branch
git checkout -b feat/cadastro-aluno

# commitar (Conventional Commits)
git commit -m "feat: adiciona cadastro de aluno com geração de código"
git commit -m "test: testa que cadastro gera código no formato E+hash"
git commit -m "fix: corrige unicidade do código em colisão"

# antes de abrir PR
pytest
```

Prefixos: `feat` (nova funcionalidade), `fix` (correção), `test` (só testes), `chore` (infra/config), `docs` (documentação).

---

## 4. Models e migrações

```python
# apps/contas/models.py
class Aluno(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    codigo = models.CharField(max_length=7, unique=True)
    # ...
```

```bash
python manage.py makemigrations contas   # sempre após mudar o model
python manage.py migrate
```

**Regras:**
- Commite a migração junto com o model — nunca separe os dois commits.
- Não edite arquivos de migração manualmente.
- Use `settings.AUTH_USER_MODEL` (não `"contas.Usuario"`) para FKs que referenciam o usuário.

---

## 5. Services vs. Views

A lógica de negócio vai em `services.py`. A view só valida, chama o serviço e redireciona.

```python
# apps/contas/services.py
def cadastrar_aluno(form_data: dict) -> Aluno:
    # gera código, cria Usuario e Aluno, retorna o Aluno
    ...

# apps/contas/views.py
def cadastro_aluno(request):
    if request.method == "POST":
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            cadastrar_aluno(form.cleaned_data)
            return redirect("contas:login")
    else:
        form = CadastroAlunoForm()
    return render(request, "contas/cadastro_aluno.html", {"form": form})
```

---

## 6. URLs e namespacing

Cada app tem `app_name` definido em `urls.py`. Adicione rotas assim:

```python
# apps/contas/urls.py
app_name = "contas"

urlpatterns = [
    path("cadastro/aluno/", views.cadastro_aluno, name="cadastro_aluno"),
    path("login/",          views.login_view,     name="login"),
    path("logout/",         views.logout_view,    name="logout"),
]
```

Para referenciar no Python: `reverse("contas:cadastro_aluno")`
Para referenciar no template: `{% url "contas:cadastro_aluno" %}`

---

## 7. Templates HTML

Todo template começa com:

```html
{% extends "base.html" %}

{% block title %}Cadastro de Aluno{% endblock %}

{% block content %}
  <h1>Cadastro de Aluno</h1>
  <!-- conteúdo da página -->
{% endblock %}
```

**Blocos disponíveis no `base.html`:**

| Bloco | Quando usar |
|---|---|
| `title` | Sempre — título da aba |
| `content` | Sempre — conteúdo da página |
| `extra_css` | Raramente — CSS específico desta página |
| `extra_js` | Raramente — JS específico desta página |

**Formulários Django com Bootstrap:**

```html
<form method="post">
  {% csrf_token %}
  {% for field in form %}
    <div class="mb-3">
      <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}
        <div class="invalid-feedback d-block">{{ field.errors.0 }}</div>
      {% endif %}
    </div>
  {% endfor %}
  <button type="submit" class="btn btn-primary">Salvar</button>
</form>
```

**LaTeX com KaTeX:**

O `base.html` já carrega KaTeX e renderiza automaticamente. Basta usar `$...$` (inline) ou `$$...$$` (bloco) em qualquer texto da página — sem configuração extra.

```html
<p>A área de um círculo é $A = \pi r^2$.</p>
```

---

## 8. Testes

```bash
pytest                          # todos
pytest apps/contas -v           # um app
pytest -k "cadastro" -v         # por palavra-chave
coverage run -m pytest && coverage report -m
```

**Fixtures disponíveis em `conftest.py`:**

| Fixture | O que entrega |
|---|---|
| `superuser` | `Usuario` com `is_superuser=True` |
| `admin_aprovado` | `Administrador` aprovado *(descomentar após F1-2)* |
| `client_admin` | client já logado como admin *(descomentar após F1-2)* |
| `aluno` | `Aluno` criado com baker *(descomentar após F1-2)* |
| `client_aluno` | client já logado como aluno *(descomentar após F1-2)* |

**Padrão de teste (AAA):**

```python
@pytest.mark.django_db
def test_cadastro_de_aluno_gera_codigo(client):
    # Arrange
    dados = {"nome": "Ana", "email": "ana@ex.com", "senha": "senha-123", ...}

    # Act
    client.post(reverse("contas:cadastro_aluno"), dados)

    # Assert
    aluno = Aluno.objects.get(usuario__email="ana@ex.com")
    assert aluno.codigo.startswith("E")
    assert len(aluno.codigo) == 7
```

Um `assert` principal por teste. Teste comportamento observável, não detalhe interno.

---

## 9. Usando IA para gerar testes

1. Escreva o critério (Template A do [testes.md](testes.md)).
2. Cole no Template B e envie para a IA.
3. **Rode o teste gerado — ele deve falhar.** Se passar, o teste está errado.
4. Implemente o código até o teste passar.
5. Leia o teste e confirme que ele cobre o critério, não apenas o código que você escreveu.

A IA gera a digitação. Você garante que o critério está correto.

---

## 10. Checklist antes do PR

- [ ] `pytest` verde localmente
- [ ] Migração commitada junto com o model
- [ ] Nenhum `print` ou `breakpoint()` esquecido
- [ ] Sem secrets ou `.env` no commit
- [ ] Branch parte de `main` atualizado
