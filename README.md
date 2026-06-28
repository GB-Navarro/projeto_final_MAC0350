# Plataforma de Questões — OBCON

Plataforma web com cadastro de alunos e administradores, área do aluno e área de admin para criar, editar e revisar questões com matemática em LaTeX.

> Descrição completa → [spec.md](spec.md) · Tarefas → [backlog.md](backlog.md) · Testes → [testes.md](testes.md) · Convenções (AI) → [CLAUDE.md](CLAUDE.md)

---

## Documentação

| Arquivo | Para quem | O que contém |
|---|---|---|
| [CLAUDE.md](CLAUDE.md) | Agentes de AI | Arquitetura, estrutura de pastas, regras de negócio, convenções de código e Definition of Done. Lido automaticamente por agentes ao entrar no projeto. |
| [spec.md](spec.md) | Humanos + AI | Descrição completa do produto: o que é, escopo, stack, modelo de domínio com todos os campos e regras, tabela de rotas e roadmap por fase. |
| [backlog.md](backlog.md) | Humanos | 21 cards prontos para colar em kanban (Trello, Notion, GitHub), organizados em 2 epics. Cada card tem camada, descrição e critérios de aceitação. |
| [testes.md](testes.md) | Humanos + AI | Ciclo TDD passo a passo, template de critério de aceitação (Gherkin), template de prompt para gerar testes com AI e exemplos prontos de testes pytest. |
| [guia-dev.md](guia-dev.md) | Humanos (devs) | Guia prático de como construir no projeto: fluxo de trabalho, ordem de implementação, padrões de código (models, services, views, templates, testes) e uso de IA. |

---

## O que instalar

- **Python 3.12+** — https://www.python.org/downloads/
- **Git**

SQLite vem com o Python. KaTeX é carregado como estático/CDN — nada extra para instalar.

---

## Como instalar

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # cria o admin inicial — único que aprova outros admins
```

`requirements.txt`:
```
Django
pytest
pytest-django
model-bakery
coverage
```

---

## Como rodar

```bash
source .venv/bin/activate
python manage.py runserver
```

Acesse **http://localhost:8000**.

---

## Como rodar os testes

```bash
pytest
coverage run -m pytest && coverage report -m
```
