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

### Branches

```bash
git checkout -b feat/cadastro-aluno   # feature
git checkout -b fix/codigo-colisao    # correção
```

Formato: `<tipo>/<nome-curto-em-kebab-case>`. Sem espaços, sem acentos.

---

### Commits — prefixos

| Prefixo | Quando usar | Exemplos |
|---|---|---|
| `add:` | Adiciona arquivo, modelo, funcionalidade ou dependência | modelo Aluno, nova view, novo campo |
| `fix:` | Corrige um bug ou comportamento errado | unicidade do código, redirect errado |
| `chore:` | Infra, config, reorganização sem impacto funcional | settings, gitignore, mover arquivos |
| `test:` | Adiciona ou corrige testes (sem mudar código de produção) | novo test_views, fixture faltando |
| `docs:` | Altera só documentação | atualiza guia-dev, corrige link |
| `refactor:` | Melhora o código sem mudar comportamento | extrai lógica para services.py |
| `style:` | Formatação, CSS, espaçamento — sem mudança de lógica | ajusta margem, alinha campo |

---

### Regras da mensagem

```
add: adiciona modelo Aluno com campos de série e escola
^──^ ^────────────────────────────────────────────────^
tipo  descrição em minúsculo, sem ponto final, até ~72 chars
```

- **Minúsculo** após os dois-pontos.
- **Sem ponto final.**
- **Imperativo:** `adiciona`, `corrige`, `remove` — não `adicionando`, `adicionei`.
- **Em português.**
- **Máximo ~72 caracteres** na primeira linha.
- Se precisar explicar o *porquê*, adicione uma linha em branco e um parágrafo depois:

```bash
git commit -m "fix: corrige geração de código duplicado em cadastro simultâneo

Colisão era possível com múltiplas requisições. Adicionado retry
com até 5 tentativas antes de lançar exceção."
```

---

### Exemplos: bom vs. ruim

| Ruim | Bom |
|---|---|
| `commit das alterações` | `add: adiciona view de cadastro de aluno` |
| `fix bug` | `fix: corrige redirect após login de admin pendente` |
| `WIP` | `test: adiciona teste de aprovação de administrador` |
| `add: Adicionando o modelo de Questão.` | `add: adiciona modelo Questao com campos de revisão` |
| `chore: moved files` | `chore: move documentação para pasta docs/` |

---

### Fluxo completo

```bash
git checkout -b add/modelo-aluno

# ... edita models.py e cria a migração ...

git add apps/contas/models.py apps/contas/migrations/0002_aluno.py
git commit -m "add: adiciona modelo Aluno com geração de código"

git add apps/contas/tests/test_models.py
git commit -m "test: testa que código do aluno começa com E e tem 7 chars"

pytest   # verde antes de abrir PR
```

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

---

## 11. Métricas de código (entrega de milestone)

O professor pede, ao final de cada milestone, um relatório de **Complexidade Ciclomática** e **Índice de Manutenibilidade** com `radon` e `pylint`.

### Quando rodar

| Evento | Milestone |
|---|---|
| F1-11 concluído (toda a Fase 1 entregue) | `1` |
| F2-10 concluído (toda a Fase 2 entregue) | `2` |

### Como rodar (Windows)

```powershell
.\scripts\relatorio_metricas.ps1 -Milestone 1
```

O script cria a pasta `metricas/milestone_1/` com 5 arquivos:

| Arquivo | Ferramenta | O que mostra |
|---|---|---|
| `raw.txt` | `radon raw` | LOC, SLOC, LLOC, comentários, linhas em branco |
| `cc.txt` | `radon cc` | Complexidade Ciclomática por função (rank A–F) + média |
| `halstead.txt` | `radon hal` | Difficulty, Effort, Volume (Halstead) |
| `mi.txt` | `radon mi` | Índice de Manutenibilidade por arquivo (0–100) |
| `pylint.txt` | `pylint` | Nota geral (0–10) e lista de avisos |

### Comandos avulsos (referência rápida)

```bash
radon cc  apps/ -s -a   # Complexidade Ciclomática: rank A–F por função + média
radon mi  apps/ -s      # Maintainability Index: 0–100 por arquivo
radon raw apps/ -s      # Linhas de código (LOC/SLOC/LLOC)
radon hal apps/         # Halstead: Difficulty, Effort, Volume
pylint    apps/         # Qualidade geral (0–10)
```

### O que significam os ranks (Complexidade Ciclomática)

| Rank | CC | Risco |
|---|---|---|
| A | 1–5 | baixo (ideal) |
| B | 6–10 | bem estruturado |
| C | 11–20 | moderado |
| D | 21–30 | mais complexo |
| E | 31–40 | alarmante |
| F | 41+ | propenso a erros |

### O que commitar

Versione a pasta `metricas/` no repositório para mostrar a **evolução entre milestones**:

```bash
git add metricas/milestone_1/
git commit -m "docs: adiciona relatorio de metricas da milestone 1"
```
