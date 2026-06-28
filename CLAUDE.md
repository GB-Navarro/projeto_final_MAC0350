# CLAUDE.md — Plataforma OBCON

> Leia isto antes de qualquer coisa.
> Setup → [README.md](README.md) · Descrição completa → [spec.md](docs/spec.md) · Tarefas → [backlog.md](docs/backlog.md) · Testes → [testes.md](docs/testes.md) · Guia do dev → [guia-dev.md](docs/guia-dev.md)

Stack: **Django full-stack** · **SQLite** · **Bootstrap 5** (CDN) · **KaTeX** (CDN) · testes com **pytest-django + model_bakery**.

---

## Arquitetura

Fluxo: Views → `services.py` → Models (ORM) → SQLite

**LaTeX é renderizado no cliente com KaTeX. O servidor nunca compila LaTeX.**

### O que vai em cada pasta

```
config/
  settings.py     ← INSTALLED_APPS, AUTH_USER_MODEL, banco, templates, static, login URLs
  urls.py         ← inclui apps.contas.urls e apps.questoes.urls
  wsgi.py         ← entrypoint de servidor (não editar)

apps/
  __init__.py     ← torna apps/ um pacote Python (não editar)

  contas/
    models.py     ← Usuario (AbstractUser), Aluno, Administrador
    services.py   ← lógica de negócio: gerar código do aluno, aprovar admin
    views.py      ← views finas; toda regra vai em services.py
    urls.py       ← rotas do app com namespace 'contas'
    apps.py       ← AppConfig com name='apps.contas' (não editar)
    migrations/   ← geradas por makemigrations; commitar junto com o modelo
    tests/
      __init__.py
      test_models.py    ← testes de modelo e serviço (unitários)
      test_views.py     ← testes de view via client (integração)

  questoes/       ← estrutura idêntica à de contas
    models.py     ← Questao
    services.py   ← lógica: marcar revisão
    views.py, urls.py, apps.py, migrations/, tests/

templates/
  base.html           ← layout base (Bootstrap, KaTeX via CDN)
  contas/
    login.html
    cadastro_aluno.html
    cadastro_adm.html
    aprovacoes.html
  questoes/
    lista.html
    form_questao.html  ← reutilizado por criar e editar

static/
  css/
    style.css     ← estilos próprios (complementam Bootstrap)
  js/
    katex-init.js ← inicializa o preview KaTeX nos campos de enunciado/solucao
  (Bootstrap e KaTeX chegam via CDN — não ficam aqui)
```

---

## Regras críticas de negócio

1. `AUTH_USER_MODEL = "contas.Usuario"` — estende `AbstractUser`, `USERNAME_FIELD = "email"`, campo `username` removido.
2. Código do aluno: `E` + `uuid4().hex[:6]` (ex: `Ea3f9c12`), `unique=True`, até 5 tentativas em colisão.
3. Admin inicial = superuser (`is_superuser=True`) criado via `createsuperuser`. **Só ele aprova novos admins** — verificado com `request.user.is_superuser`.
4. Novo admin nasce `aprovado=False` — login retorna 200 com *"Sua conta ainda não foi aprovada."*
5. Revisão de questão: marcar de novo **sobrescreve** `revisado_por`/`revisado_em` — vale a última.
6. Qualquer admin pode editar qualquer questão.
7. `alternativas`: `JSONField` schema `{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}` · `gabarito`: `CharField` choices A–E.
8. `enunciado` e `solucao` aceitam LaTeX — ambos usam o editor KaTeX (F2-6).

---

## Convenções de código

- Lógica de negócio em `services.py`; views finas.
- Feature branches: `feat/<curto>`. Commits: Conventional Commits.
- Nunca secrets no repositório — `.env` no `.gitignore`.
- Rodar `pytest` antes de abrir PR.

---

## Definition of Done (por feature)

- [ ] Critério de aceitação escrito **antes** do código e salvo em `docs/criterios/<id-da-tarefa>.md` (ver [testes.md](docs/testes.md)).
- [ ] Teste gerado e **conferido por humano** (reflete a regra, não a implementação).
- [ ] Testes passando.
- [ ] `pytest` verde localmente antes do PR.
