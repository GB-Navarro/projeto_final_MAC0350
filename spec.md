# Plataforma de Questões — OBCON

> Descrição do projeto (o *quê* e o *porquê*).
> Como instalar e rodar → [README.md](README.md) · Fluxo de testes → [testes.md](testes.md) · Tarefas → [backlog.md](backlog.md) · Convenções (AI) → [CLAUDE.md](CLAUDE.md)

---

## 1. O que é

Plataforma web com:
- **Cadastro de alunos** (página própria) e **cadastro de administradores** (página própria).
- **Login compartilhado** (aluno e admin entram pela mesma tela).
- **Área do aluno** (por enquanto, placeholder).
- **Área do administrador**: criar, editar e revisar questões.

*(Futuramente poderá ser usada na Olimpíada Brasileira de Economia — fora do escopo atual.)*

---

## 2. Escopo atual

**Inclui:**
- Cadastro de aluno com os campos da §5, gerando um **código de identificação** (`Exxxxxx`).
- Cadastro de administrador, que **só passa a valer após aprovação** de um admin já cadastrado.
- Login e logout compartilhados.
- Área do aluno (placeholder).
- Criar, editar e listar questões (com matemática em LaTeX, preview no navegador).
- **Revisão simples:** marcar uma questão como revisada, registrando **quem** revisou e **quando**. Sem fluxo de estados/aprovação.

**Fora do escopo por agora:** fluxo de revisão com etapas, provas online, automações, LGPD.

---

## 3. Stack

- **Django full-stack** (backend + frontend em templates). Um framework só.
- **Banco: SQLite** (padrão do Django, zero configuração). Trocar para PostgreSQL depois é só mudar `DATABASES`.
- **Matemática: KaTeX no cliente.** O LaTeX **não** é compilado no servidor.
- **CSS: Bootstrap 5 via CDN** (sem build step, como o KaTeX).

---

## 4. Arquitetura (simples)

Dois apps: `contas` (usuários, cadastros, login, aprovação) e `questoes` (questões + marca de revisão).

```
Navegador (templates Django + KaTeX)
        │  HTTPS (sessão + CSRF do Django)
        ▼
Views  →  Serviços (services.py)  →  Modelos (ORM)  →  SQLite
```

```
config/                 # projeto Django (settings, urls)
apps/
  contas/               # Usuario, Aluno, Administrador, cadastro, login, aprovação
  questoes/             # Questao, criar/editar, marca de revisão
templates/              # telas
static/                 # CSS, JS, KaTeX
```

---

## 5. Modelo de domínio

**Usuario** (estende `AbstractUser` do Django): `email` (único, `USERNAME_FIELD`), `nome` (`first_name` do AbstractUser), `senha` (hash — gerenciado pelo Django), `tipo` (ALUNO ou ADM). O campo `username` é removido. `AUTH_USER_MODEL = "contas.Usuario"` no settings. O superuser (`is_superuser=True`) é criado via `createsuperuser` e é o único que aprova novos admins — verificado com `request.user.is_superuser`.

**Aluno** (perfil 1:1 com Usuario):
- `genero` (masculino / feminino / outro), `serie` (choices: `9EF` 9º ano EF · `1EM` 1ª série EM · `2EM` 2ª série EM · `3EM` 3ª série EM), `escola`, `tipo_escola` (PUBLICA / PRIVADA / SELETIVA)
- `professor_nome` *(opcional)*, `professor_email` *(opcional)*
- `codigo` — formato `E` + `uuid4().hex[:6]` (ex: `Ea3f9c12`), `unique=True`, gerado no cadastro com até 5 tentativas em caso de colisão.

**Administrador** (perfil 1:1 com Usuario):
- `aprovado` (bool), `aprovado_por` (o superuser), `aprovado_em` (data/hora).

**Questao:**
- `criado_por`, `tipo` (MULTIPLA_ESCOLHA ou DISSERTATIVA), `enunciado` (LaTeX), `solucao` (LaTeX), `criado_em`, `atualizado_em`
- múltipla escolha usa `alternativas` (`JSONField`, schema: `{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}`) e `gabarito` (`CharField`, choices A–E); dissertativa usa só enunciado e solução
- `revisado_por` *(nulo até revisar)*, `revisado_em` *(nulo até revisar)*.

**Regras:**
- Ao cadastrar um aluno, o sistema gera o `codigo` (`E` + hash curto) automaticamente.
- O **admin inicial é um superuser criado direto no banco** (`createsuperuser`). **Só ele aprova novos admins.**
- Um administrador recém-cadastrado nasce **pendente** (`aprovado = False`) e **só loga depois de aprovado pelo superuser**.
- A questão guarda a **última** revisão: marcar de novo sobrescreve `revisado_por`/`revisado_em`. A tela mostra *"Revisada por X em T"*.

---

## 6. Páginas e rotas

| Rota | Ação | Quem |
|---|---|---|
| `/cadastro/aluno/` | cadastro de aluno | público |
| `/cadastro/adm/` | cadastro de admin (fica pendente) | público |
| `/login/`, `/logout/` | login/logout compartilhado | público / autenticado |
| `/aluno/` | área do aluno (placeholder) | aluno |
| `/adm/questoes/` | lista de questões | admin |
| `/adm/questoes/nova/` | criar questão | admin |
| `/adm/questoes/<id>/editar/` | editar questão | admin |
| `/adm/questoes/<id>/revisar/` | marcar como revisada | admin |
| `/adm/aprovacoes/` | aprovar admins pendentes | superuser |

---

## 7. Segurança (mínima e suficiente para o escopo)

- **Login obrigatório** nas áreas de aluno e de admin.
- **Admin só acessa a área de admin depois de aprovado.** Login com admin pendente retorna 200 com mensagem *"Sua conta ainda não foi aprovada."*
- **Apenas o superuser (admin inicial) aprova novos admins.**
- **CSRF** nos formulários (padrão do Django).
- **LaTeX renderizado no cliente** (KaTeX) — o servidor nunca compila LaTeX.

---

## 8. Roadmap

| Fase | Entregas |
|---|---|
| **1 — Contas e acesso** | Projeto Django, modelos de usuário, cadastro de aluno (com código), cadastro + aprovação de admin, login compartilhado, área do aluno (placeholder) |
| **2 — Questões** | Modelo `Questao`, criar/editar/listar, editor LaTeX + preview KaTeX, marcar como revisada |
